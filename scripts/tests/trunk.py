import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

TRUNK_ONE = {
        "trunk": {
            "status": "DOWN",
            "name": "trunk0",
            "admin_state_up": True,
            "tenant_id": "cc3641789c8a4304abaa841c64f638d9",
            "port_id": "60aac28d-1d3a-48d9-99bc-dd4bd62e50f2",
            "sub_ports": [
                {
                    "segmentation_type": "vlan",
                    "port_id": "dca33436-2a7c-415b-aa35-14769e7834e3",
                    "segmentation_id": 101
                },
                {
                    "segmentation_type": "vlan",
                    "port_id": "be28febe-bdff-45cc-8a2d-872d54e62527",
                    "segmentation_id": 102
                }
            ],
            "id": "c935240e-4aa6-496a-841c-d113c54499b9",
            "description": "test trunk0"
        }
    }

TRUNK_DEFAULT = {
        "trunk": {
            "name": "trunkdefault",
            "tenant_id": "cc3641789c8a4304abaa841c64f638d9",
            "port_id": "60aac28d-1d3a-48d9-99bc-dd4bd62e50f2",
            "sub_ports": [
                {
                    "segmentation_type": "vlan",
                    "port_id": "dca33436-2a7c-415b-aa35-14769e7834e3",
                    "segmentation_id": 101
                },
                {
                    "segmentation_type": "vlan",
                    "port_id": "be28febe-bdff-45cc-8a2d-872d54e62527",
                    "segmentation_id": 102
                }
            ],
            "id": "d935240e-4aa6-d96a-d41c-d113c54499b9",
            "description": "test trunkdefault"
        }
    }

TRUNKS_BULK = {
    "trunks": [
        {
            "status": "DOWN",
            "name": "trunk1",
            "admin_state_up": True,
            "tenant_id": "cc3641789c8a4304abaa841c64f638d9",
            "port_id": "87927a7a-86ec-4062-946f-40222ec583ca",
            "sub_ports": [
                {
                    "segmentation_type": "vlan",
                    "port_id": "75e366aa-51b6-4ec8-9695-739c465377f7",
                    "segmentation_id": 101
                },
                {
                    "segmentation_type": "vlan",
                    "port_id": "e12f8356-ff66-4948-979f-9dedb63ee299",
                    "segmentation_id": 102
                }
            ],
            "id": "bc587c4c-de31-42b1-89c3-809add88c9b3",
            "description": "test trunk1"
        },
        {
            "status": "ACTIVE",
            "name": "trunk2",
            "admin_state_up": True,
            "tenant_id": "cc3641789c8a4304abaa841c64f638d9",
            "port_id": "f5624c68-eda2-42c1-92a1-53094707dc36",
            "sub_ports": [
                {
                    "segmentation_type": "vlan",
                    "port_id": "2a4897de-d5ba-4bd5-8998-4f86e083e3fd",
                    "segmentation_id": 101
                },
                {
                    "segmentation_type": "vlan",
                    "port_id": "9dedb63e-ff66-4948-979f-e12f8356e299",
                    "segmentation_id": 102
                }
            ],
            "id": "5e97b0a4-b5a3-49fd-b0cb-821bec16acfe",
            "description": "test trunk2"
        }
    ]
}

TRUNK_UPDATE = {
        "trunk": {
            "status": "DOWN",
            "name": "trunk0",
            "admin_state_up": True,
            "port_id": "60aac28d-1d3a-48d9-99bc-dd4bd62e50f2",
            "sub_ports": [
                {
                    "segmentation_type": "vlan",
                    "port_id": "dca33436-2a7c-415b-aa35-14769e7834e3",
                    "segmentation_id": 101
                }
            ],
            "id": "c935240e-4aa6-496a-841c-d113c54499b9",
            "description": "test trunk0 updated"
        }
    }

class Trunk(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_trunk(self, trunkid):
        logging.info('get trunk: ' + trunkid)
        return self.get(config.NEUTRON_TRUNKS + '/' + trunkid)

    def get_trunks(self):
        logging.info('get all trunks')
        return self.get(config.NEUTRON_TRUNKS)

    def create_trunk(self, payload):
        if 'trunk' in payload:
            logging.info('create trunk: ' + payload['trunk']['id'])
        else:
            logging.info('bulk create trunks: ' + ', '.join([net['id'] for net in payload['trunks']]))
        return self.post(config.NEUTRON_TRUNKS, payload)

    def update_trunk(self, trunkid, payload):
        logging.info('update trunk: ' + trunkid)
        return self.put(config.NEUTRON_TRUNKS + '/' + trunkid, payload)

    def delete_trunk(self, trunkid):
        logging.info('delete trunk: ' + trunkid)
        return self.delete(config.NEUTRON_TRUNKS + '/' + trunkid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform trunk tests, server: %s, user: %s' % (servername, username))

        tester = Trunk(servername, username)

        utils.assert_status(tester.get_trunks(), 200)

        trunk_one = tester.create_trunk(TRUNK_ONE)
        utils.assert_status(trunk_one, 201)

        trunk_one_id = json.loads(trunk_one.text)['trunk']['id']

        utils.assert_status(tester.get_trunk(trunk_one_id), 200)

        utils.assert_status(tester.create_trunk(TRUNK_DEFAULT), 201)

        utils.assert_status(tester.create_trunk(TRUNKS_BULK), 201)

        utils.assert_status(tester.update_trunk(TRUNK_UPDATE['id'], TRUNK_UPDATE['trunk']), 200)

        utils.assert_status(tester.delete_trunk(TRUNKS_BULK['trunks'][0]['id']), 204)

        utils.assert_status(tester.get_trunk(TRUNKS_BULK['trunks'][0]['id']), 404)

        trunks = tester.get_trunks()

        for trunk in json.loads(trunks.text)['trunks']:
            utils.assert_status(tester.delete_trunk(trunk['id']), 204)
