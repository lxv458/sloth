import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

LOAD_BALANCER_LISTENER_ONE = {
    "listener": {
        "admin_state_up": True,
        "connection_limit": 100,
        "default_pool_id": None,
        "description": "listener one",
        "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829",
        "loadbalancers": [
            {
                "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c"
            }
        ],
        "name": "listener1",
        "protocol": "HTTP",
        "protocol_port": 80,
        "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081"
    }
}

LOAD_BALANCER_LISTENER_UPDATE = {
    "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829",
    "listener": {
        "listener": {
            "admin_state_up": False,
            "connection_limit": 200,
            "default_pool_id": None,
            "description": "listener two",
            "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829",
            "loadbalancers": [
                {
                    "id": "a36c20d0-18e9-42ce-88fd-82a35977ee8c"
                }
            ],
            "name": "listener2",
            "protocol": "HTTP",
            "protocol_port": 80,
            "tenant_id": "1a3e005cf9ce40308c900bcb08e5320c"
        }
    }
}


def change_id(listener, count):
    id = listener['listener']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    listener['listener']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return listener


class LoadbalancerListener(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_loadbalancer_listener(self, loadbalancer_listenerid):
        logging.info('get loadbalancer_listener: ' + loadbalancer_listenerid)
        return self.get(config.NEUTRON_LOAD_BALANCER_LISTENERS + '/' + loadbalancer_listenerid)

    def get_loadbalancer_listeners(self):
        logging.info('get all loadbalancer_listeners')
        return self.get(config.NEUTRON_LOAD_BALANCER_LISTENERS)

    def create_loadbalancer_listener(self, payload):
        logging.info('create loadbalancer_listener: ' + payload['listener']['id'])
        return self.post(config.NEUTRON_LOAD_BALANCER_LISTENERS, payload)

    def update_loadbalancer_listener(self, loadbalancer_listenerid, payload):
        logging.info('update loadbalancer_listener: ' + loadbalancer_listenerid)
        return self.put(config.NEUTRON_LOAD_BALANCER_LISTENERS + '/' + loadbalancer_listenerid, payload)

    def delete_loadbalancer_listener(self, loadbalancer_listenerid):
        logging.info('delete loadbalancer_listener: ' + loadbalancer_listenerid)
        return self.delete(config.NEUTRON_LOAD_BALANCER_LISTENERS + '/' + loadbalancer_listenerid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform loadbalancer_listener tests, server: %s, user: %s' % (servername, username))

        tester = LoadbalancerListener(servername, username)

        utils.assert_status(tester.get_loadbalancer_listeners(), 200)

        loadbalancer_listener_one = tester.create_loadbalancer_listener(change_id(LOAD_BALANCER_LISTENER_ONE, count))
        utils.assert_status(loadbalancer_listener_one, 201)

        loadbalancer_listener_one_id = json.loads(loadbalancer_listener_one.text)['listener']['id']

        utils.assert_status(tester.get_loadbalancer_listener(loadbalancer_listener_one_id), 200)

        utils.assert_status(tester.update_loadbalancer_listener(
            change_id(LOAD_BALANCER_LISTENER_UPDATE['listener'], count)['listener']['id'],
            change_id(LOAD_BALANCER_LISTENER_UPDATE['listener'], count)), 200)

        utils.assert_status(tester.delete_loadbalancer_listener(loadbalancer_listener_one_id), 204)

        utils.assert_status(tester.get_loadbalancer_listener(loadbalancer_listener_one_id), 404)


if __name__ == '__main__':
    LoadbalancerListener.perform_tests('server', 'admin')
