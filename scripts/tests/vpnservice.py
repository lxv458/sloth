import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

VPN_SERVICE_ONE = {
    "vpnservice": {
        "router_id": "ec8619be-0ba8-4955-8835-3b49ddb76f89",
        "status": "PENDING_CREATE",
        "name": "myservice",
        "admin_state_up": True,
        "subnet_id": "f4fb4528-ed93-467c-a57b-11c7ea9f963e",
        "tenant_id": "ccb81365fe36411a9011e90491fe1330",
        "id": "9faaf49f-dd89-4e39-a8c6-101839aa49bc",
        "description": ""
    }
}

VPN_SERVICE_UPDATE = {
    "id": "9faaf49f-dd89-4e39-a8c6-101839aa49bc",
    "vpnservice": {
        "vpnservice": {
            "router_id": "ec8619be-0ba8-4955-8835-3b49ddb76f89",
            "status": "PENDING_CREATE",
            "name": "myservice-update",
            "admin_state_up": True,
            "subnet_id": "f4fb4528-ed93-467c-a57b-11c7ea9f963e",
            "tenant_id": "ccb81365fe36411a9011e90491fe1330",
            "id": "9faaf49f-dd89-4e39-a8c6-101839aa49bc",
            "description": ""
        }
    }
}


def change_id(vpnservice, count):
    id = vpnservice['vpnservice']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    vpnservice['vpnservice']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return vpnservice


class VpnService(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_vpn_service(self, vpn_serviceid):
        logging.info('get vpn_service: ' + vpn_serviceid)
        return self.get(config.NEUTRON_VPN_SERVICES + '/' + vpn_serviceid)

    def get_vpn_services(self):
        logging.info('get all vpn_services')
        return self.get(config.NEUTRON_VPN_SERVICES)

    def create_vpn_service(self, payload):
        logging.info('create vpn_service: ' + payload['vpnservice']['id'])
        return self.post(config.NEUTRON_VPN_SERVICES, payload)

    def update_vpn_service(self, vpn_serviceid, payload):
        logging.info('update vpn_service: ' + vpn_serviceid)
        return self.put(config.NEUTRON_VPN_SERVICES + '/' + vpn_serviceid, payload)

    def delete_vpn_service(self, vpn_serviceid):
        logging.info('delete vpn_service: ' + vpn_serviceid)
        return self.delete(config.NEUTRON_VPN_SERVICES + '/' + vpn_serviceid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform vpn_service tests, server: %s, user: %s' % (servername, username))

        tester = VpnService(servername, username)

        utils.assert_status(tester.get_vpn_services(), 200)

        vpn_service_one = tester.create_vpn_service(change_id(VPN_SERVICE_ONE, count))
        utils.assert_status(vpn_service_one, 201)

        if vpn_service_one.status_code == 201:
            vpn_service_one_id = json.loads(vpn_service_one.text)['vpnservice']['id']
            utils.assert_status(tester.get_vpn_service(vpn_service_one_id), 200)

        utils.assert_status(tester.update_vpn_service(
            change_id(VPN_SERVICE_UPDATE['vpnservice'], count)['vpnservice']['id'],
            change_id(VPN_SERVICE_UPDATE['vpnservice'], count)), 201)

        utils.assert_status(tester.delete_vpn_service(change_id(VPN_SERVICE_ONE, count)['vpnservice']['id']), 204)

        utils.assert_status(tester.get_vpn_service(change_id(VPN_SERVICE_ONE, count)['vpnservice']['id']), 404)

if __name__ == '__main__':
    VpnService.perform_tests('server', 'admin')
