import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

NETWORK_ONE = {
    "network": {
        "status": "ACTIVE",
        "subnets": [],
        "name": "net1",
        "router:external": False,
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "segments": [
            {
                "provider:network_type": "vlan",
                "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                "provider:segmentation_id": 2
            },
            {
                "provider:network_type": "stt",
                "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                "provider:segmentation_id": None
            }
        ],
        "admin_state_up": True,
        "shared": False,
        "id": "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
    }
}

NETWORK_DEFAULT = {
    "network": {
        "subnets": [],
        "name": "netdefault",
        "router:external": False,
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "segments": [
            {
                "provider:network_type": "vlan",
                "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                "provider:segmentation_id": 2
            },
            {
                "provider:network_type": "stt",
                "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                "provider:segmentation_id": None
            }
        ],
        "id": "de8e5957-d49f-d77b-de5b-d1f75b21c03c"
    }
}

NETWORK_EXTERNAL = {
    "network": {
        "status": "ACTIVE",
        "subnets": [],
        "name": "external1",
        "router:external": True,
        "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
        "admin_state_up": True,
        "shared": False,
        "id": "8ca37218-28ff-41cb-9b10-039601ea7e6b"
    }
}

NETWORKS_BULK = {
    "networks": [
        {
            "status": "ACTIVE",
            "subnets": [],
            "name": "sample_network3",
            "provider:physical_network": None,
            "admin_state_up": True,
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
            "provider:network_type": "local",
            "shared": False,
            "id": "bc1a76cb-8767-4c3a-bb95-018b822f2130",
            "provider:segmentation_id": None
        },
        {
            "status": "ACTIVE",
            "subnets": [],
            "name": "sample_network4",
            "provider:physical_network": None,
            "admin_state_up": True,
            "tenant_id": "4fd44f30292945e481c7b8a0c8908869",
            "provider:network_type": "local",
            "shared": False,
            "id": "af374017-c9ae-4a1d-b799-ab73111476e2",
            "provider:segmentation_id": None
        }
    ]
}

NETWORK_UPDATE = {
    'network': {
        "network": {
            'id': '4e8e5957-649f-477b-9e5b-f1f75b21c03c',
            "status": "ACTIVE",
            "subnets": [],
            "name": "net_update",
            "router:external": False,
            "tenant_id": "9bacb3c5d39d41a79512987f338cf177",
            "segments": [
                {
                    "provider:network_type": "vlan",
                    "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                    "provider:segmentation_id": 2
                },
                {
                    "provider:network_type": "stt",
                    "provider:physical_network": "8bab8453-1bc9-45af-8c70-f83aa9b50453",
                    "provider:segmentation_id": None
                }
            ],
            "admin_state_up": True,
            "shared": False
        }
    }
}


def change_id(network, count):
    id = network['network']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    network['network']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return network


class Network(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_network(self, networkid):
        logging.info('get network: ' + networkid)
        return self.get(config.NEUTRON_NETWORKS + '/' + networkid)

    def get_networks(self):
        logging.info('get all networks')
        return self.get(config.NEUTRON_NETWORKS)

    def create_network(self, payload):
        if 'network' in payload:
            logging.info('create network: ' + payload['network']['id'])
        else:
            logging.info('bulk create networks: ' + ', '.join([net['id'] for net in payload['networks']]))
        return self.post(config.NEUTRON_NETWORKS, payload)

    def update_network(self, networkid, payload):
        logging.info('update network: ' + networkid)
        return self.put(config.NEUTRON_NETWORKS + '/' + networkid, payload)

    def delete_network(self, networkid):
        logging.info('delete network: ' + networkid)
        return self.delete(config.NEUTRON_NETWORKS + '/' + networkid)

    @staticmethod
    def throughput_test(servername, username):
        logging.info('perform throughput test, server: %s, user: %s' % (servername, username))
        tester = Network(servername, username)
        return tester

    @staticmethod
    def perform_tests(servername, username, count):
        logging.info('perform network tests, server: %s, user: %s' % (servername, username))

        tester = Network(servername, username)

        utils.assert_status(tester.get_networks(), 200)

        network_one = tester.create_network(change_id(NETWORK_ONE, count))
        utils.assert_status(network_one, 201)

        network_one_id = json.loads(network_one.text)['network']['id']

        utils.assert_status(tester.get_network(network_one_id), 200)

        utils.assert_status(tester.create_network(change_id(NETWORK_DEFAULT, count)), 201)

        utils.assert_status(tester.update_network(change_id(NETWORK_UPDATE['network'], count)['network']['id'],
                                                  change_id(NETWORK_UPDATE['network'], count)), 200)

        if count == 0:
            # utils.assert_status(tester.create_network(change_id(NETWORK_EXTERNAL, count)), 201)
            utils.assert_status(tester.create_network(NETWORKS_BULK), 201)
            utils.assert_status(tester.delete_network(NETWORKS_BULK['networks'][0]['id']), 204)
            utils.assert_status(tester.get_network(NETWORKS_BULK['networks'][0]['id']), 404)

        networks = tester.get_networks()

        for net in json.loads(networks.text)['networks']:
            utils.assert_status(tester.delete_network(net['id']), 204)


if __name__ == '__main__':
    Network.perform_tests('server', 'admin', 0)
