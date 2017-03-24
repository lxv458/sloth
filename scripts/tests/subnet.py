import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

SUBNET = {
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
}

SUBNET_EXTERNAL = {
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
}

SUBNETS_BULK = {
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
}

SUBNET_UPDATE = {
    "id": "b0e7435c-1512-45fb-aa9e-9a7c5932fb30",
    "subnet": {
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
}


class Subnet(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_subnet(self, subnetid):
        logging.info('get subnet: ' + subnetid)
        return self.get(config.NEUTRON_SUBNETS + '/' + subnetid)

    def get_subnets(self):
        logging.info('get all subnets')
        return self.get(config.NEUTRON_SUBNETS)

    def create_subnet(self, payload):
        if 'subnet' in payload:
            logging.info('create subnet: ' + payload['subnet']['id'])
        else:
            logging.info('bulk create subnets: ' + ', '.join([sub['id'] for sub in payload['subnets']]))
        return self.post(config.NEUTRON_SUBNETS, payload)

    def update_subnet(self, subnetid, payload):
        logging.info('update subnet: ' + subnetid)
        return self.put(config.NEUTRON_SUBNETS + '/' + subnetid, payload)

    def delete_subnet(self, subnetid):
        logging.info('delete subnet: ' + subnetid)
        return self.delete(config.NEUTRON_SUBNETS + '/' + subnetid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform subnet tests, server: %s, user: %s' % (servername, username))

        tester = Subnet(servername, username)

        utils.assert_status(tester.get_subnets(), 200)

        subnet = tester.create_subnet(SUBNET)
        utils.assert_status(subnet, 201)

        subnet_id = json.loads(subnet.text)['subnet']['id']

        utils.assert_status(tester.get_subnet(subnet_id), 200)

        utils.assert_status(tester.create_subnet(SUBNET_EXTERNAL), 201)

        utils.assert_status(tester.create_subnet(SUBNETS_BULK), 201)

        utils.assert_status(tester.update_subnet(SUBNET_UPDATE['id'], SUBNET_UPDATE['subnet']), 200)

        utils.assert_status(tester.delete_subnet(SUBNETS_BULK['subnets'][0]['id']), 204)

        utils.assert_status(tester.get_subnet(SUBNETS_BULK['subnets'][0]['id']), 404)

        subnets = tester.get_subnets()

        for sub in json.loads(subnets.text)['subnets']:
            utils.assert_status(tester.delete_subnet(sub['id']), 204)
