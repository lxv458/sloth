import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

FLOATING_IP_ONE = {
    "floatingip": {
        "fixed_ip_address": "10.0.0.3",
        "floating_ip_address": "172.24.4.228",
        "floating_network_id": "376da547-b977-4cfe-9cba-275c80debf57",
        "id": "2f245a7b-796b-4f26-9cf9-9e82d248fda7",
        "port_id": "ce705c24-c1ef-408a-bda3-7bbd946164ab",
        "router_id": "d23abc8d-2991-4a55-ba98-2aaea84cc72f",
        "status": "ACTIVE",
        "tenant_id": "4969c491a3c74ee4af974e6d800c62de"
    }
}
FLOATING_IP_UPDATE_ONE = {
    "id": "2f245a7b-796b-4f26-9cf9-9e82d248fda7",
    "floatingip": {
        "floatingip": {
            "floating_network_id": "376da547-b977-4cfe-9cba-275c80debf57",
            "router_id": "d23abc8d-2991-4a55-ba98-2aaea84cc72f",
            "fixed_ip_address": "10.0.0.4",
            "floating_ip_address": "172.24.4.228",
            "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
            "status": "ACTIVE",
            "port_id": "fc861431-0e6c-4842-a0ed-e2363f9bc3a8",
            "id": "2f245a7b-796b-4f26-9cf9-9e82d248fda7"
        }
    }
}
FLOATING_IP_UPDATE_TWO = {
    "id": "2f245a7b-796b-4f26-9cf9-9e82d248fda7",
    "floatingip": {
        "floatingip": {
            "floating_network_id": "376da547-b977-4cfe-9cba-275c80debf57",
            "router_id": "d23abc8d-2991-4a55-ba98-2aaea84cc72f",
            "fixed_ip_address": None,
            "floating_ip_address": "172.24.4.228",
            "tenant_id": "4969c491a3c74ee4af974e6d800c62de",
            "status": "ACTIVE",
            "port_id": None,
            "id": "2f245a7b-796b-4f26-9cf9-9e82d248fda7"
        }
    }
}


class FloatingIP(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_floating_ip(self, floating_ip_id):
        logging.info('get floating_ip: ' + floating_ip_id)
        return self.get(config.NEUTRON_FLOATING_IPS + '/' + floating_ip_id)

    def get_floating_ips(self):
        logging.info('get all floating_ips')
        return self.get(config.NEUTRON_FLOATING_IPS)

    def create_floating_ip(self, payload):
        logging.info('create floating_ip: ' + payload['floatingip']['id'])
        return self.post(config.NEUTRON_FLOATING_IPS, payload)

    def update_floating_ip(self, floating_ip_id, payload):
        logging.info('update floating_ip: ' + floating_ip_id)
        return self.put(config.NEUTRON_FLOATING_IPS + '/' + floating_ip_id, payload)

    def delete_floating_ip(self, floating_ip_id):
        logging.info('delete floating_ip: ' + floating_ip_id)
        return self.delete(config.NEUTRON_FLOATING_IPS + '/' + floating_ip_id)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform floating_ip tests, server: %s, user: %s' % (servername, username))

        tester = FloatingIP(servername, username)

        utils.assert_status(tester.get_floating_ips(), 200)

        floating_ip_one = tester.create_floating_ip(FLOATING_IP_ONE)
        utils.assert_status(floating_ip_one, 201)

        floating_ip_one_id = json.loads(floating_ip_one.text)['floatingip']['id']

        utils.assert_status(tester.get_floating_ip(floating_ip_one_id), 200)

        utils.assert_status(tester.update_floating_ip(FLOATING_IP_UPDATE_ONE['id'],
                                                      FLOATING_IP_UPDATE_ONE['floatingip']), 200)

        utils.assert_status(tester.update_floating_ip(FLOATING_IP_UPDATE_TWO['id'],
                                                      FLOATING_IP_UPDATE_TWO['floatingip']), 200)

        utils.assert_status(tester.delete_floating_ip(floating_ip_one_id), 204)

        utils.assert_status(tester.get_floating_ip(floating_ip_one_id), 404)


if __name__ == '__main__':
    FloatingIP.perform_tests('server', 'admin')
