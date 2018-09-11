class Authenticator:
    """ Class used to authenticate requests and build request headers """

    def hello(self, name: str) -> str:
        return "hello {}".format(name)


class Fetcher:
    """ Class used to fetch nodes data from MAAS """

    def hello(self, name: str) -> str:
        return "hello {}".format(name)


class InventoryBuilder:
    """ Class used to build the inventory """

    def __init__(self, authenticator: Authenticator, fetcher: Fetcher):
        self.authenticator = authenticator
        self.fetcher = fetcher


if __name__ == '__main__':
    Authenticator()
    Fetcher()
    InventoryBuilder()
