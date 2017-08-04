import logging
import latency
import time
import os

from scripts import utils
from scripts.tests.network import Network
from scripts.tests.router import Router
from scripts.tests.subnet import Subnet
from scripts.tests.port import Port
from scripts.tests.trunk import Trunk
from scripts.tests.bgpvpn import Bgpvpn
from scripts.tests.firewall import Firewall
from scripts.tests.firewallpolicy import FirewallPolicy
from scripts.tests.firewallrule import FirewallRule
from scripts.tests.floatingip import FloatingIP
from scripts.tests.gateway import Gateway
from scripts.tests.gatewayconnection import GatewayConnection
from scripts.tests.loadbalancer import Loadbalancer
from scripts.tests.loadbalancerhealthmonitor import LoadbalancerHealthMonitor
from scripts.tests.loadbalancerlistener import LoadbalancerListener
from scripts.tests.loadbalancerpool import LoadbalancerPool
from scripts.tests.meteringlabel import MeteringLabel
from scripts.tests.meteringrule import MeteringLabelRule
from scripts.tests.qospolicy import QosPolicy
from scripts.tests.vpnservice import VpnService
# from scripts.tests.securitygroup import SecurityGroup
from scripts.tests.securitygrouprule import SecurityGroupRule
from scripts.tests.sfcflowclassifier import SFCFlowClassifier
from scripts.tests.sfcportchain import SFCPortChain
from scripts.tests.sfcportpair import SFCPortPair
from scripts.tests.sfcportpairgroup import SFCPortPairGroup

if __name__ == '__main__':

    logging_config = utils.get_logging_config('logging')
    filename = logging_config['filename']

    if os.path.exists(filename):
        os.remove(filename)

    logging.basicConfig(filename=filename, level=logging_config['level'])

    for i in range(5):
        print('Test Round ' + str(i) + ' ' + time.strftime('%Y-%m-%d', time.localtime(time.time())))
        logging.info('Test Round ' + str(i) + ' ' + time.strftime('%Y-%m-%d', time.localtime(time.time())))

        Network.perform_tests('server', 'admin')
        Router.perform_tests('server', 'Lily')
        Subnet.perform_tests('server', 'Tom')
        Port.perform_tests('server', 'Tom')
        Trunk.perform_tests('server', 'Gary')
        Bgpvpn.perform_tests('server', 'Gary')
        Firewall.perform_tests('server', 'Tom')
        FirewallPolicy.perform_tests('server', 'Tom')
        FirewallRule.perform_tests('server', 'Tom')
        FloatingIP.perform_tests('server', 'Gary')
        Gateway.perform_tests('server', 'admin')
        GatewayConnection.perform_tests('server', 'admin')
        Loadbalancer.perform_tests('server', 'Gary')
        LoadbalancerHealthMonitor.perform_tests('server', 'Tom')
        LoadbalancerListener.perform_tests('server', 'Jack')
        LoadbalancerPool.perform_tests('server', 'admin')
        MeteringLabel.perform_tests('server', 'Gary')
        MeteringLabelRule.perform_tests('server', 'Tom')
        QosPolicy.perform_tests('server', 'Tom')
        VpnService.perform_tests('server', 'admin')
        # SecurityGroup.perform_tests('server', 'admin')
        SecurityGroupRule.perform_tests('server', 'Gary')
        SFCFlowClassifier.perform_tests('server', 'admin')
        SFCPortChain.perform_tests('server', 'admin')
        SFCPortPair.perform_tests('server', 'admin')
        SFCPortPairGroup.perform_tests('server', 'admin')
        latency.latency_data_transform(filename, 'Latency_neutron_5_8-3')


