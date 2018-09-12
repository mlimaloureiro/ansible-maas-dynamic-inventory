import unittest
from inventory import InventoryBuilder
import test_fixtures as fixtures


class TestInventoryBuilderMethods(unittest.TestCase):

    def setUp(self):
        self.inventory_builder = InventoryBuilder()

    def test_build_from_tagged_machines(self):
        inventory = self.inventory_builder.build_from_tagged_machines(
            fixtures.test_build_from_tagged_machines_input
        )

        self.assertEqual(inventory, fixtures.test_build_from_tagged_machines_result)


if __name__ == '__main__':
    unittest.main()
