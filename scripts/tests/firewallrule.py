import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

FIREWALL_RULE_ONE = {
    "firewall_rule": {
        "source_port_max": None,
        "protocol": "tcp",
        "name": "ALLOW_HTTP",
        "source_ip_address": None,
        "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
        "enabled": True,
        "destination_port_max": "80",
        "source_port_min": None,
        "destination_port_min": "80",
        "ip_version": 4,
        "destination_ip_address": None,
        "firewall_policy_id": None,
        "shared": False,
        "action": "allow",
        "position": None,
        "id": "8722e0e0-9cc9-4490-9660-8c9a5732fbb0"
    }
}

FIREWALL_RULE_UPDATE = {
    "id": "8722e0e0-9cc9-4490-9660-8c9a5732fbb0",
    "firewall_rule": {
        "firewall_rule": {
            "source_port_max": None,
            "protocol": "tcp",
            "name": "ALLOW_HTTP",
            "source_ip_address": None,
            "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
            "enabled": True,
            "destination_port_max": "80",
            "source_port_min": None,
            "destination_port_min": "80",
            "ip_version": 4,
            "destination_ip_address": None,
            "firewall_policy_id": None,
            "shared": True,
            "action": "allow",
            "position": None,
            "id": "8722e0e0-9cc9-4490-9660-8c9a5732fbb0"
        }
    }
}


def change_id(firewall_rule, count):
    id = firewall_rule['firewall_rule']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    firewall_rule['firewall_rule']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return firewall_rule


class FirewallRule(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_firewall_rule(self, firewall_ruleid):
        logging.info('get firewall_rule: ' + firewall_ruleid)
        return self.get(config.NEUTRON_FIREWALL_RULES + '/' + firewall_ruleid)

    def get_firewall_rules(self):
        logging.info('get all firewall_rules')
        return self.get(config.NEUTRON_FIREWALL_RULES)

    def create_firewall_rule(self, payload):
        logging.info('create firewall_rule: ' + payload['firewall_rule']['id'])
        return self.post(config.NEUTRON_FIREWALL_RULES, payload)

    def update_firewall_rule(self, firewall_ruleid, payload):
        logging.info('update firewall_rule: ' + firewall_ruleid)
        return self.put(config.NEUTRON_FIREWALL_RULES + '/' + firewall_ruleid, payload)

    def delete_firewall_rule(self, firewall_ruleid):
        logging.info('delete firewall_rule: ' + firewall_ruleid)
        return self.delete(config.NEUTRON_FIREWALL_RULES + '/' + firewall_ruleid)

    @staticmethod
    def perform_tests(servername, username, count):
        logging.info('perform firewall_rule tests, server: %s, user: %s' % (servername, username))

        tester = FirewallRule(servername, username)

        utils.assert_status(tester.get_firewall_rules(), 200)

        firewall_rule_one = tester.create_firewall_rule(change_id(FIREWALL_RULE_ONE, count))
        utils.assert_status(firewall_rule_one, 201)

        firewall_rule_one_id = json.loads(firewall_rule_one.text)['firewall_rule']['id']

        utils.assert_status(tester.get_firewall_rule(firewall_rule_one_id), 200)

        utils.assert_status(tester.update_firewall_rule(
            change_id(FIREWALL_RULE_UPDATE['firewall_rule'], count)['firewall_rule']['id'],
            change_id(FIREWALL_RULE_UPDATE['firewall_rule'], count)), 200)

        utils.assert_status(tester.delete_firewall_rule(firewall_rule_one_id), 204)

        utils.assert_status(tester.get_firewall_rule(firewall_rule_one_id), 404)

if __name__ == '__main__':
    FirewallRule.perform_tests('server', 'admin', 0)
