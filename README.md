[![Build Status](https://travis-ci.com/mlimaloureiro/ansible-maas-dynamic-inventory.svg?branch=master)](https://travis-ci.com/mlimaloureiro/ansible-maas-dynamic-inventory)
[![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

# ansible-maas-inventory
A inventory generator script to work with Ubuntu [MAAS](https://maas.io/). It will generate your groups by looking
at the tags you have in your MAAS nodes.

### Requirements

* Python3

### Example

By looking at the tests it's quite easy to understand how it works. Just look at the fixtures file `test_fixtures.py`.

Set environment variables for `MAAS_API_URL` and `MAAS_API_KEY`. After that you can run

```
   $ python inventories.py
```

and with ansible

```
    $ ansible -i inventories.py some-playbook.yml
```

### TODO's

Wrap with proper CLI interface with `--list` and `--host` arguments