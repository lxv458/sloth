SUBNETS = [
    {
        "subnet": {
            "name": "",
            "enable_dhcp": True,
            "network_id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "dns_nameservers": [
                "8.8.8.8"
            ],
            "allocation_pools": [
                {
                    "start": "10.0.0.2",
                    "end": "10.0.0.254"
                }
            ],
            "host_routes": [
                {
                    "nexthop": "10.0.0.1",
                    "destination": "0.0.0.0/0"
                },
                {
                    "nexthop": "10.0.0.2",
                    "destination": "192.168.0.0/24"
                }
            ],
            "ip_version": 4,
            "gateway_ip": "10.0.0.1",
            "cidr": "10.0.0.0/24",
            "id": "3b80198d-4f7b-4f77-9ef5-774d54e17126"
        }
    },
    {
        "subnet": {
            "name": "",
            "enable_dhcp": True,
            "network_id": "8ca37218-28ff-41cb-9b10-039601ea7e6b",
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "dns_nameservers": [],
            "allocation_pools": [
                {
                    "start": "10.1.0.2",
                    "end": "10.1.0.254"
                }
            ],
            "host_routes": [],
            "ip_version": 4,
            "gateway_ip": "10.1.0.1",
            "cidr": "10.1.0.0/24",
            "id": "f13b537f-1268-455f-b5fa-1e6817a9c204"
        }
    },
    {
        "subnets": [
            {
                "name": "",
                "enable_dhcp": True,
                "network_id": "af374017-c9ae-4a1d-b799-ab73111476e2",
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
                "dns_nameservers": [
                    "8.8.8.8"
                ],
                "allocation_pools": [
                    {
                        "start": "192.168.199.2",
                        "end": "192.168.199.254"
                    }
                ],
                "host_routes": [
                    {
                        "nexthop": "192.168.199.3",
                        "destination": "0.0.0.0/0"
                    },
                    {
                        "nexthop": "192.168.199.4",
                        "destination": "192.168.0.0/24"
                    }
                ],
                "ip_version": 4,
                "gateway_ip": "192.168.199.1",
                "cidr": "192.168.199.0/24",
                "id": "0468a7a7-290d-4127-aedd-6c9449775a24"
            },
            {
                "name": "",
                "enable_dhcp": True,
                "network_id": "af374017-c9ae-4a1d-b799-ab73111476e2",
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
                "dns_nameservers": [
                    "8.8.8.8",
                    "8.8.8.4"
                ],
                "allocation_pools": [
                    {
                        "start": "10.56.4.2",
                        "end": "10.56.7.254"
                    }
                ],
                "host_routes": [
                    {
                        "nexthop": "10.56.4.3",
                        "destination": "0.0.0.0/0"
                    },
                    {
                        "nexthop": "10.56.4.4",
                        "destination": "192.168.0.0/24"
                    }
                ],
                "ip_version": 4,
                "gateway_ip": "10.56.4.1",
                "cidr": "10.56.4.0/22",
                "id": "b0e7435c-1512-45fb-aa9e-9a7c5932fb30"
            }
        ]
    },
    {
        "subnet": {
            "name": "my_subnet",
            "enable_dhcp": True,
            "network_id": "af374017-c9ae-4a1d-b799-ab73111476e2",
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
            "dns_nameservers": [
                "8.8.8.8",
                "8.8.8.4"
            ],
            "allocation_pools": [
                {
                    "start": "10.0.0.2",
                    "end": "10.0.0.254"
                }
            ],
            "host_routes": [
                {
                    "nexthop": "10.0.0.11",
                    "destination": "192.168.0.0/24"
                }
            ],
            "ip_version": 4,
            "gateway_ip": "10.0.0.1",
            "cidr": "10.0.0.0/24",
            "id": "b0e7435c-1512-45fb-aa9e-9a7c5932fb30"
        }
    }
]
