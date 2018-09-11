"""
MAAS dynamic inventory generator script.

Usage:
  inventories.py (-h | --help)
  inventories.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
import requests


if __name__ == '__main__':
    arguments = docopt(__doc__, version='MAAS dynamic inventory 0.1')
    print(arguments)
