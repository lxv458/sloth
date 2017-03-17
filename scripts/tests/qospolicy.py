QOS_POLICIES = [
    {
        "policy": {
            "shared": False,
            "tenant_id": "aa902936679e4ea29bfe1158e3450a13",
            "id": "d6220bbb-35f3-48ab-8eae-69c60aef3546",
            "name": "jaxb-test"
        }
    },
    {
        "policy": {
            "bandwidth_limit_rules": [
                {
                    "tenant_id": "aa902936679e4ea29bfe1158e3450a14",
                    "id": "d6220bbb-35f3-48ab-8eae-69c60aef3547",
                    "max_burst_kbps": 100,
                    "max_kbps": 25
                }
            ],
            "name": "jaxb-test",
            "tenant_id": "aa902936679e4ea29bfe1158e3450a13",
            "dscp_marking_rules": [
                {
                    "tenant_id": "aa902936679e4ea29bfe1158e3450a14",
                    "dscp_mark": 8,
                    "id": "d6220bbb-35f3-48ab-8eae-69c60aef3547"
                }
            ],
            "shared": False,
            "id": "d6220bbb-35f3-48ab-8eae-69c60aef3546"
        }
    }
]
