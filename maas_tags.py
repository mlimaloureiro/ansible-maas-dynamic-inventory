#!/usr/bin/env python

import click
import sys
import os
import json
import uuid
import requests
import requests_cache
import oauth2 as oauth

DEFAULTS = {
    "cache_path": "~/.ansible/tmp",
    "cache_expire": 300
}


class MaasStatusEnum:
    """ Class used to enumerate MAAS statuses """
    DEPLOYED = 'Deployed'


class Authenticator:
    """ Class used to authenticate requests and build request headers """

    def __init__(self, maas_api_url: str, maas_api_key: str):
        self.maas_api_url = maas_api_url
        self.maas_api_key = maas_api_key

    def create_headers(self) -> dict:
        (consumer_key, key, secret) = self.maas_api_key.split(':')

        resource_token_string = "oauth_token_secret={}&oauth_token={}".format(secret, key)
        resource_token = oauth.Token.from_string(resource_token_string)

        consumer_token = oauth.Consumer(consumer_key, "")

        oauth_request = oauth.Request.from_consumer_and_token(
            consumer_token, token=resource_token, http_url=self.maas_api_url,
            parameters={'auth_nonce': uuid.uuid4().hex})

        oauth_request.sign_request(oauth.SignatureMethod_PLAINTEXT(), consumer_token, resource_token)
        headers = oauth_request.to_header()
        headers['Accept'] = 'application/json'

        return headers


class Fetcher:
    """ Class used to fetch nodes data from MAAS """

    def __init__(self, authenticator: Authenticator, maas_api_url: str):
        self.authenticator = authenticator
        self.maas_api_url = maas_api_url

    def fetch_machines_grouped_by_tags(self) -> dict:
        tags_summary = self._fetch_tags_summary()
        groups = {}
        for tag in tags_summary:
            machines = self._fetch_machines_by_tag(tag['name'])
            groups[tag['name']] = machines

        # i.e: { 'group-1': [ { fqdn: 'host-1', .. }, { fqdn: 'host-2', .. } ]}
        return groups

    def _fetch_tags_summary(self) -> dict:
        url = "{}/tags/".format(self.maas_api_url.rstrip())

        return self._api_call(url)

    def _fetch_machines_by_tag(self, tag_name: str) -> dict:
        url = "{}/tags/{}/?op=machines".format(self.maas_api_url.rstrip(), tag_name)

        return self._api_call(url)

    def _api_call(self, url: str) -> dict:
        headers = self.authenticator.create_headers()
        request = requests.get(url, headers=headers)
        response = json.loads(request.text)

        return response


class InventoryBuilder:
    """ Class used to build the inventory """

    def build_from_tagged_machines(self, machines: dict) -> dict:
        inventory = self._get_default_inventory()

        for tag_name, grouped_machines in machines.items():
            hosts = []
            ansible_group_name = tag_name
            for machine in grouped_machines:
                if machine['status_name'] == MaasStatusEnum.DEPLOYED:
                    hosts.append(machine['fqdn'])
                    inventory['_meta']['hostvars'][machine['fqdn']] = self._build_meta(machine)

            inventory[ansible_group_name] = self._build_hosts(hosts)

        return inventory

    def _get_default_inventory(self) -> dict:
        return {
            '_meta': {
                'hostvars': {}
            }
        }

    def _build_meta(self, machine: dict) -> dict:
        return {
            'ansible_ssh_host': machine['ip_addresses'][0],
            'ansible_ssh_host_private': machine['ip_addresses'][0]
        }

    def _build_hosts(self, hosts_list: list) -> dict:
        return {
            'hosts': hosts_list,
            'vars': {}
        }


@click.command()
@click.option('--list', 'list_flag', '-l', is_flag=True)
@click.option('--refresh-cache', 'refresh_cache', is_flag=True)
def cli(list_flag, refresh_cache):
    _setup_cache(refresh_cache)

    maas_api_url = os.environ.get('MAAS_API_URL')
    maas_api_key = os.environ.get('MAAS_API_KEY')
    authenticator = Authenticator(maas_api_url, maas_api_key)
    fetcher = Fetcher(authenticator, maas_api_url)
    builder = InventoryBuilder()

    if not maas_api_key:
        sys.exit("MAAS_API_KEY environment variable not found")
    if not maas_api_url:
        sys.exit("MAAS_API_URL environment variable not found")

    if list_flag:
        click.echo(_list(fetcher, builder))


def _list(fetcher: Fetcher, builder: InventoryBuilder) -> dict:
    machines = fetcher.fetch_machines_grouped_by_tags()
    inventory = builder.build_from_tagged_machines(machines)

    return json.dumps(inventory, indent=4)


def _setup_cache(refresh_cache: bool, path=DEFAULTS["cache_path"], expire_after=DEFAULTS["cache_expire"]):
    folder_path = os.path.expanduser(path)
    file_name = os.path.join(folder_path, "ansible-maas-dynamics-inventory")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    requests_cache.install_cache(file_name, expire_after=expire_after)

    if refresh_cache and os.path.isfile("{}.sqlite".format(file_name)):
        requests_cache.clear()


if __name__ == '__main__':
    cli()
