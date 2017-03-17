PORTS = [
    {
        "port": {
            "status": "DOWN",
            "binding:host_id": "",
            "name": "private-port",
            "allowed_address_pairs": [],
            "admin_state_up": True,
            "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "binding:vif_details": {},
            "binding:vnic_type": "normal",
            "binding:vif_type": "unbound",
            "device_owner": "",
            "mac_address": "fa:16:3e:c9:cb:f0",
            "binding:profile": {},
            "port_security_enabled": True,
            "fixed_ips": [
                {
                    "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
                    "ip_address": "10.0.0.2"
                }
            ],
            "id": "65c0ee9f-d634-4522-8954-51021b570b0d",
            "security_groups": [],
            "device_id": ""
        }
    },
    {
        "port": {
            "binding:host_id": "",
            "name": "default-port",
            "allowed_address_pairs": [],
            "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "binding:vif_details": {},
            "binding:vnic_type": "normal",
            "binding:vif_type": "unbound",
            "device_owner": "",
            "mac_address": "fa:16:3e:c9:cb:f0",
            "binding:profile": {},
            "fixed_ips": [
                {
                    "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
                    "ip_address": "10.0.0.2"
                }
            ],
            "id": "d5c0ee9f-d634-d522-d954-d1021b570b0d",
            "security_groups": [],
            "device_id": ""
        }
    },
    {
        "ports": [
            {
                "status": "DOWN",
                "binding:host_id": "",
                "name": "",
                "allowed_address_pairs": [],
                "admin_state_up": True,
                "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
                "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
                "binding:vif_details": {},
                "binding:vnic_type": "normal",
                "binding:vif_type": "unbound",
                "device_owner": "network:router_gateway",
                "mac_address": "fa:16:3e:dc:1d:8d",
                "binding:profile": {},
                "fixed_ips": [
                    {
                        "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
                        "ip_address": "10.0.0.1"
                    }
                ],
                "id": "d8a4cc85-ad78-46ac-b5a1-8e04f16fa51e",
                "security_groups": [],
                "device_id": "8604a0de-7f6b-409a-a47c-a1cc7bc77b2e"
            },
            {
                "status": "DOWN",
                "binding:host_id": "",
                "name": "",
                "allowed_address_pairs": [],
                "admin_state_up": True,
                "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
                "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
                "binding:vif_details": {},
                "binding:vnic_type": "normal",
                "binding:vif_type": "unbound",
                "device_owner": "network:router_gateway",
                "mac_address": "fa:16:3e:dc:1d:8e",
                "binding:profile": {},
                "fixed_ips": [
                    {
                        "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
                        "ip_address": "10.0.0.2"
                    }
                ],
                "id": "d8a4cc85-ad78-46ac-b5a1-8e04f16fa51f",
                "security_groups": [],
                "device_id": "8604a0de-7f6b-409a-a47c-a1cc7bc77b2f"
            }
        ]
    },
    {
        "ports": [
            {
                "status": "DOWN",
                "name": "sample_port_1",
                "allowed_address_pairs": [],
                "admin_state_up": False,
                "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
                "tenant_id": "d6700c0c9ffa4f1cb322cd4a1f3906fa",
                "device_owner": "",
                "mac_address": "fa:16:3e:48:b8:9f",
                "fixed_ips": [
                    {
                        "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
                        "ip_address": "10.0.0.5"
                    }
                ],
                "id": "94225baa-9d3f-4b93-bf12-b41e7ce49cdb",
                "security_groups": [],
                "device_id": ""
            },
            {
                "status": "DOWN",
                "name": "sample_port_2",
                "allowed_address_pairs": [],
                "admin_state_up": False,
                "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
                "tenant_id": "d6700c0c9ffa4f1cb322cd4a1f3906fa",
                "device_owner": "",
                "mac_address": "fa:16:3e:f4:73:df",
                "port_security_enabled": False,
                "fixed_ips": [
                    {
                        "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
                        "ip_address": "10.0.0.6"
                    }
                ],
                "id": "43c831e0-19ce-4a76-9a49-57b57e69428b",
                "security_groups": [],
                "device_id": ""
            }
        ]
    },
    {
        "port": {
            "status": "DOWN",
            "binding:host_id": "00000000-1111-2222-3333-444444444444",
            "name": "test-for-port-update",
            "allowed_address_pairs": [
                {
                    "ip_address": "192.168.1.200/32",
                    "mac_address": "fa:16:3e:11:11:5e"
                }
            ],
            "admin_state_up": True,
            "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "tenant_id": "522eda8d23124b25bf03fe44f1986b74",
            "extra_dhcp_opts": [],
            "mac_address": "fa:16:3e:11:11:5e",
            "binding:vif_details": {},
            "binding:vif_type": "binding_failed",
            "device_owner": "compute:nova",
            "port_security_enabled": True,
            "binding:profile": {},
            "binding:vnic_type": "normal",
            "fixed_ips": [
                {
                    "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
                    "ip_address": "10.0.0.7"
                }
            ],
            "id": "43c831e0-19ce-4a76-9a49-57b57e69428b",
            "security_groups": [],
            "device_id": ""
        }
    }
]
