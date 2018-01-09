import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

LOAD_BALANCER_ONE = {
    "loadbalancer": {
        "description": "simple lb",
        "admin_state_up": True,
        "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081",
        "provisioning_status": "ACTIVE",
        "listeners": [],
        "vip_address": "10.0.0.4",
        "vip_subnet_id": "013d3059-87a4-45a5-91e9-d721068ae0b2",
        "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c",
        "operating_status": "ONLINE",
        "name": "loadbalancer1"
    }
}

LOAD_BALANCER_UPDATE = {
    "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c",
    "loadbalancer": {
        "loadbalancer": {
            "description": "simple lb2",
            "admin_state_up": False,
            "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081",
            "provisioning_status": "PENDING_UPDATE",
            "listeners": [],
            "vip_address": "10.0.0.4",
            "vip_subnet_id": "013d3059-87a4-45a5-91e9-d721068ae0b2",
            "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c",
            "operating_status": "ONLINE",
            "name": "loadbalancer2"
        }
    }
}


def change_id(loadbalancer, count):
    id = loadbalancer['loadbalancer']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    loadbalancer['loadbalancer']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return loadbalancer


class Loadbalancer(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_loadbalancer(self, loadbalancerid):
        logging.info('get loadbalancer: ' + loadbalancerid)
        return self.get(config.NEUTRON_LOAD_BALANCERS + '/' + loadbalancerid)

    def get_loadbalancers(self):
        logging.info('get all loadbalancers')
        return self.get(config.NEUTRON_LOAD_BALANCERS)

    def create_loadbalancer(self, payload):
        logging.info('create loadbalancer: ' + payload['loadbalancer']['id'])
        return self.post(config.NEUTRON_LOAD_BALANCERS, payload)

    def update_loadbalancer(self, loadbalancerid, payload):
        logging.info('update loadbalancer: ' + loadbalancerid)
        return self.put(config.NEUTRON_LOAD_BALANCERS + '/' + loadbalancerid, payload)

    def delete_loadbalancer(self, loadbalancerid):
        logging.info('delete loadbalancer: ' + loadbalancerid)
        return self.delete(config.NEUTRON_LOAD_BALANCERS + '/' + loadbalancerid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform loadbalancer tests, server: %s, user: %s' % (servername, username))

        tester = Loadbalancer(servername, username)

        utils.assert_status(tester.get_loadbalancers(), 200)

        loadbalancer_one = tester.create_loadbalancer(change_id(LOAD_BALANCER_ONE, count))
        utils.assert_status(loadbalancer_one, 201)

        if loadbalancer_one.status_code == 201:
            loadbalancer_one_id = json.loads(loadbalancer_one.text)['loadbalancer']['id']
            utils.assert_status(tester.get_loadbalancer(loadbalancer_one_id), 200)

        utils.assert_status(tester.update_loadbalancer(
            change_id(LOAD_BALANCER_UPDATE['loadbalancer'], count)['loadbalancer']['id'],
            change_id(LOAD_BALANCER_UPDATE['loadbalancer'], count)), 201)

        utils.assert_status(tester.delete_loadbalancer(change_id(LOAD_BALANCER_ONE, count)['loadbalancer']['id']), 204)

        utils.assert_status(tester.get_loadbalancer(change_id(LOAD_BALANCER_ONE, count)['loadbalancer']['id']), 404)

if __name__ == '__main__':
    Loadbalancer.perform_tests('server', 'admin')
