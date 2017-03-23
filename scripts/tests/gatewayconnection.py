import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

GATEWAY_CONNECTION_ONE = {
    "l2gateway_connection": {
        "port_id": "9ea656c7-c9b8-4474-94f3-3b0bc741d9a9",
        "gateway_id": "d3590f37-b072-4358-9719-71964d84a31c",
        "segmentation_id": 100,
        "network_id": "c69933c1-b472-44f9-8226-30dc4ffd454c",
        "id": "3b0ef8f4-82c7-44d4-a4fb-6177f9a21977",
        "tenant_id": "45977fa2dbd7482098dd68d0d8970117"
    }
}

GATEWAY_CONNECTION_TWO = {
    "l2gateway_connection": {
        "gateway_id": "5227c228-6bba-4bbe-bdb8-6942768ff0f1",
        "segmentation_id": 100,
        "network_id": "9227c228-6bba-4bbe-bdb8-6942768ff0f1",
        "id": "5227c228-6bba-4bbe-bdb8-6942768ff0e1",
        "tenant_id": "de0a7495-05c4-4be0-b796-1412835c6820"
    }
}

class Gateway_Connection(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_gateway_connection(self, gateway_connectionid):
        logging.info('get gateway_connection: ' + gateway_connectionid)
        return self.get(config.NEUTRON_L2_GATEWAY_CONNECTIONS + '/' + gateway_connectionid)

    def get_gateway_connections(self):
        logging.info('get all gateway_connections')
        return self.get(config.NEUTRON_L2_GATEWAY_CONNECTIONS)

    def create_gateway_connection(self, payload):
        logging.info('create gateway_connection: ' + payload['l2gateway_connection']['id'])
        return self.post(config.NEUTRON_L2_GATEWAY_CONNECTIONS, payload)

    def delete_gateway_connection(self, gateway_connectionid):
        logging.info('delete gateway_connection: ' + gateway_connectionid)
        return self.delete(config.NEUTRON_L2_GATEWAY_CONNECTIONS + '/' + gateway_connectionid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform gateway_connection tests, server: %s, user: %s' % (servername, username))

        tester = Gateway_Connection(servername, username)

        utils.assert_status(tester.get_gateway_connections(), 200)

        gateway_connection_one = tester.create_gateway_connection(GATEWAY_CONNECTION_ONE)
        utils.assert_status(gateway_connection_one, 201)

        gateway_connection_one_id = json.loads(gateway_connection_one.text)['l2gateway_connection']['id']

        utils.assert_status(tester.get_gateway_connection(gateway_connection_one_id), 200)

        gateway_connection_two = tester.create_gateway_connection(GATEWAY_CONNECTION_TWO)
        utils.assert_status(gateway_connection_two, 201)

        gateway_connection_two_id = json.loads(gateway_connection_two.text)['l2gateway_connection']['id']

        utils.assert_status(tester.get_gateway_connection(gateway_connection_two_id), 200)

        utils.assert_status(tester.delete_gateway_connection(gateway_connection_one_id), 204)

        utils.assert_status(tester.get_gateway_connection(gateway_connection_one_id), 404)

        utils.assert_status(tester.delete_gateway_connection(gateway_connection_two_id), 204)

        utils.assert_status(tester.get_gateway_connection(gateway_connection_two_id), 404)