LOAD_BALANCER_HEALTH_MONITORS = [
    {
        "healthmonitor": {
            "admin_state_up": True,
            "delay": 1,
            "expected_codes": "200,201,202",
            "http_method": "GET",
            "id": "0a9ac99d-0a09-4b18-8499-a0796850279a",
            "max_retries": 5,
            "pools": [
                {
                    "id": "74aa2010-a59f-4d35-a436-60a6da882819"
                }
            ],
            "tenant_id": "6f3584d5754048a18e30685362b88411",
            "timeout": 1,
            "type": "HTTP",
            "url_path": "/index.html"
        }
    },
    {
        "healthmonitor": {
            "admin_state_up": False,
            "delay": 2,
            "expected_codes": "200",
            "http_method": "POST",
            "id": "0a9ac99d-0a09-4b18-8499-a0796850279a",
            "max_retries": 2,
            "pools": [
                {
                    "id": "74aa2010-a59f-4d35-a436-60a6da882819"
                }
            ],
            "tenant_id": "6f3584d5754048a18e30685362b88411",
            "timeout": 2,
            "type": "HTTP",
            "url_path": "/page.html"
        }
    }
]
