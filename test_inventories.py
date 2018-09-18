import unittest
from unittest.mock import MagicMock
from maas_tags import Fetcher as FetcherT
from maas_tags import InventoryBuilder as InventoryBuilderT
from maas_hostname import Fetcher as FetcherH
from maas_hostname import InventoryBuilder as InventoryBuilderH
import test_fixtures as fixtures


class TestInventoryBuilderMethods(unittest.TestCase):

    def setUp(self):
        self.fetcherTags = FetcherT(None, None)
        self.inventory_builderTags = InventoryBuilderT()
        self.fetcherHostname = FetcherH(None, None)
        self.inventory_builderHostname = InventoryBuilderH()

    def test_fetch_machines_grouped_by_tags(self):
        self.fetcherTags._fetch_tags_summary = MagicMock(side_effect=fixtures.fetch_tags_summary)
        self.fetcherTags._fetch_machines_by_tag = MagicMock(side_effect=fixtures.fetch_machines_by_tag)
        machines_by_tag = self.fetcherTags.fetch_machines_grouped_by_tags()

        self.assertEqual(machines_by_tag, fixtures.test_fetch_machines_grouped_by_tags_result)

    def test_fetch_machines_grouped_by_hostname(self):
        self.fetcherHostname._fetch_machines_all = MagicMock(side_effect=fixtures.fetch_machines_all)
        machines_by_hostname = self.fetcherHostname.fetch_machines_grouped_by_hostname()

        self.assertEqual(machines_by_hostname, fixtures.test_fetch_machines_grouped_by_hostname_result)

    def test_build_from_tagged_machines(self):
        inventory = self.inventory_builderTags.build_from_tagged_machines(
            fixtures.test_build_from_tagged_machines_input
        )

        self.assertEqual(inventory, fixtures.test_build_from_tagged_machines_result)

    def test_build_from_machines_hostname(self):
        inventory = self.inventory_builderHostname.build_from_hostname_machines(
            fixtures.test_fetch_machines_grouped_by_hostname_result
        )

        self.assertEqual(inventory, fixtures.test_build_from_machines_hostname_result)


if __name__ == '__main__':
    unittest.main()
