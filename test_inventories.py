import unittest
from unittest.mock import MagicMock
from maas import Fetcher
from maas import InventoryBuilder
import test_fixtures as fixtures


class TestInventoryBuilderMethods(unittest.TestCase):

    def setUp(self):
        cache_settings = {
            'filename': 'ansible-maas-dynamics-inventory-test',
            'path': '~/.ansible/tmp',
            'max_age_in_seconds': 0,
            'refresh_cache': False
        }
        self.fetcher = Fetcher(None, None, cache_settings)
        self.inventory_builder = InventoryBuilder()

    def test_fetch_machines_grouped_by_tags(self):
        self.fetcher._fetch_tags_summary = MagicMock(side_effect=fixtures.fetch_tags_summary)
        self.fetcher._fetch_machines_by_tag = MagicMock(side_effect=fixtures.fetch_machines_by_tag)
        machines_by_tag = self.fetcher.fetch_machines_grouped_by_tags()

        self.assertEqual(machines_by_tag, fixtures.test_fetch_machines_grouped_by_tags_result)

    def test_fetch_machines_grouped_by_hostname(self):
        self.fetcher._fetch_all_machines = MagicMock(side_effect=fixtures.fetch_all_machines)
        machines_by_hostname = self.fetcher.fetch_machines_grouped_by_hostname()

        self.assertEqual(machines_by_hostname, fixtures.test_fetch_machines_grouped_by_hostname_result)

    def test_build_from_tagged_machines(self):
        inventory = self.inventory_builder.build_from_machines(
            fixtures.test_build_from_tagged_machines_input
        )

        self.assertEqual(inventory, fixtures.test_build_from_tagged_machines_result)

    def test_build_from_machines_hostname(self):
        inventory = self.inventory_builder.build_from_machines(
            fixtures.test_fetch_machines_grouped_by_hostname_result
        )

        self.assertEqual(inventory, fixtures.test_build_from_machines_hostname_result)


if __name__ == '__main__':
    unittest.main()
