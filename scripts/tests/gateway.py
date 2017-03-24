import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

GATEWAY_ONE = {
    "l2_gateway": {
        "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
        "name": "gateway1",
        "devices": [
            {
                "interfaces": [
                    {
                        "segmentation_id": [
                            100
                        ],
                        "name": "interface1"
                    }
                ],
                "id": "0a24b09a-88a1-4f2c-94e9-92515972a704",
                "device_name": "device1"
            }
        ],
        "id": "3b0ef8f4-82c7-44d4-a4fb-6177f9a21977"
    }
}

GATEWAY_UPDATE = {
    "id": "3b0ef8f4-82c7-44d4-a4fb-6177f9a21977",
    "l2_gateway": {
        "l2_gateway": {
            "tenant_id": "45977fa2dbd7482098dd68d0d8970117",
            "name": "gateway1",
            "devices": [
                {
                    "interfaces": [
                        {
                            "segmentation_id": [
                                100,
                                50
                            ],
                            "name": "interface1"
                        }
                    ],
                    "id": "0a24b09a-88a1-4f2c-94e9-92515972a704",
                    "device_name": "device1"
                }
            ],
            "id": "3b0ef8f4-82c7-44d4-a4fb-6177f9a21977"
        }
    }
}


class Gateway(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_gateway(self, gatewayid):
        logging.info('get gateway: ' + gatewayid)
        return self.get(config.NEUTRON_L2_GATEWAYS + '/' + gatewayid)

    def get_gateways(self):
        logging.info('get all gateways')
        return self.get(config.NEUTRON_L2_GATEWAYS)

    def create_gateway(self, payload):
        logging.info('create gateway: ' + payload['l2_gateway']['id'])
        return self.post(config.NEUTRON_L2_GATEWAYS, payload)

    def update_gateway(self, gatewayid, payload):
        logging.info('update gateway: ' + gatewayid)
        return self.put(config.NEUTRON_L2_GATEWAYS + '/' + gatewayid, payload)

    def delete_gateway(self, gatewayid):
        logging.info('delete gateway: ' + gatewayid)
        return self.delete(config.NEUTRON_L2_GATEWAYS + '/' + gatewayid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform gateway tests, server: %s, user: %s' % (servername, username))

        tester = Gateway(servername, username)

        utils.assert_status(tester.get_gateways(), 200)

        gateway_one = tester.create_gateway(GATEWAY_ONE)
        utils.assert_status(gateway_one, 201)

        gateway_one_id = json.loads(gateway_one.text)['l2_gateway']['id']

        utils.assert_status(tester.get_gateway(gateway_one_id), 200)

        utils.assert_status(tester.update_gateway(GATEWAY_UPDATE['id'], GATEWAY_UPDATE['l2_gateway']), 200)

        utils.assert_status(tester.delete_gateway(gateway_one_id), 204)

        utils.assert_status(tester.get_gateway(gateway_one_id), 404)
