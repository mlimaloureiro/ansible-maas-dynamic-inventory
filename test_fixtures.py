import maas_status_enum

test_build_from_tagged_machines_input = {
    # key is the tag attached to maas node, value are the machines
    # containing that tag
    'ceph': [
        {
            'fqdn': 'ceph-node1.dev',
            'ip_addresses': ['127.0.0.1', '127.0.0.2'],
            'status_name': maas_status_enum.DEPLOYED,
        },
        {
            'fqdn': 'ceph-node2.dev',
            'ip_addresses': ['127.0.0.20', '127.0.0.30'],
            'status_name': maas_status_enum.DEPLOYED,
        },
    ],
    'kubernetes': [
        {
            'fqdn': 'kubernetes1.dev',
            'ip_addresses': ['192.168.0.1', '192.168.0.2'],
            'status_name': maas_status_enum.DEPLOYED,
        },
        {
            'fqdn': 'kubernetes2.dev',
            'ip_addresses': ['192.168.0.2', '192.168.0.3'],
            'status_name': maas_status_enum.DEPLOYED,
        },
        {
            'fqdn': 'kubernetes3.dev',
            'ip_addresses': ['192.168.0.4', '192.168.0.5'],
            'status_name': maas_status_enum.DEPLOYED,
        },
        {
            'fqdn': 'kubernetes4.dev',
            'ip_addresses': ['192.168.0.4', '192.168.0.5'],
            'status_name': 'not-deployed',
        },
    ],
    'unnused_tag': [],
}

test_build_from_tagged_machines_result = {
    # inventories dict
    '_meta': {
        'hostvars': {
            'ceph-node1.dev': {
                'ansible_ssh_host': '127.0.0.1',
                'ansible_ssh_host_private': '127.0.0.1',
            },
            'ceph-node2.dev': {
                'ansible_ssh_host': '127.0.0.20',
                'ansible_ssh_host_private': '127.0.0.20',
            },
            'kubernetes1.dev': {
                'ansible_ssh_host': '192.168.0.1',
                'ansible_ssh_host_private': '192.168.0.1',
            },
            'kubernetes2.dev': {
                'ansible_ssh_host': '192.168.0.2',
                'ansible_ssh_host_private': '192.168.0.2',
            },
            'kubernetes3.dev': {
                'ansible_ssh_host': '192.168.0.4',
                'ansible_ssh_host_private': '192.168.0.4',
            },
        },
    },
    'ceph': {
        'hosts': [
            'ceph-node1.dev',
            'ceph-node2.dev',
        ],
        'vars': {},
    },
    'kubernetes': {
        'hosts': [
            'kubernetes1.dev',
            'kubernetes2.dev',
            'kubernetes3.dev',
        ],
        'vars': {},
    },
    'unnused_tag': {
        'hosts': [],
        'vars': {},
    },
}
