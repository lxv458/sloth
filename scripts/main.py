import logging
import latency

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
    logging.basicConfig(filename=logging_config['filename'], level=logging_config['level'])
    Network.perform_tests('server', 'admin', 0)
    Router.perform_tests('server', 'admin', 0)
    Subnet.perform_tests('server', 'admin', 0)
    Port.perform_tests('server', 'admin', 0)
    Trunk.perform_tests('server', 'admin', 0)
    Bgpvpn.perform_tests('server', 'admin', 0)
    Firewall.perform_tests('server', 'admin', 0)
    FirewallPolicy.perform_tests('server', 'admin', 0)
    FirewallRule.perform_tests('server', 'admin', 0)
    FloatingIP.perform_tests('server', 'admin', 0)
    Gateway.perform_tests('server', 'admin', 0)
    GatewayConnection.perform_tests('server', 'admin', 0)
    Loadbalancer.perform_tests('server', 'admin', 0)
    LoadbalancerHealthMonitor.perform_tests('server', 'admin', 0)
    LoadbalancerListener.perform_tests('server', 'admin', 0)
    LoadbalancerPool.perform_tests('server', 'admin', 0)
    MeteringLabel.perform_tests('server', 'admin', 0)
    MeteringLabelRule.perform_tests('server', 'admin', 0)
    QosPolicy.perform_tests('server', 'admin', 0)
    VpnService.perform_tests('server', 'admin', 0)
    # SecurityGroup.perform_tests('server', 'admin', 0)
    SecurityGroupRule.perform_tests('server', 'admin', 0)
    SFCFlowClassifier.perform_tests('server', 'admin', 0)
    SFCPortChain.perform_tests('server', 'admin', 0)
    SFCPortPair.perform_tests('server', 'admin', 0)
    SFCPortPairGroup.perform_tests('server', 'admin', 0)
    latency.latency_data_transform()
