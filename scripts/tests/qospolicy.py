import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

QOS_POLICY_ONE = {
    "policy": {
        "shared": False,
        "tenant_id": "aa902936679e4ea29bfe1158e3450a13",
        "id": "d6220bbb-35f3-48ab-8eae-69c60aef3546",
        "name": "jaxb-test"
    }
}

QOS_POLICY_UPDATE = {
    "id": "d6220bbb-35f3-48ab-8eae-69c60aef3546",
    "policy": {
        "policy": {
            "bandwidth_limit_rules": [
                {
                    "tenant_id": "aa902936679e4ea29bfe1158e3450a14",
                    "id": "d6220bbb-35f3-48ab-8eae-69c60aef3547",
                    "max_burst_kbps": 100,
                    "max_kbps": 25
                }
            ],
            "name": "jaxb-test",
            "tenant_id": "aa902936679e4ea29bfe1158e3450a13",
            "dscp_marking_rules": [
                {
                    "tenant_id": "aa902936679e4ea29bfe1158e3450a14",
                    "dscp_mark": 8,
                    "id": "d6220bbb-35f3-48ab-8eae-69c60aef3547"
                }
            ],
            "shared": False,
            "id": "d6220bbb-35f3-48ab-8eae-69c60aef3546"
        }
    }
}


class QosPolicy(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_qos_policy(self, qos_policyid):
        logging.info('get qos_policy: ' + qos_policyid)
        return self.get(config.NEUTRON_QOS_POLICIES + '/' + qos_policyid)

    def get_qos_policys(self):
        logging.info('get all qos_policys')
        return self.get(config.NEUTRON_QOS_POLICIES)

    def create_qos_policy(self, payload):
        logging.info('create qos_policy: ' + payload['policy']['id'])
        return self.post(config.NEUTRON_QOS_POLICIES, payload)

    def update_qos_policy(self, qos_policyid, payload):
        logging.info('update qos_policy: ' + qos_policyid)
        return self.put(config.NEUTRON_QOS_POLICIES + '/' + qos_policyid, payload)

    def delete_qos_policy(self, qos_policyid):
        logging.info('delete qos_policy: ' + qos_policyid)
        return self.delete(config.NEUTRON_QOS_POLICIES + '/' + qos_policyid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform qos_policy tests, server: %s, user: %s' % (servername, username))

        tester = QosPolicy(servername, username)

        utils.assert_status(tester.get_qos_policys(), 200)

        qos_policy_one = tester.create_qos_policy(QOS_POLICY_ONE)
        utils.assert_status(qos_policy_one, 201)

        qos_policy_one_id = json.loads(qos_policy_one.text)['policy']['id']

        utils.assert_status(tester.get_qos_policy(qos_policy_one_id), 200)

        utils.assert_status(tester.update_qos_policy(QOS_POLICY_UPDATE['id'], QOS_POLICY_UPDATE['policy']), 200)

        utils.assert_status(tester.delete_qos_policy(qos_policy_one_id), 204)

        utils.assert_status(tester.get_qos_policy(qos_policy_one_id), 404)
