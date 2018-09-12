#!/usr/bin/env python

import click
import sys
import os
import json
from inventory import Authenticator
from inventory import Fetcher
from inventory import InventoryBuilder


@click.command()
@click.option('--list', 'list_flag', '-l', is_flag=True)
def cli(list_flag):
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


if __name__ == '__main__':
    cli()
