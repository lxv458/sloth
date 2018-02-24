import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

SECURITY_GROUP_RULE_ONE = {
    "security_group_rule": {
        "remote_group_id": None,
        "direction": "ingress",
        "remote_ip_prefix": None,
        "protocol": "tcp",
        "ethertype": "IPv6",
        "tenant_id": "00f340c7c3b34ab7be1fc690c05a0275",
        "port_range_max": 77,
        "port_range_min": 77,
        "id": "9b4be7fa-e56e-40fb-9516-1f0fa9185669",
        "security_group_id": "b60490fe-60a5-40be-af63-1d641381b784"
    }
}

SECURITY_GROUP_RULES_BULK = {
    "security_group_rules": [
        {
            "id": "35fb0f34-c8d3-416d-a205-a2c75f7b8e22",
            "direction": "egress",
            "ethertype": "IPv6",
            "protocol": "tcp",
            "security_group_id": "70f1b157-e79b-44dc-85a8-7de0fc9f2aab",
            "tenant_id": "2640ee2ac2474bf3906e482047204fcb"
        },
        {
            "id": "63814eed-bc12-4fe4-8b17-2af178224c71",
            "direction": "egress",
            "ethertype": "IPv4",
            "protocol": "6",
            "security_group_id": "70f1b157-e79b-44dc-85a8-7de0fc9f2aab",
            "tenant_id": "2640ee2ac2474bf3906e482047204fcb"
        },
        {
            "id": "ccb9823e-559b-4d84-b656-2739f8e56d89",
            "direction": "ingress",
            "ethertype": "IPv6",
            "protocol": 6,
            "remote_group_id": "70f1b157-e79b-44dc-85a8-7de0fc9f2aab",
            "security_group_id": "70f1b157-e79b-44dc-85a8-7de0fc9f2aab",
            "tenant_id": "2640ee2ac2474bf3906e482047204fcb"
        },
        {
            "id": "fbc3f809-7378-40a4-822f-7a70f6ccba98",
            "direction": "ingress",
            "ethertype": "IPv4",
            "protocol": "udp",
            "remote_group_id": "70f1b157-e79b-44dc-85a8-7de0fc9f2aab",
            "security_group_id": "70f1b157-e79b-44dc-85a8-7de0fc9f2aab",
            "tenant_id": "2640ee2ac2474bf3906e482047204fcb"
        }
    ]
}

SECURITY_GROUP_RULE_UPDATE = {
    "id": "9b4be7fa-e56e-40fb-9516-1f0fa9185669",
    "security_group_rule": {
        "security_group_rule": {
            "remote_group_id": None,
            "direction": "egress",
            "remote_ip_prefix": None,
            "protocol": "tcp",
            "ethertype": "IPv6",
            "tenant_id": "00f340c7c3b34ab7be1fc690c05a0275",
            "port_range_ma": 77,
            "port_range_min": 77,
            "id": "9b4be7fa-e56e-40fb-9516-1f0fa9185669",
            "security_group_id": "b60490fe-60a5-40be-af63-1d641381b784"
        }
    }
}


def change_id(security_group_rule, count):
    id = security_group_rule['security_group_rule']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    security_group_rule['security_group_rule']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return security_group_rule


class SecurityGroupRule(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_security_group_rule(self, security_group_ruleid):
        logging.info('get security_group_rule: ' + security_group_ruleid)
        return self.get(config.NEUTRON_SECURITY_GROUP_RULES + '/' + security_group_ruleid)

    def get_security_group_rules(self):
        logging.info('get all security_group_rules')
        return self.get(config.NEUTRON_SECURITY_GROUP_RULES)

    def create_security_group_rule(self, payload):
        if 'security_group_rule' in payload:
            logging.info('create security_group_rule: ' + payload['security_group_rule']['id'])
        else:
            logging.info('bulk create security_group_rules: ' + ', '.join([s['id']
                                                                           for s in payload['security_group_rules']]))
        return self.post(config.NEUTRON_SECURITY_GROUP_RULES, payload)

    def update_security_group_rule(self, security_group_ruleid, payload):
        logging.info('update security_group_rule: ' + security_group_ruleid)
        return self.put(config.NEUTRON_SECURITY_GROUP_RULES + '/' + security_group_ruleid, payload)

    def delete_security_group_rule(self, security_group_ruleid):
        logging.info('delete security_group_rule: ' + security_group_ruleid)
        return self.delete(config.NEUTRON_SECURITY_GROUP_RULES + '/' + security_group_ruleid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform security_group_rule tests, server: %s, user: %s' % (servername, username))

        tester = SecurityGroupRule(servername, username)

        utils.assert_status(tester.get_security_group_rules(), 200)

        security_group_rule_one = tester.create_security_group_rule(change_id(SECURITY_GROUP_RULE_ONE, count))
        utils.assert_status(security_group_rule_one, 201)

        if security_group_rule_one.status_code == 201:
            security_group_rule_one_id = json.loads(security_group_rule_one.text)['security_group_rule']['id']
            utils.assert_status(tester.get_security_group_rule(security_group_rule_one_id), 200)

        utils.assert_status(tester.update_security_group_rule(
            change_id(SECURITY_GROUP_RULE_UPDATE['security_group_rule'], count)['security_group_rule']['id'],
            change_id(SECURITY_GROUP_RULE_UPDATE['security_group_rule'], count)), 201)

        if count == 0:
            utils.assert_status(tester.create_security_group_rule(SECURITY_GROUP_RULES_BULK), 201)
            utils.assert_status(tester.delete_security_group_rule(
                SECURITY_GROUP_RULES_BULK['security_group_rules'][0]['id']), 204)

            utils.assert_status(tester.get_security_group_rule(
                SECURITY_GROUP_RULES_BULK['security_group_rules'][0]['id']), 404)

        security_group_rules = tester.get_security_group_rules()

        if 'status code: 401' in security_group_rules.text:
            utils.assert_status(tester.delete_security_group_rule('0000'), 204)
            return

        for s in json.loads(security_group_rules.text)['security_group_rules']:
            utils.assert_status(tester.delete_security_group_rule(s['id']), 204)

if __name__ == '__main__':
    SecurityGroupRule.perform_tests('server', 'admin')
