import threading
import logging
import time
import utils
import os

from tests.network import Network
from tests.network import NETWORK_ONE
from tests.router import Router
from tests.subnet import Subnet
from tests.port import Port
from tests.trunk import Trunk
from tests.bgpvpn import Bgpvpn
from tests.firewall import Firewall
from tests.firewallpolicy import FirewallPolicy
from tests.firewallrule import FirewallRule
from tests.floatingip import FloatingIP
from tests.gateway import Gateway
from tests.gatewayconnection import GatewayConnection
from tests.loadbalancer import Loadbalancer
from tests.loadbalancerhealthmonitor import LoadbalancerHealthMonitor
from tests.loadbalancerlistener import LoadbalancerListener
from tests.loadbalancerpool import LoadbalancerPool
from tests.meteringlabel import MeteringLabel
from tests.meteringrule import MeteringLabelRule
from tests.qospolicy import QosPolicy
from tests.vpnservice import VpnService
# from tests.securitygroup import SecurityGroup
from tests.securitygrouprule import SecurityGroupRule
from tests.sfcflowclassifier import SFCFlowClassifier
from tests.sfcportchain import SFCPortChain
from tests.sfcportpair import SFCPortPair
from tests.sfcportpairgroup import SFCPortPairGroup

lock = threading.Lock()
count_get = 0
count_post = 0
count_delete = 0


def send_post_request(tester, payload):
    tester.create_network(payload)


def send_get_request(tester):
    tester.get_networks()


def send_put_request(tester, netid, payload):
    tester.update_network(netid, payload)


def send_delete_request(tester, netid):
    tester.delete_network(netid)


def test_get(network_tester, num):
    global count_get
    for i in range(1, num):
        logging.info('i_get = %d' % i)
        if lock.acquire():
            send_get_request(network_tester)
            count_get += 1
            logging.info('count_get = %d' % count_get)
            lock.release()


def test_post(network_tester, num):
    global count_post
    for i in range(1, num):
        logging.info('i_post = %d' % i)
        if lock.acquire():
            send_post_request(network_tester, NETWORK_ONE)
            count_post += 1
            logging.info('count_post = %d' % count_post)
            lock.release()


def test_delete(network_tester, num):
    global count_delete
    for i in range(1, num):
        logging.info('i_delete = %d' % i)
        if lock.acquire():
            send_delete_request(network_tester, NETWORK_ONE['network']['id'])
            count_delete += 1
            logging.info('count_delete = %d' % count_delete)
            lock.release()


def throughput_get_test():
    log_config()
    network_tester = Network.throughput_test('server', 'admin')
    send_post_request(network_tester, NETWORK_ONE)
    start_time = time.time()
    logging.info('start_time: %f' % start_time)
    task = []
    for i in range(10):
        task.append(threading.Thread(target=test_get, args=(network_tester, 81)))
    for t in task:
        t.start()
    for t in task:
        t.join()
    end_time = time.time()
    logging.info('end_time: %f' % end_time)
    logging.info('cost time: %f ms' % ((end_time - start_time) * 1000))
    logging.info('Successfully!')


def throughput_post_test():
    log_config()
    network_tester = Network.throughput_test('server', 'admin')
    start_time = time.time()
    logging.info('start_time: %f' % start_time)
    task = []
    for i in range(10):
        task.append(threading.Thread(target=test_post, args=(network_tester, 81)))
    for t in task:
        t.start()
    for t in task:
        t.join()
    end_time = time.time()
    logging.info('end_time: %f' % end_time)
    logging.info('cost time: %f ms' % ((end_time - start_time) * 1000))
    logging.info('Successfully!')


def throughput_put_test():
    log_config()
    logging.info('Successfully!')


def throughput_delete_test():
    log_config()
    network_tester = Network.throughput_test('server', 'admin')
    start_time = time.time()
    logging.info('start_time: %f' % start_time)
    task = []
    for i in range(10):
        task.append(threading.Thread(target=test_delete, args=(network_tester, 81)))
    for t in task:
        t.start()
    for t in task:
        t.join()
    end_time = time.time()
    logging.info('end_time: %f' % end_time)
    logging.info('cost time: %f ms' % ((end_time - start_time) * 1000))
    logging.info('Successfully!')


