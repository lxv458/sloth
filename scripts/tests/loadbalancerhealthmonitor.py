import json
import logging

from scripts import config
from scripts import utils
from scripts.httpapi import HttpAPI

LOAD_BALANCER_HEALTH_MONITOR_ONE = {
    "healthmonitor": {
        "admin_state_up": True,
        "delay": 1,
        "expected_codes": "200,201,202",
        "http_method": "GET",
        "id": "0a9ac99d-0a09-4b18-8499-a0796850279a",
        "max_retries": 5,
        "pools": [
            {
                "id": "74aa2010-a59f-4d35-a436-60a6da882819"
            }
        ],
        "tenant_id": "6f3584d5754048a18e30685362b88411",
        "timeout": 1,
        "type": "HTTP",
        "url_path": "/index.html"
    }
}

LOAD_BALANCER_HEALTH_MONITOR_UPDATE = {
    "id": "0a9ac99d-0a09-4b18-8499-a0796850279a",
    "healthmonitor": {
        "healthmonitor": {
            "admin_state_up": False,
            "delay": 2,
            "expected_codes": "200",
            "http_method": "POST",
            "id": "0a9ac99d-0a09-4b18-8499-a0796850279a",
            "max_retries": 2,
            "pools": [
                {
                    "id": "74aa2010-a59f-4d35-a436-60a6da882819"
                }
            ],
            "tenant_id": "6f3584d5754048a18e30685362b88411",
            "timeout": 2,
            "type": "HTTP",
            "url_path": "/page.html"
        }
    }
}


def change_id(healthmonitor, count):
    id = healthmonitor['healthmonitor']['id']
    l = id.split('-')
    tmp = int(l[4], 16) + count
    tmp_id = str(hex(tmp))[2:]
    healthmonitor['healthmonitor']['id'] = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    return healthmonitor


class LoadbalancerHealthMonitor(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_loadbalancer_health_monitor(self, loadbalancer_health_monitorid):
        logging.info('get loadbalancer_health_monitor: ' + loadbalancer_health_monitorid)
        return self.get(config.NEUTRON_LOAD_BALANCER_HEALTH_MONITORS + '/' + loadbalancer_health_monitorid)

    def get_loadbalancer_health_monitors(self):
        logging.info('get all loadbalancer_health_monitors')
        return self.get(config.NEUTRON_LOAD_BALANCER_HEALTH_MONITORS)

    def create_loadbalancer_health_monitor(self, payload):
        logging.info('create loadbalancer_health_monitor: ' + payload['healthmonitor']['id'])
        return self.post(config.NEUTRON_LOAD_BALANCER_HEALTH_MONITORS, payload)

    def update_loadbalancer_health_monitor(self, loadbalancer_health_monitorid, payload):
        logging.info('update loadbalancer_health_monitor: ' + loadbalancer_health_monitorid)
        return self.put(config.NEUTRON_LOAD_BALANCER_HEALTH_MONITORS + '/' + loadbalancer_health_monitorid, payload)

    def delete_loadbalancer_health_monitor(self, loadbalancer_health_monitorid):
        logging.info('delete loadbalancer_health_monitor: ' + loadbalancer_health_monitorid)
        return self.delete(config.NEUTRON_LOAD_BALANCER_HEALTH_MONITORS + '/' + loadbalancer_health_monitorid)

    @staticmethod
    def perform_tests(servername, username, count=0):
        logging.info('perform loadbalancer_health_monitor tests, server: %s, user: %s' % (servername, username))

        tester = LoadbalancerHealthMonitor(servername, username)

        utils.assert_status(tester.get_loadbalancer_health_monitors(), 200)

        loadbalancer_health_monitor_one = tester.create_loadbalancer_health_monitor(
            change_id(LOAD_BALANCER_HEALTH_MONITOR_ONE, count))
        utils.assert_status(loadbalancer_health_monitor_one, 201)

        loadbalancer_health_monitor_one_id = json.loads(loadbalancer_health_monitor_one.text)['healthmonitor']['id']

        utils.assert_status(tester.get_loadbalancer_health_monitor(loadbalancer_health_monitor_one_id), 200)

        utils.assert_status(tester.update_loadbalancer_health_monitor(
            change_id(LOAD_BALANCER_HEALTH_MONITOR_UPDATE['healthmonitor'], count)['healthmonitor']['id'],
            change_id(LOAD_BALANCER_HEALTH_MONITOR_UPDATE['healthmonitor'], count)), 200)

        utils.assert_status(tester.delete_loadbalancer_health_monitor(loadbalancer_health_monitor_one_id), 204)

        utils.assert_status(tester.get_loadbalancer_health_monitor(loadbalancer_health_monitor_one_id), 404)


if __name__ == '__main__':
    LoadbalancerHealthMonitor.perform_tests('server', 'admin')
