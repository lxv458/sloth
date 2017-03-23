import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

METERING_LABEL_ONE = {
    "metering_label": {
        "id": "bc91b832-8465-40a7-a5d8-ba87de442266",
        "tenant_id": "45345b0ee1ea477fac0f541b2cb79cd4",
        "description": "description of label1",
        "name": "label1"
    }
}

class Metering_label(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_metering_label(self, metering_labelid):
        logging.info('get metering_label: ' + metering_labelid)
        return self.get(config.NEUTRON_METERING_LABELS + '/' + metering_labelid)

    def get_metering_labels(self):
        logging.info('get all metering_labels')
        return self.get(config.NEUTRON_METERING_LABELS)

    def create_metering_label(self, payload):
        logging.info('create metering_label: ' + payload['metering_label']['id'])
        return self.post(config.NEUTRON_METERING_LABELS, payload)

    def delete_metering_label(self, metering_labelid):
        logging.info('delete metering_label: ' + metering_labelid)
        return self.delete(config.NEUTRON_METERING_LABELS + '/' + metering_labelid)

    @staticmethod
    def perform_tests(servername, username):
        logging.info('perform metering_label tests, server: %s, user: %s' % (servername, username))

        tester = Metering_label(servername, username)

        utils.assert_status(tester.get_metering_labels(), 200)

        metering_label_one = tester.create_metering_label(METERING_LABEL_ONE)
        utils.assert_status(metering_label_one, 201)

        metering_label_one_id = json.loads(metering_label_one.text)['metering_label']['id']

        utils.assert_status(tester.get_metering_label(metering_label_one_id), 200)

        utils.assert_status(tester.delete_metering_label(metering_label_one_id), 204)

        utils.assert_status(tester.get_metering_label(metering_label_one_id), 404)