def test_multiple(thread_num):
    total_round = 64
    time_round = int(total_round / thread_num)

    for i in range(time_round):
        Network.perform_tests('server', 'admin')
        Router.perform_tests('server', 'admin')
        Subnet.perform_tests('server', 'admin')
        Port.perform_tests('server', 'admin')
        # Trunk.perform_tests('server', 'admin')
        Bgpvpn.perform_tests('server', 'admin')
        Firewall.perform_tests('server', 'admin')
        FirewallPolicy.perform_tests('server', 'admin')
        FirewallRule.perform_tests('server', 'admin')
        FloatingIP.perform_tests('server', 'admin')
        Gateway.perform_tests('server', 'admin')
        GatewayConnection.perform_tests('server', 'admin')
        Loadbalancer.perform_tests('server', 'admin')
        LoadbalancerHealthMonitor.perform_tests('server', 'admin')
        LoadbalancerListener.perform_tests('server', 'admin')
        LoadbalancerPool.perform_tests('server', 'admin')
        MeteringLabel.perform_tests('server', 'admin')
        MeteringLabelRule.perform_tests('server', 'admin')
        QosPolicy.perform_tests('server', 'admin')
        VpnService.perform_tests('server', 'admin')
        # SecurityGroup.perform_tests('server', 'admin')
        SecurityGroupRule.perform_tests('server', 'admin')
        SFCFlowClassifier.perform_tests('server', 'admin')
        SFCPortChain.perform_tests('server', 'admin')
        SFCPortPair.perform_tests('server', 'admin')
        SFCPortPairGroup.perform_tests('server', 'admin')


def test_API(API, num):
    for i in range(num):
        API.perform_tests('server', 'admin')


def throughput_mix():
    # log_config()
    task = []
    task.append(threading.Thread(target=test_API, args=(Network, 8)))
    task.append(threading.Thread(target=test_API, args=(Router, 8)))
    task.append(threading.Thread(target=test_API, args=(Subnet, 8)))
    task.append(threading.Thread(target=test_API, args=(Port, 8)))
    task.append(threading.Thread(target=test_API, args=(Trunk, 8)))
    task.append(threading.Thread(target=test_API, args=(Bgpvpn, 8)))
    task.append(threading.Thread(target=test_API, args=(Firewall, 8)))
    task.append(threading.Thread(target=test_API, args=(FirewallPolicy, 8)))
    task.append(threading.Thread(target=test_API, args=(FirewallRule, 8)))
    task.append(threading.Thread(target=test_API, args=(FloatingIP, 8)))
    task.append(threading.Thread(target=test_API, args=(Gateway, 8)))
    task.append(threading.Thread(target=test_API, args=(GatewayConnection, 8)))
    task.append(threading.Thread(target=test_API, args=(Loadbalancer, 8)))
    task.append(threading.Thread(target=test_API, args=(LoadbalancerHealthMonitor, 8)))
    task.append(threading.Thread(target=test_API, args=(LoadbalancerListener, 8)))
    task.append(threading.Thread(target=test_API, args=(LoadbalancerPool, 8)))
    task.append(threading.Thread(target=test_API, args=(MeteringLabel, 8)))
    task.append(threading.Thread(target=test_API, args=(MeteringLabelRule, 8)))
    task.append(threading.Thread(target=test_API, args=(QosPolicy, 8)))
    task.append(threading.Thread(target=test_API, args=(VpnService, 8)))
    # task.append(threading.Thread(target=test_API, args=(SecurityGroup, 8)))
    task.append(threading.Thread(target=test_API, args=(SecurityGroupRule, 8)))
    task.append(threading.Thread(target=test_API, args=(SFCFlowClassifier, 8)))
    task.append(threading.Thread(target=test_API, args=(SFCPortChain, 8)))
    task.append(threading.Thread(target=test_API, args=(SFCPortPair, 8)))
    task.append(threading.Thread(target=test_API, args=(SFCPortPairGroup, 8)))
    for t in task:
        t.setDaemon(True)
    for t in task:
        t.start()


if __name__ == '__main__':
    throughput_mix()

