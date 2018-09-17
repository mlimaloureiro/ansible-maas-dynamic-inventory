import unittest
from unittest.mock import MagicMock
from inventory import Fetcher
from inventory import InventoryBuilder
import test_mocks as mocks
import test_fixtures as fixtures

class TestInventoryBuilderMethods(unittest.TestCase):

    def setUp(self):
        self.inventory_fetcher = Fetcher(None, None)
        self.inventory_builder = InventoryBuilder()

    def test_fetch_machines_grouped_by_tags(self):
        self.inventory_fetcher._fetch_tags_summary = MagicMock(side_effect=mocks.fetch_tags_summary)
        self.inventory_fetcher._fetch_machines_by_tag = MagicMock(side_effect=mocks.fetch_machines_by_tag)
        machines_by_tag = self.inventory_fetcher.fetch_machines_grouped_by_tags()

        self.assertEqual(machines_by_tag,fixtures.test_fetch_machines_grouped_by_tags_output)

    def test_build_from_tagged_machines(self):
        inventory = self.inventory_builder.build_from_tagged_machines(
            fixtures.test_build_from_tagged_machines_input
        )

        self.assertEqual(inventory, fixtures.test_build_from_tagged_machines_result)


if __name__ == '__main__':
    unittest.main()
