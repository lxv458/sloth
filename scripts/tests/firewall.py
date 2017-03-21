import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

FIREWALL_ONE = {
    "firewall": {
        "status": "PENDING_CREATE",
        "description": "",
        "admin_state_up": True,
        "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
        "firewall_policy_id": "c69933c1-b472-44f9-8226-30dc4ffd454c",
        "id": "3b0ef8f4-82c7-44d4-a4fb-6177f9a21977",
        "name": ""
    }
}

FIREWALL_UPDATE = {
    "id": "3b0ef8f4-82c7-44d4-a4fb-6177f9a21977",
    "firewall": {
        "status": "PENDING_CREATE",
        "description": "",
        "admin_state_up": False,
        "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
        "firewall_policy_id": "c69933c1-b472-44f9-8226-30dc4ffd454c",
        "id": "3b0ef8f4-82c7-44d4-a4fb-6177f9a21977",
        "name": ""
    }
}

class Firewall(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_firewall(self, firewallid):
        logging.info('get firewall: ' + firewallid)
        return self.get(config.NEUTRON_FIREWALLS + '/' + firewallid)

    def get_firewalls(self):
        logging.info('get all firewalls')
        return self.get(config.NEUTRON_FIREWALLS)

    def create_firewall(self, payload):
        logging.info('create firewall: ' + payload['firewall']['id'])
        return self.post(config.NEUTRON_FIREWALLS, payload)

    def update_firewall(self, firewallid, payload):
        logging.info('update firewall: ' + firewallid)
        return self.put(config.NEUTRON_FIREWALLS + '/' + firewallid, payload)

    def delete_firewall(self, firewallid):
        logging.info('delete firewall: ' + firewallid)
        return self.delete(config.NEUTRON_FIREWALLS + '/' + firewallid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform firewall tests, server: %s, user: %s' % (servername, username))

        tester = Firewall(servername, username)

        utils.assert_status(tester.get_firewalls(), 200)

        firewall_one = tester.create_firewall(FIREWALL_ONE)
        utils.assert_status(firewall_one, 201)

        firewall_one_id = json.loads(firewall_one.text)['firewall']['id']

        utils.assert_status(tester.get_firewall(firewall_one_id), 200)

        utils.assert_status(tester.update_firewall(FIREWALL_UPDATE['id'], FIREWALL_UPDATE['firewall']), 200)

        utils.assert_status(tester.delete_firewall(firewall_one_id), 204)

        utils.assert_status(tester.get_firewall(firewall_one_id), 404)
