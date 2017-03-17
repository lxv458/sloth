LOAD_BALANCER_LISTENERS = [
    {
        "listener": {
            "admin_state_up": True,
            "connection_limit": 100,
            "default_pool_id": None,
            "description": "listener one",
            "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829",
            "loadbalancers": [
                {
                    "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c"
                }
            ],
            "name": "listener1",
            "protocol": "HTTP",
            "protocol_port": 80,
            "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081"
        }
    },
    {
        "listener": {
            "admin_state_up": False,
            "connection_limit": 200,
            "default_pool_id": None,
            "description": "listener two",
            "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829",
            "loadbalancers": [
                {
                    "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c"
                }
            ],
            "name": "listener2",
            "protocol": "HTTP",
            "protocol_port": 80,
            "tenant_id": "1a3e005cf9ce40308c900bcb08e5320c"
        }
    },
    {
        "listener": {
            "admin_state_up": True,
            "connection_limit": 100,
            "default_pool_id": None,
            "description": "listener one",
            "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829",
            "loadbalancers": [
                {
                    "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c"
                }
            ],
            "name": "listener1",
            "protocol": "http",
            "protocol_port": 80,
            "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081"
        }
    }
]
