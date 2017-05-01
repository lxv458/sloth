import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

LOAD_BALANCER_POOL_ONE = {
    "pool": {
        "admin_state_up": True,
        "description": "simple pool",
        "healthmonitor_id": None,
        "id": "12ff63af-4127-4074-a251-bcb2ecc53ebe",
        "lb_algorithm": "ROUND_ROBIN",
        "listeners": [
            {
                "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829"
            }
        ],
        "members": [],
        "name": "pool1",
        "protocol": "HTTP",
        "session_persistence": {
            "cookie_name": "my_cookie",
            "type": "APP_COOKIE"
        },
        "tenant_id": "b7c1a69e88bf4b21a8148f787aef2081"
    }
}

LOAD_BALANCER_POOL_UPDATE = {
    "id": "12ff63af-4127-4074-a251-bcb2ecc53ebe",
    "pool": {
        "pool": {
            "admin_state_up": False,
            "description": "pool two",
            "healthmonitor_id": None,
            "id": "12ff63af-4127-4074-a251-bcb2ecc53ebe",
            "lb_algorithm": "LEAST_CONNECTIONS",
            "listeners": [
                {
                    "id": "39de4d56-d663-46e5-85a1-5b9d5fa17829"
                }
            ],
            "members": [],
            "name": "pool2",
            "protocol": "HTTP",
            "session_persistence": {
                "cookie_name": None,
                "type": "HTTP_COOKIE"
            },
            "tenant_id": "1a3e005cf9ce40308c900bcb08e5320c"
        }
    }
}


def change_id(pool, count):
    id = pool['pool']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    pool['pool']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return pool


class LoadbalancerPool(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_loadbalancer_pool(self, loadbalancer_poolid):
        logging.info('get loadbalancer_pool: ' + loadbalancer_poolid)
        return self.get(config.NEUTRON_LOAD_BALANCER_POOLS + '/' + loadbalancer_poolid)

    def get_loadbalancer_pools(self):
        logging.info('get all loadbalancer_pools')
        return self.get(config.NEUTRON_LOAD_BALANCER_POOLS)

    def create_loadbalancer_pool(self, payload):
        logging.info('create loadbalancer_pool: ' + payload['pool']['id'])
        return self.post(config.NEUTRON_LOAD_BALANCER_POOLS, payload)

    def update_loadbalancer_pool(self, loadbalancer_poolid, payload):
        logging.info('update loadbalancer_pool: ' + loadbalancer_poolid)
        return self.put(config.NEUTRON_LOAD_BALANCER_POOLS + '/' + loadbalancer_poolid, payload)

    def delete_loadbalancer_pool(self, loadbalancer_poolid):
        logging.info('delete loadbalancer_pool: ' + loadbalancer_poolid)
        return self.delete(config.NEUTRON_LOAD_BALANCER_POOLS + '/' + loadbalancer_poolid)

    @staticmethod
    def perform_tests(servername, username, count):
        logging.info('perform loadbalancer_pool tests, server: %s, user: %s' % (servername, username))

        tester = LoadbalancerPool(servername, username)

        utils.assert_status(tester.get_loadbalancer_pools(), 200)

        loadbalancer_pool_one = tester.create_loadbalancer_pool(change_id(LOAD_BALANCER_POOL_ONE, count))
        utils.assert_status(loadbalancer_pool_one, 201)

        loadbalancer_pool_one_id = json.loads(loadbalancer_pool_one.text)['pool']['id']

        utils.assert_status(tester.get_loadbalancer_pool(loadbalancer_pool_one_id), 200)

        utils.assert_status(tester.update_loadbalancer_pool(
            change_id(LOAD_BALANCER_POOL_UPDATE['pool'], count)['pool']['id'],
            change_id(LOAD_BALANCER_POOL_UPDATE['pool'], count)), 200)

        utils.assert_status(tester.delete_loadbalancer_pool(loadbalancer_pool_one_id), 204)

        utils.assert_status(tester.get_loadbalancer_pool(loadbalancer_pool_one_id), 404)

if __name__ == '__main__':
    LoadbalancerPool.perform_tests('server', 'admin', 0)
