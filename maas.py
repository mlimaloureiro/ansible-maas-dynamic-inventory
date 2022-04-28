#!/usr/bin/env python

import argparse
import configparser
import json
import os
import re
import sys
import uuid

import oauth2 as oauth
import requests
import requests_cache

DEFAULTS = {
    "group_machines_by": "tags",
    "cache_filename": "ansible-maas-dynamics-inventory",
    "cache_path": "~/.ansible/tmp",
    "cache_max_age_in_seconds": 300,
    "refresh_cache": False
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

    def __init__(self, authenticator: Authenticator, maas_api_url: str, cache_settings: dict):
        self.authenticator = authenticator
        self.maas_api_url = maas_api_url
        self._config_cache(cache_settings)

    def fetch_machine_by_node(self, system_id: str) -> dict:
        return self._fetch_node(system_id)

    def fetch_machines_grouped_by_hostname(self) -> dict:
        machines = self._fetch_all_machines()
        groups = {}
        for machine in machines:
            prefix = self._get_hostname_prefix(machine['hostname'])
            self._add_machine_to_group(groups, prefix, machine)

        # i.e: { 'hostname': [ { fqdn: 'host-1', .. }, { fqdn: 'host-2', .. } ]}
        return groups

    def fetch_machines_grouped_by_tags(self) -> dict:
        tags_summary = self._fetch_tags_summary()
        groups = {}
        for tag in tags_summary:
            machines = self._fetch_machines_by_tag(tag['name'])
            groups[tag['name']] = machines

        # i.e: { 'group-1': [ { fqdn: 'host-1', .. }, { fqdn: 'host-2', .. } ]}
        return groups

    def _config_cache(self, cache_settings: dict):
        ''' Configure the cache settings '''

        folder_path = os.path.expanduser(os.path.expandvars(cache_settings['path']))
        file_name = os.path.join(folder_path, cache_settings['filename'])

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        requests_cache.install_cache(file_name, expire_after=cache_settings['max_age_in_seconds'])

        if cache_settings['refresh_cache'] and os.path.isfile("{}.sqlite".format(file_name)):
            requests_cache.clear()

    def _get_hostname_prefix(self, hostname: str) -> str:
        result = re.findall(r'([a-zA-Z]+)', hostname)
        return result[0] if len(result) else None

    def _add_machine_to_group(self, groups: dict, hostname: str, machine: dict) -> dict:
        if hostname in groups:
            groups[hostname].append(machine)
            return groups

        groups[hostname] = [machine]

        return groups

    def _fetch_all_machines(self) -> dict:
        url = "{}/machines/".format(self.maas_api_url.rstrip())

        return self._api_call(url)

    def _fetch_tags_summary(self) -> dict:
        url = "{}/tags/".format(self.maas_api_url.rstrip())

        return self._api_call(url)

    def _fetch_machines_by_tag(self, tag_name: str) -> dict:
        url = "{}/tags/{}/?op=machines".format(self.maas_api_url.rstrip(), tag_name)

        return self._api_call(url)

    def _fetch_node(self, system_id: str) -> dict:
        url = "{}/nodes/{}".format(self.maas_api_url.rstrip(), system_id)

        return self._api_call(url)

    def _api_call(self, url: str) -> dict:
        headers = self.authenticator.create_headers()
        request = requests.get(url, headers=headers)
        response = json.loads(request.text)

        return response


class InventoryBuilder:
    """ Class used to build the inventory """

    def build_from_machines(self, machines: dict) -> dict:
        inventory = self._get_default_inventory()

        for key, grouped_machines in machines.items():
            hosts = []
            ansible_group_name = key
            for machine in grouped_machines:
                if machine['status_name'] == MaasStatusEnum.DEPLOYED:
                    hosts.append(machine['fqdn'])
                    inventory['_meta']['hostvars'][machine['fqdn']] = self._build_meta(machine)

            inventory[ansible_group_name] = self._build_hosts(hosts)

        return inventory

    def build_from_machine_node(self, machine: dict) -> dict:
        machine.update(self._build_meta(machine))

        return machine

    def build_default(self) -> dict:
        return self._get_default_inventory()

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


class Main(object):

    def __init__(self):
        """ Main execution path """

        self.credentials = {}

        self.parse_cli_args()
        self.load_settings()

        self.authenticator = Authenticator(self.maas_api_url, self.maas_api_key)
        self.fetcher = Fetcher(self.authenticator, self.maas_api_url, self.cache_settings)
        self.builder = InventoryBuilder()

        self.inventory = self._default_inventory()

        if self.args.list:
            print(self._list())
        elif self.args.host:
            print(self._host())

    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on MAAS')
        parser.add_argument('--list', action='store_true', default=False,
                            help='List instances (default: True)')
        parser.add_argument('--host', action='store',
                            help='Get all the variables about a specific instance')
        parser.add_argument('--refresh-cache', action='store_true', default=False,
                            help='Force refresh of cache by making API requests to MAAS (default: False)')
        self.args = parser.parse_args()

    def load_settings(self):
        ''' Read configuration settings from ini file and env vars '''

        config = self._load_config_file()
        self._load_auth_settings(config)
        self._load_cache_settings(config)
        self._load_maas_settings(config)

    def _load_config_file(self):
        scriptbasename = os.path.basename(__file__)
        scriptbasename = scriptbasename.replace('.py', '')

        ini_path_defaults = {
            'ini_path': os.path.join(os.path.dirname(__file__), '{}.ini'.format(scriptbasename)),
            'ini_fallback': os.path.join(os.path.dirname(__file__), 'maas.ini')
        }

        config = configparser.ConfigParser(DEFAULTS)
        maas_ini_path = os.environ.get('MAAS_INI_PATH', ini_path_defaults['ini_path'])
        maas_ini_path = os.path.expanduser(os.path.expandvars(maas_ini_path))

        if not os.path.isfile(maas_ini_path):
            maas_ini_path = os.path.expanduser(os.path.expandvars(ini_path_defaults['ini_fallback']))

        if os.path.isfile(maas_ini_path):
            config.read(maas_ini_path)

        return config

    def _load_auth_settings(self, config):
        if not config.has_section('auth'):
            config.add_section('auth')

        self.maas_api_url = os.environ.get('MAAS_API_URL', config.get('auth', 'maas_api_url', fallback=None))
        self.maas_api_key = os.environ.get('MAAS_API_KEY', config.get('auth', 'maas_api_key', fallback=None))

        if not self.maas_api_url:
            sys.exit("MAAS_API_URL environment variable not found")
        if not self.maas_api_key:
            sys.exit("MAAS_API_KEY environment variable not found")

    def _load_cache_settings(self, config):
        if not config.has_section('cache'):
            config.add_section('cache')

        self.cache_settings = {}
        self.cache_settings['filename'] = config.get('cache', 'cache_filename')
        self.cache_settings['path'] = config.get('cache', 'cache_path')
        self.cache_settings['max_age_in_seconds'] = config.getint('cache', 'cache_max_age_in_seconds')
        self.cache_settings['refresh_cache'] = True if self.args.refresh_cache else config.getboolean('cache', 'refresh_cache')

    def _load_maas_settings(self, config):
        if not config.has_section('maas'):
            config.add_section('maas')

        self.group_machines_by = config.get('maas', 'group_machines_by')

    def _default_inventory(self) -> dict:
        return self.builder.build_default()

    def _group_machines_by_tag(self) -> dict:
        machines = self.fetcher.fetch_machines_grouped_by_tags()

        return self.builder.build_from_machines(machines)

    def _group_machines_by_hostname(self) -> dict:
        machines = self.fetcher.fetch_machines_grouped_by_hostname()

        return self.builder.build_from_machines(machines)

    def _get_machine_by_node(self, system_id: str) -> dict:
        machine = self.fetcher.fetch_machine_by_node(system_id)

        return self.builder.build_from_machine_node(machine)

    def _list(self):
        ''' Fetch and build the inventory '''

        if self.group_machines_by == "tags":
            self.inventory = self._group_machines_by_tag()
        elif self.group_machines_by == "hostnames":
            self.inventory = self._group_machines_by_hostname()

        return json.dumps(self.inventory, indent=4)

    def _host(self):
        ''' Fetch machine by host system id '''

        self.inventory = self._get_machine_by_node(self.args.host)
        return json.dumps(self.inventory, indent=4)


if __name__ == '__main__':
    Main()
