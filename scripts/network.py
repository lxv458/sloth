NETWORKS = [
    {
        "network": {
            "status": "ACTIVE",
            "subnets": [],
            "name": "net1",
            "router:external": False,
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "segments": [
                {
                    "provider:network_type": "vlan",
                    "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                    "provider:segmentation_id": 2
                },
                {
                    "provider:network_type": "stt",
                    "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                    "provider:segmentation_id": None
                }
            ],
            "admin_state_up": True,
            "shared": False,
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
        }
    },
    {
        "network": {
            "subnets": [],
            "name": "netdefault",
            "router:external": False,
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "segments": [
                {
                    "provider:network_type": "vlan",
                    "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                    "provider:segmentation_id": 2
                },
                {
                    "provider:network_type": "stt",
                    "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                    "provider:segmentation_id": None
                }
            ],
            "id": "de8e5957-d49f-d77b-de5b-d1f75b21c03c"
        }
    },
    {
        "network": {
            "status": "ACTIVE",
            "subnets": [],
            "name": "external1",
            "router:external": True,
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "admin_state_up": True,
            "shared": False,
            "id": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
        }
    },
    {
        "networks": [
            {
                "status": "ACTIVE",
                "subnets": [],
                "name": "sample_network3",
                "provider:physical_network": None,
                "admin_state_up": True,
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
                "provider:network_type": "local",
                "shared": False,
                "id": "bc1a76cb-8767-4c3a-bb95-018b822f2130",
                "provider:segmentation_id": None
            },
            {
                "status": "ACTIVE",
                "subnets": [],
                "name": "sample_network4",
                "provider:physical_network": None,
                "admin_state_up": True,
                "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
                "provider:network_type": "local",
                "shared": False,
                "id": "af374017-c9ae-4a1d-b799-ab73111476e2",
                "provider:segmentation_id": None
            }
        ]
    },
    {
        "network": {
            "status": "ACTIVE",
            "subnets": [],
            "name": "sample_network_5_updated",
            "provider:physical_network": None,
            "admin_state_up": True,
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
            "provider:network_type": "local",
            "router:external": False,
            "shared": False,
            "provider:segmentation_id": None
        }
    }
]


