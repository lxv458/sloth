import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

PORT_ONE = {
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
}

PORT_DEFAULT = {
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
}

ROUTER_INTERFACE_PORT = {
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
}

PORTS_BULK = {
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
}

PORT_UPDATE = {
    "id": "43c831e0-19ce-4a76-9a49-57b57e69428b",
    "port": {
        "port": {
            "status": "DOWN",
            "binding:host_id": "",
            "name": "private-port-update",
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
    }
}


def change_id(port, count):
    id = port['port']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    port['port']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return port


class Port(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_port(self, portid):
        logging.info('get port: ' + portid)
        return self.get(config.NEUTRON_PORTS + '/' + portid)

    def get_ports(self):
        logging.info('get all ports')
        return self.get(config.NEUTRON_PORTS)

    def create_port(self, payload):
        if 'port' in payload:
            logging.info('create port: ' + payload['port']['id'])
        else:
            logging.info('bulk create ports: ' + ', '.join([port['id'] for port in payload['ports']]))
        return self.post(config.NEUTRON_PORTS, payload)

    def update_port(self, portid, payload):
        logging.info('update port: ' + portid)
        return self.put(config.NEUTRON_PORTS + '/' + portid, payload)

    def delete_port(self, portid):
        logging.info('delete port: ' + portid)
        return self.delete(config.NEUTRON_PORTS + '/' + portid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform port tests, server: %s, user: %s' % (servername, username))

        tester = Port(servername, username)

        utils.assert_status(tester.get_ports(), 200)

        port_one = tester.create_port(change_id(PORT_ONE, count))
        utils.assert_status(port_one, 201)

        if port_one.status_code == 201:
            port_one_id = json.loads(port_one.text)['port']['id']
            utils.assert_status(tester.get_port(port_one_id), 200)

        utils.assert_status(tester.create_port(change_id(PORT_DEFAULT, count)), 201)

        if count == 0:
            utils.assert_status(tester.create_port(ROUTER_INTERFACE_PORT), 201)
            utils.assert_status(tester.create_port(PORTS_BULK), 201)
            utils.assert_status(tester.delete_port(PORTS_BULK['ports'][0]['id']), 204)
            utils.assert_status(tester.get_port(PORTS_BULK['ports'][0]['id']), 404)

        utils.assert_status(tester.update_port(change_id(PORT_UPDATE['port'], count)['port']['id'],
                                               change_id(PORT_UPDATE['port'], count)), 201)

        ports = tester.get_ports()

        if 'status code: 401' in ports.text:
            utils.assert_status(tester.delete_port('0000'), 204)
            return

        for port in json.loads(ports.text)['ports']:
            utils.assert_status(tester.delete_port(port['id']), 204)


if __name__ == '__main__':
    Port.perform_tests('server', 'admin')
