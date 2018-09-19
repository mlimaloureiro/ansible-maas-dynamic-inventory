[![Build Status](https://travis-ci.com/mlimaloureiro/ansible-maas-dynamic-inventory.svg?branch=master)](https://travis-ci.com/mlimaloureiro/ansible-maas-dynamic-inventory)
[![License](http://img.shields.io/:license-apache-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

# ansible-maas-inventory
A inventory generator script to work with Ubuntu [MAAS](https://maas.io/). It will generate your groups by looking
at either the tags (`maas_tags.py`) or hostname prefix (`maas_hostname.py`) you have in your MAAS nodes.

### Requirements

* Python3

### Example

By looking at the tests it's quite easy to understand how it works. Just look at the fixtures file `test_fixtures.py`.

Set environment variables for `MAAS_API_URL` and `MAAS_API_KEY`. After that you can run

```
   $ python maas_tags.py --list
```

and with ansible

```
    $ ansible -i maas_tags.py some-playbook.yml
```

### Output
```
{
    '_meta': {
        'hostvars': {
            'web-node1.dev': {
                'ansible_ssh_host': '127.0.0.1',
                'ansible_ssh_host_private': '127.0.0.1',
            },
            'web-node2.dev': {
                'ansible_ssh_host': '127.0.0.20',
                'ansible_ssh_host_private': '127.0.0.20',
            },
            'database1.dev': {
                'ansible_ssh_host': '192.168.0.1',
                'ansible_ssh_host_private': '192.168.0.1',
            },
            'database2.dev': {
                'ansible_ssh_host': '192.168.0.2',
                'ansible_ssh_host_private': '192.168.0.2',
            },
            'database3.dev': {
                'ansible_ssh_host': '192.168.0.4',
                'ansible_ssh_host_private': '192.168.0.4',
            },
        },
    },
    'web': {
        'hosts': [
            'web-node1.dev',
            'web-node2.dev',
        ],
        'vars': {},
    },
    'db': {
        'hosts': [
            'database1.dev',
            'database2.dev',
            'database3.dev',
        ],
        'vars': {},
    },
    'unnused_tag': {
        'hosts': [],
        'vars': {},
    },
}

