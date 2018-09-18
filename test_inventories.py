import unittest
from unittest.mock import MagicMock
from maas_tags import Fetcher as FetcherByTags
from maas_tags import InventoryBuilder as InventoryBuilderByTags
from maas_hostname import Fetcher as FetcherByHostname
from maas_hostname import InventoryBuilder as InventoryBuilderByHostname
import test_fixtures as fixtures


class TestInventoryBuilderMethods(unittest.TestCase):

    def setUp(self):
        self.fetcher_tags = FetcherByTags(None, None)
        self.inventory_builder_tags = InventoryBuilderByTags()
        self.fetcher_hostname = FetcherByHostname(None, None)
        self.inventory_builder_hostname = InventoryBuilderByHostname()

    def test_fetch_machines_grouped_by_tags(self):
        self.fetcher_tags._fetch_tags_summary = MagicMock(side_effect=fixtures.fetch_tags_summary)
        self.fetcher_tags._fetch_machines_by_tag = MagicMock(side_effect=fixtures.fetch_machines_by_tag)
        machines_by_tag = self.fetcher_tags.fetch_machines_grouped_by_tags()

        self.assertEqual(machines_by_tag, fixtures.test_fetch_machines_grouped_by_tags_result)

    def test_fetch_machines_grouped_by_hostname(self):
        self.fetcher_hostname._fetch_all_machines = MagicMock(side_effect=fixtures.fetch_all_machines)
        machines_by_hostname = self.fetcher_hostname.fetch_machines_grouped_by_hostname()

        self.assertEqual(machines_by_hostname, fixtures.test_fetch_machines_grouped_by_hostname_result)

    def test_build_from_tagged_machines(self):
        inventory = self.inventory_builder_tags.build_from_tagged_machines(
            fixtures.test_build_from_tagged_machines_input
        )

        self.assertEqual(inventory, fixtures.test_build_from_tagged_machines_result)

    def test_build_from_machines_hostname(self):
        inventory = self.inventory_builder_hostname.build_from_hostname_machines(
            fixtures.test_fetch_machines_grouped_by_hostname_result
        )

        self.assertEqual(inventory, fixtures.test_build_from_machines_hostname_result)


if __name__ == '__main__':
    unittest.main()
