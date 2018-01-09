import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

SFC_PORT_PAIR_GROUP_ONE = {
    "portpairgroup": {
        "name": "portpair1",
        "port_pairs": [],
        "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
        "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
    }
}

SFC_PORT_PAIR_GROUP_UPDATE = {
    "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
    "portpairgroup": {
        "portpairgroup": {
            "name": "portpair1",
            "port_pairs": [
                "d11e9190-73d4-11e5-b392-2c27d72acb4c",
                "d11e9190-73d4-11e5-b392-2c27d72acb4d"
            ],
            "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
        }
    }
}


def change_id(portpairgroup, count):
    id = portpairgroup['portpairgroup']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    portpairgroup['portpairgroup']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return portpairgroup


class SFCPortPairGroup(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_sfc_port_pair_group(self, sfc_port_pair_groupid):
        logging.info('get sfc_port_pair_group: ' + sfc_port_pair_groupid)
        return self.get(config.NEUTRON_SFC_PORT_PAIR_GROUPS + '/' + sfc_port_pair_groupid)

    def get_sfc_port_pair_groups(self):
        logging.info('get all sfc_port_pair_groups')
        return self.get(config.NEUTRON_SFC_PORT_PAIR_GROUPS)

    def create_sfc_port_pair_group(self, payload):
        logging.info('create sfc_port_pair_group: ' + payload['portpairgroup']['id'])
        return self.post(config.NEUTRON_SFC_PORT_PAIR_GROUPS, payload)

    def update_sfc_port_pair_group(self, sfc_port_pair_groupid, payload):
        logging.info('update sfc_port_pair_group: ' + sfc_port_pair_groupid)
        return self.put(config.NEUTRON_SFC_PORT_PAIR_GROUPS + '/' + sfc_port_pair_groupid, payload)

    def delete_sfc_port_pair_group(self, sfc_port_pair_groupid):
        logging.info('delete sfc_port_pair_group: ' + sfc_port_pair_groupid)
        return self.delete(config.NEUTRON_SFC_PORT_PAIR_GROUPS + '/' + sfc_port_pair_groupid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform sfc_port_pair_group tests, server: %s, user: %s' % (servername, username))

        tester = SFCPortPairGroup(servername, username)

        utils.assert_status(tester.get_sfc_port_pair_groups(), 200)

        sfc_port_pair_group_one = tester.create_sfc_port_pair_group(change_id(SFC_PORT_PAIR_GROUP_ONE, count))
        utils.assert_status(sfc_port_pair_group_one, 201)

        if sfc_port_pair_group_one.status_code == 201:
            sfc_port_pair_group_one_id = json.loads(sfc_port_pair_group_one.text)['portpairgroup']['id']
            utils.assert_status(tester.get_sfc_port_pair_group(sfc_port_pair_group_one_id), 200)

        utils.assert_status(tester.update_sfc_port_pair_group(
            change_id(SFC_PORT_PAIR_GROUP_UPDATE['portpairgroup'], count)['portpairgroup']['id'],
            change_id(SFC_PORT_PAIR_GROUP_UPDATE['portpairgroup'], count)), 201)

        utils.assert_status(tester.delete_sfc_port_pair_group(
            change_id(SFC_PORT_PAIR_GROUP_ONE, count)['portpairgroup']['id']), 204)

        utils.assert_status(tester.get_sfc_port_pair_group(
            change_id(SFC_PORT_PAIR_GROUP_ONE, count)['portpairgroup']['id']), 404)


if __name__ == '__main__':
    SFCPortPairGroup.perform_tests('server', 'admin')
