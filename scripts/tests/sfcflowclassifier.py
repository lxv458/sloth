import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

SFC_FLOW_CLASSIFIER_ONE = {
    "flowclassifier": {
        "name": "flowclassifier1",
        "ethertype": "IPv4",
        "protocol": "udp",
        "source_port_range_min": 100,
        "source_port_range_max": 200,
        "destination_port_range_min": 100,
        "destination_port_range_max": 200,
        "source_ip_prefix": "10.0.0.0/24",
        "destination_ip_prefix": "11.0.0.0/24",
        "logical_source_port": "5e8e5957-649f-477b-9e5b-f1f75b21c03c",
        "logical_destination_port": "6e8e5957-649f-477b-9e5b-f1f75b21c03c",
        "l7_parameters": [
            {
                "Key": "value"
            }
        ],
        "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
        "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
    }
}

SFC_FLOW_CLASSIFIER_UPDATE = {
    "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
    "flowclassifier": {
        "flowclassifier": {
            "name": "flowclassifier1",
            "ethertype": "IPv4",
            "protocol": "udp",
            "source_port_range_min": 100,
            "source_port_range_max": 200,
            "destination_port_range_min": 100,
            "destination_port_range_max": 200,
            "source_ip_prefix": "10.0.0.0/24",
            "destination_ip_prefix": "11.0.0.0/24",
            "logical_source_port": "5e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "logical_destination_port": "6e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "l7_parameters": [
                {
                    "Key": "value"
                }
            ],
            "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
        }
    }
}


def change_id(flowclassifier, count):
    id = flowclassifier['flowclassifier']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    flowclassifier['flowclassifier']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return flowclassifier


class SFCFlowClassifier(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_sfc_flow_classifier(self, sfc_flow_classifierid):
        logging.info('get sfc_flow_classifier: ' + sfc_flow_classifierid)
        return self.get(config.NEUTRON_SFC_FLOW_CLASSIFIERS + '/' + sfc_flow_classifierid)

    def get_sfc_flow_classifiers(self):
        logging.info('get all sfc_flow_classifiers')
        return self.get(config.NEUTRON_SFC_FLOW_CLASSIFIERS)

    def create_sfc_flow_classifier(self, payload):
        logging.info('create sfc_flow_classifier: ' + payload['flowclassifier']['id'])
        return self.post(config.NEUTRON_SFC_FLOW_CLASSIFIERS, payload)

    def update_sfc_flow_classifier(self, sfc_flow_classifierid, payload):
        logging.info('update sfc_flow_classifier: ' + sfc_flow_classifierid)
        return self.put(config.NEUTRON_SFC_FLOW_CLASSIFIERS + '/' + sfc_flow_classifierid, payload)

    def delete_sfc_flow_classifier(self, sfc_flow_classifierid):
        logging.info('delete sfc_flow_classifier: ' + sfc_flow_classifierid)
        return self.delete(config.NEUTRON_SFC_FLOW_CLASSIFIERS + '/' + sfc_flow_classifierid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform sfc_flow_classifier tests, server: %s, user: %s' % (servername, username))

        tester = SFCFlowClassifier(servername, username)

        utils.assert_status(tester.get_sfc_flow_classifiers(), 200)

        sfc_flow_classifier_one = tester.create_sfc_flow_classifier(change_id(SFC_FLOW_CLASSIFIER_ONE, count))
        utils.assert_status(sfc_flow_classifier_one, 201)

        if sfc_flow_classifier_one.status_code == 201:
            sfc_flow_classifier_one_id = json.loads(sfc_flow_classifier_one.text)['flowclassifier']['id']
            utils.assert_status(tester.get_sfc_flow_classifier(sfc_flow_classifier_one_id), 200)

        utils.assert_status(tester.update_sfc_flow_classifier(
            change_id(SFC_FLOW_CLASSIFIER_UPDATE['flowclassifier'], count)['flowclassifier']['id'],
            change_id(SFC_FLOW_CLASSIFIER_UPDATE['flowclassifier'], count)), 200)

        utils.assert_status(tester.delete_sfc_flow_classifier(
            change_id(SFC_FLOW_CLASSIFIER_ONE, count)['flowclassifier']['id']), 204)

        utils.assert_status(tester.get_sfc_flow_classifier(
            change_id(SFC_FLOW_CLASSIFIER_ONE, count)['flowclassifier']['id']), 404)

if __name__ == '__main__':
    SFCFlowClassifier.perform_tests('server', 'admin')
