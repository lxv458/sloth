TRUNKS = [
    {
        "trunk":{
            "status":"DOWN",
            "name": "trunk0",
            "admin_state_up":True,
            "tenant_id":"cc3641789c8a4304abaa841c64f638d9",
            "port_id":"60aac28d-1d3a-48d9-99bc-dd4bd62e50f2",
            "sub_ports":[
                {
                    "segmentation_type": "vlan",
                    "port_id": "dca33436-2a7c-415b-aa35-14769e7834e3",
                    "segmentation_id":101
                },
                {
                    "segmentation_type": "vlan",
                    "port_id": "be28febe-bdff-45cc-8a2d-872d54e62527",
                    "segmentation_id":102
                }
            ],
            "id": "c935240e-4aa6-496a-841c-d113c54499b9",
            "description": "test trunk0"
        }
    },
    {
        "trunk":{
            "name": "trunkdefault",
            "tenant_id": "cc3641789c8a4304abaa841c64f638d9",
            "port_id": "60aac28d-1d3a-48d9-99bc-dd4bd62e50f2",
            "sub_ports":[
                {
                    "segmentation_type": "vlan",
                    "port_id": "dca33436-2a7c-415b-aa35-14769e7834e3",
                    "segmentation_id":101
                },
                {
                    "segmentation_type": "vlan",
                    "port_id": "be28febe-bdff-45cc-8a2d-872d54e62527",
                    "segmentation_id":102
                }
            ],
            "id": "d935240e-4aa6-d96a-d41c-d113c54499b9",
            "description": "test trunkdefault"
        }
    },
    {
        "trunk":{
            "status": "DOWN",
            "name": "trunk0",
            "admin_state_up":True,
            "port_id": "60aac28d-1d3a-48d9-99bc-dd4bd62e50f2",
            "sub_ports":[
                {
                    "segmentation_type": "vlan",
                    "port_id": "dca33436-2a7c-415b-aa35-14769e7834e3",
                    "segmentation_id":101
                }
            ],
            "id": "c935240e-4aa6-496a-841c-d113c54499b9",
            "description": "test trunk0 updated"
        }
    }
]