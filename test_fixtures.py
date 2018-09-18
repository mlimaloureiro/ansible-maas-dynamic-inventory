from maas import MaasStatusEnum


def fetch_tags_summary() -> dict:
    return test_fetch_machines_grouped_by_tags_tags


def fetch_machines_by_tag(tag_name: str) -> dict:
    return test_fetch_machines_grouped_by_tags_machines[tag_name]

def fetch_machines_all() -> dict:
    return test_fetch_machines_grouped_by_hostname_machines


test_fetch_machines_grouped_by_tags_tags = [
    {
        'name': 'ceph',
    },
    {
        'name': 'kubernets',
    },
    {
        'name': 'empty-tag',
    },
]

test_fetch_machines_grouped_by_tags_machines = {
    'ceph': [
        {
            "fqdn": "ceph-node1.dev",
            "hostname": "ceph-node1",
            "osystem": "ubuntu",
            "tag_names": ["ceph"],
            "system_id": "ff3aqd",
            "resource_uri": "/MAAS/api/2.0/machines/ff3aqd/",
        },
        {
            "fqdn": "ceph-node2.dev",
            "hostname": "ceph-node2",
            "osystem": "ubuntu",
            "tag_names": ["ceph"],
            "system_id": "ff3aqe",
            "resource_uri": "/MAAS/api/2.0/machines/ff3aqe/",
        },
    ],
    'kubernets': [
        {
            "fqdn": "kubernetes1.dev",
            "hostname": "kubernetes1",
            "osystem": "ubuntu",
            "tag_names": ["kubernets"],
            "system_id": "ff4aqd",
            "resource_uri": "/MAAS/api/2.0/machines/ff4aqd/",
        },
        {
            "fqdn": "kubernetes2.dev",
            "hostname": "kubernetes2",
            "osystem": "ubuntu",
            "tag_names": ["kubernets"],
            "system_id": "ff4aqe",
            "resource_uri": "/MAAS/api/2.0/machines/ff4aqe/",
        },
        {
            "fqdn": "kubernetes3.dev",
            "hostname": "kubernetes3",
            "osystem": "ubuntu",
            "tag_names": ["kubernets"],
            "system_id": "ff4aqf",
            "resource_uri": "/MAAS/api/2.0/machines/ff4aqf/",
        },
        {
            "fqdn": "kubernetes4.dev",
            "hostname": "kubernetes4",
            "osystem": "ubuntu",
            "tag_names": ["kubernets"],
            "system_id": "ff4aqg",
            "resource_uri": "/MAAS/api/2.0/machines/ff4aqg/",
        },
    ],
    'empty-tag': [],
}

test_fetch_machines_grouped_by_tags_result = {
  'ceph': [
    {
      'fqdn': 'ceph-node1.dev',
      'hostname': 'ceph-node1',
      'osystem': 'ubuntu',
      'tag_names': ['ceph'],
      'system_id': 'ff3aqd',
      'resource_uri': '/MAAS/api/2.0/machines/ff3aqd/',
    },
    {
      'fqdn': 'ceph-node2.dev',
      'hostname': 'ceph-node2',
      'osystem': 'ubuntu',
      'tag_names': ['ceph'],
      'system_id': 'ff3aqe',
      'resource_uri': '/MAAS/api/2.0/machines/ff3aqe/',
    }
  ],
  'kubernets': [
    {
      'fqdn': 'kubernetes1.dev',
      'hostname': 'kubernetes1',
      'osystem': 'ubuntu',
      'tag_names': ['kubernets'],
      'system_id': 'ff4aqd',
      'resource_uri': '/MAAS/api/2.0/machines/ff4aqd/',
    },
    {
      'fqdn': 'kubernetes2.dev',
      'hostname': 'kubernetes2',
      'osystem': 'ubuntu',
      'tag_names': ['kubernets'],
      'system_id': 'ff4aqe',
      'resource_uri': '/MAAS/api/2.0/machines/ff4aqe/',
    },
    {
      'fqdn': 'kubernetes3.dev',
      'hostname': 'kubernetes3',
      'osystem': 'ubuntu',
      'tag_names': ['kubernets'],
      'system_id': 'ff4aqf',
      'resource_uri': '/MAAS/api/2.0/machines/ff4aqf/',
    },
    {
      'fqdn': 'kubernetes4.dev',
      'hostname': 'kubernetes4',
      'osystem': 'ubuntu',
      'tag_names': ['kubernets'],
      'system_id': 'ff4aqg',
      'resource_uri': '/MAAS/api/2.0/machines/ff4aqg/',
    }
  ],
  'empty-tag': [],
}

test_fetch_machines_grouped_by_hostname_machines = [
    # List of machines provided by the get all machines API
    {
        "ip_addresses": ["172.16.1.63"],
        "hostname": "joint-1",
        "fqdn": "joint-1.maas",
        "status_name": "Deployed",
    },
    {
        "ip_addresses": ["172.16.1.66"],
        "hostname": "gentle-mole",
        "fqdn": "gentle-mole.maas",
        "status_name": "Deployed",
    },
    {
        "ip_addresses": ["172.16.1.64"],
        "hostname": "key-chimp",
        "fqdn": "key-chimp.maas",
        "status_name": "Deployed",
    },
    {
        "ip_addresses": ["172.16.1.62"],
        "hostname": "joint-2",
        "fqdn": "loyal-2.maas",
        "status_name": "Deployed",
    },
]

test_fetch_machines_grouped_by_hostname_result = {
    # key is the hostname prefix attached to maas node, value are the machines
    # containing that hostname prefix
    'joint': [
        {
            'ip_addresses': ['172.16.1.63'],
            'hostname': 'joint-1',
            'fqdn': 'joint-1.maas',
            'status_name': 'Deployed',
        },
        {
            'ip_addresses': ['172.16.1.62'],
            'hostname': 'joint-2',
            'fqdn': 'loyal-2.maas',
            'status_name': 'Deployed',
        }
    ],
    'gentle': [
        {
            'ip_addresses': ['172.16.1.66'],
            'hostname': 'gentle-mole',
            'fqdn': 'gentle-mole.maas',
            'status_name': 'Deployed',
        }
    ],
    'key': [
        {
            'ip_addresses': ['172.16.1.64'],
            'hostname': 'key-chimp',
            'fqdn': 'key-chimp.maas',
            'status_name': 'Deployed',
        }
    ]
}

test_build_from_tagged_machines_input = {
    # key is the tag attached to maas node, value are the machines
    # containing that tag
    'ceph': [
        {
            'fqdn': 'ceph-node1.dev',
            'ip_addresses': ['127.0.0.1', '127.0.0.2'],
            'status_name': MaasStatusEnum.DEPLOYED,
        },
        {
            'fqdn': 'ceph-node2.dev',
            'ip_addresses': ['127.0.0.20', '127.0.0.30'],
            'status_name': MaasStatusEnum.DEPLOYED,
        },
    ],
    'kubernetes': [
        {
            'fqdn': 'kubernetes1.dev',
            'ip_addresses': ['192.168.0.1', '192.168.0.2'],
            'status_name': MaasStatusEnum.DEPLOYED,
        },
        {
            'fqdn': 'kubernetes2.dev',
            'ip_addresses': ['192.168.0.2', '192.168.0.3'],
            'status_name': MaasStatusEnum.DEPLOYED,
        },
        {
            'fqdn': 'kubernetes3.dev',
            'ip_addresses': ['192.168.0.4', '192.168.0.5'],
            'status_name': MaasStatusEnum.DEPLOYED,
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
