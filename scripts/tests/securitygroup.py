import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

SECURITY_GROUP_ONE = {
    "security_group": {
        "tenant_id": "1dfe7dffa0624ae882cdbda397d1d276",
        "description": "",
        "id": "521e29d6-67b8-4b3c-8633-027d21195333",
        "security_group_rules": [
            {
                "remote_group_id": None,
                "direction": "egress",
                "remote_ip_prefix": None,
                "protocol": None,
                "ethertype": "IPv4",
                "tenant_id": "1dfe7dffa0624ae882cdbda397d1d276",
                "port_range_max": None,
                "port_range_min": None,
                "id": "823faaf7-175d-4f01-a271-0bf56fb1e7e6",
                "security_group_id": "d3329053-bae5-4bf4-a2d1-7330f11ba5db"
            },
            {
                "remote_group_id": None,
                "direction": "egress",
                "remote_ip_prefix": None,
                "protocol": None,
                "ethertype": "IPv6",
                "tenant_id": "1dfe7dffa0624ae882cdbda397d1d276",
                "port_range_max": None,
                "port_range_min": None,
                "id": "d3329053-bae5-4bf4-a2d1-7330f11ba5db",
                "security_group_id": "d3329053-bae5-4bf4-a2d1-7330f11ba5db"
            }
        ],
        "name": "tempest-secgroup-1272206251"
    }
}
SECURITY_GROUP_UPDATE = {
    "id": "521e29d6-67b8-4b3c-8633-027d21195333",
    "security_group": {
        "tenant_id": "00f340c7c3b34ab7be1fc690c05a0275",
        "description": "tempest-security-description-897433715",
        "id": "521e29d6-67b8-4b3c-8633-027d21195333",
        "security_group_rules": [
            {
                "remote_group_id": None,
                "direction": "egress",
                "remote_ip_prefix": None,
                "protocol": None,
                "ethertype": "IPv4",
                "tenant_id": "00f340c7c3b34ab7be1fc690c05a0275",
                "port_range_max": None,
                "port_range_min": None,
                "id": "808bcefb-9917-4640-be68-14157bf33288",
                "security_group_id": "521e29d6-67b8-4b3c-8633-027d21195333"
            },
            {
                "remote_group_id": None,
                "direction": "egress",
                "remote_ip_prefix": None,
                "protocol": None,
                "ethertype": "IPv6",
                "tenant_id": "00f340c7c3b34ab7be1fc690c05a0275",
                "port_range_max": None,
                "port_range_min": None,
                "id": "c376f7b5-a281-40e0-a703-5c832c03aeb3",
                "security_group_id": "521e29d6-67b8-4b3c-8633-027d21195333"
            }
        ],
        "name": "tempest-security--1135434738"
    }
}


class Security_group(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_security_group(self, security_groupid):
        logging.info('get security_group: ' + security_groupid)
        return self.get(config.NEUTRON_SECURITY_GROUPS + '/' + security_groupid)

    def get_security_groups(self):
        logging.info('get all security_groups')
        return self.get(config.NEUTRON_SECURITY_GROUPS)

    def create_security_group(self, payload):
        logging.info('create security_group: ' + payload['security_group']['id'])
        return self.post(config.NEUTRON_SECURITY_GROUPS, payload)

    def update_security_group(self, security_groupid, payload):
        logging.info('update security_group: ' + security_groupid)
        return self.put(config.NEUTRON_SECURITY_GROUPS + '/' + security_groupid, payload)

    def delete_security_group(self, security_groupid):
        logging.info('delete security_group: ' + security_groupid)
        return self.delete(config.NEUTRON_SECURITY_GROUPS + '/' + security_groupid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform security_group tests, server: %s, user: %s' % (servername, username))

        tester = Security_group(servername, username)

        utils.assert_status(tester.get_security_groups(), 200)

        security_group_one = tester.create_security_group(SECURITY_GROUP_ONE)
        utils.assert_status(security_group_one, 201)

        security_group_one_id = json.loads(security_group_one.text)['security_group']['id']

        utils.assert_status(tester.get_security_group(security_group_one_id), 200)

        utils.assert_status(tester.update_security_group(SECURITY_GROUP_UPDATE['id'],
                                                         SECURITY_GROUP_UPDATE['security_group']), 200)

        utils.assert_status(tester.delete_security_group(security_group_one_id), 204)

        utils.assert_status(tester.get_security_group(security_group_one_id), 404)
