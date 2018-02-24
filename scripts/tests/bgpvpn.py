import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

BGPVPN_ONE = {
    "bgpvpn": {
        "status": "ACTIVE",
        "type": "l3",
        "name": "vpn1",
        "admin_state_up": True,
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "route_targets": "64512:1",
        "networks": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
        "auto_aggregate": True,
        "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
    }
}

BGPVPNS_BULK = {
    "bgpvpns": [
        {
            "status": "ACTIVE",
            "name": "sample_bgpvpn1",
            "admin_state_up": True,
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
            "id": "bc1a76cb-8767-4c3a-bb95-018b822f2130",
            "route_targets": "64512:1",
            "auto_aggregate": True,
            "type": "l3"
        },
        {
            "status": "ACTIVE",
            "name": "sample_bgpvpn2",
            "admin_state_up": True,
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
            "id": "af374017-c9ae-4a1d-b799-ab73111476e2",
            "route_targets": "64512:2",
            "auto_aggregate": False,
            "type": "l3"
        }
    ]
}

BGPVPN_UPDATE = {
    "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c",
    "bgpvpn": {
        "bgpvpn": {
            "status": "ACTIVE",
            "type": "l3",
            "name": "vpn1",
            "admin_state_up": True,
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "route_targets": "64512:1",
            "networks": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
            "auto_aggregate": True,
            "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
        }
    }
}


def change_id(bgpvpn, count):
    id = bgpvpn['bgpvpn']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    bgpvpn['bgpvpn']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return bgpvpn


class Bgpvpn(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_bgpvpn(self, bgpvpnid):
        logging.info('get bgpvpn: ' + bgpvpnid)
        return self.get(config.NEUTRON_BGPVPNS + '/' + bgpvpnid)

    def get_bgpvpns(self):
        logging.info('get all bgpvpns')
        return self.get(config.NEUTRON_BGPVPNS)

    def create_bgpvpn(self, payload):
        if 'bgpvpn' in payload:
            logging.info('create bgpvpn: ' + payload['bgpvpn']['id'])
        else:
            logging.info('bulk create bgpvpns: ' + ', '.join([bgp['id'] for bgp in payload['bgpvpns']]))
        return self.post(config.NEUTRON_BGPVPNS, payload)

    def update_bgpvpn(self, bgpvpnid, payload):
        logging.info('update bgpvpn: ' + bgpvpnid)
        return self.put(config.NEUTRON_BGPVPNS + '/' + bgpvpnid, payload)

    def delete_bgpvpn(self, bgpvpnid):
        logging.info('delete bgpvpn: ' + bgpvpnid)
        return self.delete(config.NEUTRON_BGPVPNS + '/' + bgpvpnid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform bgpvpn tests, server: %s, user: %s' % (servername, username))

        tester = Bgpvpn(servername, username)

        utils.assert_status(tester.get_bgpvpns(), 200)

        bgpvpn_one = tester.create_bgpvpn(change_id(BGPVPN_ONE, count))
        utils.assert_status(bgpvpn_one, 201)

        if bgpvpn_one.status_code == 201:
            bgpvpn_one_id = json.loads(bgpvpn_one.text)['bgpvpn']['id']
            utils.assert_status(tester.get_bgpvpn(bgpvpn_one_id), 200)

        utils.assert_status(tester.update_bgpvpn(change_id(BGPVPN_UPDATE['bgpvpn'], count)['bgpvpn']['id'],
                                                 change_id(BGPVPN_UPDATE['bgpvpn'], count)), 201)

        if count == 0:
            utils.assert_status(tester.create_bgpvpn(BGPVPNS_BULK), 201)
            utils.assert_status(tester.delete_bgpvpn(BGPVPNS_BULK['bgpvpns'][0]['id']), 204)

            utils.assert_status(tester.get_bgpvpn(BGPVPNS_BULK['bgpvpns'][0]['id']), 404)

        bgpvpns = tester.get_bgpvpns()

        if 'status code: 401' in bgpvpns.text:
            utils.assert_status(tester.delete_bgpvpn('0000'), 204)
            return

        for bgp in json.loads(bgpvpns.text)['bgpvpns']:
            utils.assert_status(tester.delete_bgpvpn(bgp['id']), 204)

if __name__ == '__main__':
    Bgpvpn.perform_tests('server', 'admin')
