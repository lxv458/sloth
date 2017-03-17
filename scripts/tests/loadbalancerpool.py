LOAD_BALANCER_POOLS = [
    {
        "pool": {
            "admin_state_up": True,
            "description": "simple pool",
            "healthmonitor_id": None,
            "id": "12ff63af-4127-4074-a251-bcb2ecc53ebe",
            "lb_algorithm": "ROUND_ROBIN",
            "listeners": [
                {
                    "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829"
                }
            ],
            "members": [],
            "name": "pool1",
            "protocol": "HTTP",
            "session_persistence": {
                "cookie_name": "my_cookie",
                "type": "APP_COOKIE"
            },
            "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081"
        }
    },
    {
        "pool": {
            "admin_state_up": False,
            "description": "pool two",
            "healthmonitor_id": None,
            "id": "12ff63af-4127-4074-a251-bcb2ecc53ebe",
            "lb_algorithm": "LEAST_CONNECTIONS",
            "listeners": [
                {
                    "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829"
                }
            ],
            "members": [],
            "name": "pool2",
            "protocol": "HTTP",
            "session_persistence": {
                "cookie_name": None,
                "type": "HTTP_COOKIE"
            },
            "tenant_id": "1a3e005cf9ce40308c900bcb08e5320c"
        }
    }
]
