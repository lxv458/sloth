import logging

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
from scripts.tests.securitygroup import SecurityGroup
from scripts.tests.securitygrouprule import SecurityGroupRule
from scripts.tests.sfcflowclassifier import SFCFlowClassifier
from scripts.tests.sfcportchain import SFCPortChain
from scripts.tests.sfcportpair import SFCPortPair
from scripts.tests.sfcportpairgroup import SFCPortPairGroup

if __name__ == '__main__':
    logging_config = utils.get_logging_config('logging')
    logging.basicConfig(filename=logging_config['filename'], level=logging_config['level'])
    Network.perform_tests('server', 'admin')
    Router.perform_tests('server', 'admin')
    Subnet.perform_tests('server', 'admin')
    Port.perform_tests('server', 'admin')
    Trunk.perform_tests('server', 'admin')
    Bgpvpn.perform_tests('server', 'admin')
    Firewall.perform_tests('server', 'admin')
    FirewallPolicy.perform_tests('server', 'admin')
    FirewallRule.perform_tests('server', 'admin')
    #FloatingIP.perform_tests('server', 'admin')
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
    SecurityGroup.perform_tests('server', 'admin')
    SecurityGroupRule.perform_tests('server', 'admin')
    SFCFlowClassifier.perform_tests('server', 'admin')
    SFCPortChain.perform_tests('server', 'admin')
    SFCPortPair.perform_tests('server', 'admin')
    SFCPortPairGroup.perform_tests('server', 'admin')
