import unittest
from inventories import Authenticator
from inventories import Fetcher
from inventories import InventoryBuilder

class TestAuthenticatorMethods(unittest.TestCase):

    def setUp(self):
        self.authenticator = Authenticator()

    def test_hello(self):
        result = self.authenticator.hello('test')
        self.assertEqual(result, 'hello test')


class TestFetcherMethods(unittest.TestCase):

    def setUp(self):
        self.fetcher = Fetcher()

    def test_hello(self):
        result = self.fetcher.hello('test')
        self.assertEqual(result, 'hello test')


class TestInventoryBuilderMethods(unittest.TestCase):

    def setUp(self):
        self.inventory_builder = InventoryBuilder()

    def test_hello(self):
        print(self.inventory_builder)


if __name__ == '__main__':
    unittest.main()
