import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

METERING_LABEL_RULE_ONE = {
    "metering_label_rule": {
        "remote_ip_prefix": "10.0.1.0/24",
        "direction": "ingress",
        "metering_label_id": "bc91b832-8465-40a7-a5d8-ba87de442266",
        "id": "00e13b58-b4f2-4579-9c9c-7ac94615f9ae",
        "excluded": False
    }
}


def change_id(metering_label_rule, count):
    id = metering_label_rule['metering_label_rule']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    metering_label_rule['metering_label_rule']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return metering_label_rule


class MeteringLabelRule(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_metering_label_rule(self, metering_label_ruleid):
        logging.info('get metering_label_rule: ' + metering_label_ruleid)
        return self.get(config.NEUTRON_METERING_LABEL_RULES + '/' + metering_label_ruleid)

    def get_metering_label_rules(self):
        logging.info('get all metering_label_rules')
        return self.get(config.NEUTRON_METERING_LABEL_RULES)

    def create_metering_label_rule(self, payload):
        logging.info('create metering_label_rule: ' + payload['metering_label_rule']['id'])
        return self.post(config.NEUTRON_METERING_LABEL_RULES, payload)

    def delete_metering_label_rule(self, metering_label_ruleid):
        logging.info('delete metering_label_rule: ' + metering_label_ruleid)
        return self.delete(config.NEUTRON_METERING_LABEL_RULES + '/' + metering_label_ruleid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform metering_label_rule tests, server: %s, user: %s' % (servername, username))

        tester = MeteringLabelRule(servername, username)

        utils.assert_status(tester.get_metering_label_rules(), 200)

        metering_label_rule_one = tester.create_metering_label_rule(change_id(METERING_LABEL_RULE_ONE, count))
        utils.assert_status(metering_label_rule_one, 201)

        if metering_label_rule_one.status_code == 201:
            metering_label_rule_one_id = json.loads(metering_label_rule_one.text)['metering_label_rule']['id']
            utils.assert_status(tester.get_metering_label_rule(metering_label_rule_one_id), 200)

        utils.assert_status(tester.delete_metering_label_rule(
            change_id(METERING_LABEL_RULE_ONE, count)['metering_label_rule']['id']), 204)

        utils.assert_status(tester.get_metering_label_rule(
            change_id(METERING_LABEL_RULE_ONE, count)['metering_label_rule']['id']), 404)

if __name__ == '__main__':
    MeteringLabelRule.perform_tests('server', 'admin')
