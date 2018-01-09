import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

FIREWALL_POLICY_ONE = {
    "firewall_policy": {
        "name": "test-policy",
        "firewall_rules": [
            "8722e0e0-9cc9-4490-9660-8c9a5732fbb0"
        ],
        "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
        "audited": False,
        "shared": False,
        "id": "c69933c1-b472-44f9-8226-30dc4ffd454c",
        "description": ""
    }
}

FIREWALL_POLICY_UPDATE = {
    "id": "c69933c1-b472-44f9-8226-30dc4ffd454c",
    "firewall_policy": {
        "firewall_policy": {
            "name": "test-policy",
            "firewall_rules": [
                "a08ef905-0ff6-4784-8374-175fffe7dade",
                "8722e0e0-9cc9-4490-9660-8c9a5732fbb0"
            ],
            "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
            "audited": False,
            "shared": False,
            "id": "c69933c1-b472-44f9-8226-30dc4ffd454c",
            "description": ""
        }
    }
}


def change_id(firewall_policy, count):
    id = firewall_policy['firewall_policy']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    firewall_policy['firewall_policy']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return firewall_policy


class FirewallPolicy(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_firewall_policy(self, firewall_policyid):
        logging.info('get firewall_policy: ' + firewall_policyid)
        return self.get(config.NEUTRON_FIREWALL_POLICIES + '/' + firewall_policyid)

    def get_firewall_policies(self):
        logging.info('get all firewall_policies')
        return self.get(config.NEUTRON_FIREWALL_POLICIES)

    def create_firewall_policy(self, payload):
        logging.info('create firewall_policy: ' + payload['firewall_policy']['id'])
        return self.post(config.NEUTRON_FIREWALL_POLICIES, payload)

    def update_firewall_policy(self, firewall_policyid, payload):
        logging.info('update firewall_policy: ' + firewall_policyid)
        return self.put(config.NEUTRON_FIREWALL_POLICIES + '/' + firewall_policyid, payload)

    def delete_firewall_policy(self, firewall_policyid):
        logging.info('delete firewall_policy: ' + firewall_policyid)
        return self.delete(config.NEUTRON_FIREWALL_POLICIES + '/' + firewall_policyid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform firewall_policy tests, server: %s, user: %s' % (servername, username))

        tester = FirewallPolicy(servername, username)

        utils.assert_status(tester.get_firewall_policies(), 200)

        firewall_policy_one = tester.create_firewall_policy(change_id(FIREWALL_POLICY_ONE, count))
        utils.assert_status(firewall_policy_one, 201)

        if firewall_policy_one.status_code == 201:
            firewall_policy_one_id = json.loads(firewall_policy_one.text)['firewall_policy']['id']
            utils.assert_status(tester.get_firewall_policy(firewall_policy_one_id), 200)

        utils.assert_status(tester.update_firewall_policy(
            change_id(FIREWALL_POLICY_UPDATE['firewall_policy'], count)['firewall_policy']['id'],
            change_id(FIREWALL_POLICY_UPDATE['firewall_policy'], count)), 201)

        utils.assert_status(tester.delete_firewall_policy(
            change_id(FIREWALL_POLICY_ONE, count)['firewall_policy']['id']), 204)

        utils.assert_status(tester.get_firewall_policy(
            change_id(FIREWALL_POLICY_ONE, count)['firewall_policy']['id']), 404)

if __name__ == '__main__':
    FirewallPolicy.perform_tests('server', 'admin')
