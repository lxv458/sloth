import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

SFC_PORT_CHAIN_ONE = {
    "portchain": {
        "name": "portchain1",
        "port_pair_groups": [
            "4512d643-24fc-4fae-af4b-321c5e2eb3d1",
            "4a634d49-76dc-4fae-af4b-321c5e23d651"
        ],
        "flow_classifiers": [
            "4a334cd4-fe9c-4fae-af4b-321c5e2eb051",
            "105a4b0a-73d6-11e5-b392-2c27d72acb4c"
        ],
        "chain_parameters": [
            {
                "correlation": "value"
            }
        ],
        "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
        "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
    }
}

SFC_PORT_CHAIN_UPDATE = {
    "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
    "portchain": {
        "portchain": {
            "name": "portchain1",
            "port_pair_groups": [
                "4512d643-24fc-4fae-af4b-321c5e2eb3d1",
                "4a634d49-76dc-4fae-af4b-321c5e23d651",
                "4a634d49-76dc-4fae-af4b-321c5e23d652"
            ],
            "flow_classifiers": [
                "4a334cd4-fe9c-4fae-af4b-321c5e2eb051",
                "105a4b0a-73d6-11e5-b392-2c27d72acb4c"
            ],
            "chain_parameters": [
                {
                    "correlation": "value"
                }
            ],
            "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
        }
    }
}


def change_id(portchain, count):
    id = portchain['portchain']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    portchain['portchain']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return portchain


class SFCPortChain(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_sfc_port_chain(self, sfc_port_chainid):
        logging.info('get sfc_port_chain: ' + sfc_port_chainid)
        return self.get(config.NEUTRON_SFC_PORT_CHAINS + '/' + sfc_port_chainid)

    def get_sfc_port_chains(self):
        logging.info('get all sfc_port_chains')
        return self.get(config.NEUTRON_SFC_PORT_CHAINS)

    def create_sfc_port_chain(self, payload):
        logging.info('create sfc_port_chain: ' + payload['portchain']['id'])
        return self.post(config.NEUTRON_SFC_PORT_CHAINS, payload)

    def update_sfc_port_chain(self, sfc_port_chainid, payload):
        logging.info('update sfc_port_chain: ' + sfc_port_chainid)
        return self.put(config.NEUTRON_SFC_PORT_CHAINS + '/' + sfc_port_chainid, payload)

    def delete_sfc_port_chain(self, sfc_port_chainid):
        logging.info('delete sfc_port_chain: ' + sfc_port_chainid)
        return self.delete(config.NEUTRON_SFC_PORT_CHAINS + '/' + sfc_port_chainid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform sfc_port_chain tests, server: %s, user: %s' % (servername, username))

        tester = SFCPortChain(servername, username)

        utils.assert_status(tester.get_sfc_port_chains(), 200)

        sfc_port_chain_one = tester.create_sfc_port_chain(change_id(SFC_PORT_CHAIN_ONE, count))
        utils.assert_status(sfc_port_chain_one, 201)

        if sfc_port_chain_one.status_code == 201:
            sfc_port_chain_one_id = json.loads(sfc_port_chain_one.text)['portchain']['id']
            utils.assert_status(tester.get_sfc_port_chain(sfc_port_chain_one_id), 200)

        utils.assert_status(tester.update_sfc_port_chain(
            change_id(SFC_PORT_CHAIN_UPDATE['portchain'], count)['portchain']['id'],
            change_id(SFC_PORT_CHAIN_UPDATE['portchain'], count)), 200)

        utils.assert_status(tester.delete_sfc_port_chain(change_id(SFC_PORT_CHAIN_ONE, count)['portchain']['id']), 204)

        utils.assert_status(tester.get_sfc_port_chain(change_id(SFC_PORT_CHAIN_ONE, count)['portchain']['id']), 404)

if __name__ == '__main__':
    SFCPortChain.perform_tests('server', 'admin')
