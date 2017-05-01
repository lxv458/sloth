import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

ROUTER_ONE = {
    "router": {
        "status": "ACTIVE",
        "external_gateway_info": {
            "network_id": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
        },
        "name": "another_router",
        "admin_state_up": True,
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "id": "8604a0de-7f6b-409a-a47c-a1cc7bc77b2e"
    }
}

ROUTER_ADD_INTERFACE = {
    'id': '8604a0de-7f6b-409a-a47c-a1cc7bc77b2f',
    'interface': {
        "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "port_id": "d8a4cc85-ad78-46ac-b5a1-8e04f16fa51e",
        "id": "8604a0de-7f6b-409a-a47c-a1cc7bc77b2e"
    }
}

ROUTER_UPDATE = {
    "router": {
        "status": "ACTIVE",
        "external_gateway_info": {
            "network_id": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
        },
        "name": "another_router",
        "admin_state_up": True,
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "id": "8604a0de-7f6b-409a-a47c-a1cc7bc77b2e"
    }
}

ROUTER_CREATED = {
    "router": {
        "status": "ACTIVE",
        "external_gateway_info": {
            "network_id": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
        },
        "name": "another_router",
        "admin_state_up": True,
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "id": "8604a0de-7f6b-409a-a47c-a1cc7bc77b2f"
    }
}

ROUTER_ADD_INTERFACE2 = {
    'id': '8604a0de-7f6b-409a-a47c-a1cc7bc77b2f',
    'interface': {
        "subnet_id": "3b80198d-4f7b-4f77-9ef5-774d54e17126",
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "port_id": "d8a4cc85-ad78-46ac-b5a1-8e04f16fa51f",
        "id": "8604a0de-7f6b-409a-a47c-a1cc7bc77b2f"
    }
}


def change_id(router, count):
    id = router['router']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    router['router']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return router


class Router(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_router(self, routerid):
        logging.info('get router: ' + routerid)
        return self.get(config.NEUTRON_ROUTERS + '/' + routerid)

    def get_routers(self):
        logging.info('get routers')
        return self.get(config.NEUTRON_ROUTERS)

    def create_router(self, payload):
        logging.info('create router: ' + payload['router']['id'])
        return self.post(config.NEUTRON_ROUTERS, payload)

    def update_router(self, routerid, payload):
        logging.info('update router: ' + routerid)
        return self.put(config.NEUTRON_ROUTERS + '/' + routerid, payload)

    def delete_router(self, routerid):
        logging.info('delete router: ' + routerid)
        return self.delete(config.NEUTRON_ROUTERS + '/' + routerid)

    def add_interface(self, routerid, payload):
        logging.info('add interface for router: ' + routerid)
        return self.put(config.NEUTRON_ROUTERS + '/' + routerid + '/add_router_interface', payload)

    def remove_interface(self, routerid, payload):
        logging.info('remove interface for router: ' + routerid)
        return self.put(config.NEUTRON_ROUTERS + '/' + routerid + '/remove_router_interface', payload)

    @staticmethod
    def perform_tests(servername, username, count):
        tester = Router(servername, username)

        router_one = tester.create_router(change_id(ROUTER_ONE, count))
        utils.assert_status(router_one, 201)

        router_one_id = json.loads(router_one.text)['router']['id']
        utils.assert_status(tester.get_router(router_one_id), 200)

        if count == 0:
            utils.assert_status(tester.add_interface(ROUTER_ADD_INTERFACE['id'], ROUTER_ADD_INTERFACE['interface']),
                                200)
            utils.assert_status(tester.add_interface(ROUTER_ADD_INTERFACE2['id'], ROUTER_ADD_INTERFACE2['interface']),
                                200)
            utils.assert_status(tester.remove_interface(ROUTER_ADD_INTERFACE2['id'], ROUTER_ADD_INTERFACE2['interface'])
                                , 200)

        utils.assert_status(tester.update_router(change_id(ROUTER_UPDATE, count)['router']['id'],
                                                 change_id(ROUTER_UPDATE, count)), 200)

        utils.assert_status(tester.create_router(change_id(ROUTER_CREATED, count)), 201)

        utils.assert_status(tester.get_router(change_id(ROUTER_CREATED, count)['router']['id']), 200)

        utils.assert_status(tester.delete_router(change_id(ROUTER_CREATED, count)['router']['id']), 204)

        utils.assert_status(tester.get_router(change_id(ROUTER_CREATED, count)['router']['id']), 404)

        routers = tester.get_routers()
        for r in json.loads(routers.text)['routers']:
            utils.assert_status(tester.delete_router(r['id']), 204)


if __name__ == '__main__':
    Router.perform_tests('server', 'admin', 0)
