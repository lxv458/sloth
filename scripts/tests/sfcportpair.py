import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

SFC_PORT_PAIR_ONE = {
    "portpair": {
        "name": "portpair1",
        "ingress": "5e8e5957-649f-477b-9e5b-f1f75b21c03c",
        "egress": "6e8e5957-649f-477b-9e5b-f1f75b21c03c",
        "service_function_parameters": [
            {
                "correlation": "value"
            }
        ],
        "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
        "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
    }
}

SFC_PORT_PAIR_UPDATE = {
    "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
    "portpair": {
        "portpair": {
            "name": "portpair2",
            "ingress": "5e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "egress": "6e8e5957-649f-477b-9e5b-f1f75b21c03c",
            "service_function_parameters": [
                {
                    "correlation": "value"
                }
            ],
            "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
        }
    }
}


class SFCPortPair(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_sfc_port_pair(self, sfc_port_pairid):
        logging.info('get sfc_port_pair: ' + sfc_port_pairid)
        return self.get(config.NEUTRON_SFC_PORT_PAIRS + '/' + sfc_port_pairid)

    def get_sfc_port_pairs(self):
        logging.info('get all sfc_port_pairs')
        return self.get(config.NEUTRON_SFC_PORT_PAIRS)

    def create_sfc_port_pair(self, payload):
        logging.info('create sfc_port_pair: ' + payload['portpair']['id'])
        return self.post(config.NEUTRON_SFC_PORT_PAIRS, payload)

    def update_sfc_port_pair(self, sfc_port_pairid, payload):
        logging.info('update sfc_port_pair: ' + sfc_port_pairid)
        return self.put(config.NEUTRON_SFC_PORT_PAIRS + '/' + sfc_port_pairid, payload)

    def delete_sfc_port_pair(self, sfc_port_pairid):
        logging.info('delete sfc_port_pair: ' + sfc_port_pairid)
        return self.delete(config.NEUTRON_SFC_PORT_PAIRS + '/' + sfc_port_pairid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform sfc_port_pair tests, server: %s, user: %s' % (servername, username))

        tester = SFCPortPair(servername, username)

        utils.assert_status(tester.get_sfc_port_pairs(), 200)

        sfc_port_pair_one = tester.create_sfc_port_pair(SFC_PORT_PAIR_ONE)
        utils.assert_status(sfc_port_pair_one, 201)

        sfc_port_pair_one_id = json.loads(sfc_port_pair_one.text)['portpair']['id']

        utils.assert_status(tester.get_sfc_port_pair(sfc_port_pair_one_id), 200)

        utils.assert_status(tester.update_sfc_port_pair(SFC_PORT_PAIR_UPDATE['id'],
                                                        SFC_PORT_PAIR_UPDATE['portpair']), 200)

        utils.assert_status(tester.delete_sfc_port_pair(sfc_port_pair_one_id), 204)

        utils.assert_status(tester.get_sfc_port_pair(sfc_port_pair_one_id), 404)
