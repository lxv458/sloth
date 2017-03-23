import logging

from scripts import utils
from scripts.tests.network import Network
from scripts.tests.router import Router
from scripts.tests.subnet import Subnet
from scripts.tests.port import Port
from scripts.tests.trunk import Trunk
from scripts.tests.bgpvpn import Bgpvpn
from scripts.tests.firewall import Firewall
from scripts.tests.firewallpolicy import Firewall_Policy
from scripts.tests.firewallrule import Firewall_Rule
from scripts.tests.floatingip import FloatingIP
from scripts.tests.gateway import Gateway
from scripts.tests.gatewayconnection import Gateway_Connection
from scripts.tests.loadbalancer import Loadbalancer
from scripts.tests.loadbalancerhealthmonitor import Loadbalancer_health_monitor
from scripts.tests.loadbalancerlistener import Loadbalancer_listener
from scripts.tests.loadbalancerpool import Loadbalancer_pool
from scripts.tests.meteringlabel import Metering_label
from scripts.tests.meteringrule import Metering_label_rule
from scripts.tests.qospolicy import Qos_policy
from scripts.tests.vpnservice import Vpn_service
from scripts.tests.securitygroup import Security_group
from scripts.tests.securitygrouprule import Security_group_rule
from scripts.tests.sfcflowclassifier import SFC_flow_classifier
from scripts.tests.sfcportchain import SFC_port_chain
from scripts.tests.sfcportpair import SFC_port_pair
from scripts.tests.sfcportpairgroup import SFC_port_pair_group

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
    Firewall_Policy.perform_tests('server', 'admin')
    Firewall_Rule.perform_tests('server', 'admin')
    #FloatingIP.perform_tests('server', 'admin')
    Gateway.perform_tests('server', 'admin')
    Gateway_Connection.perform_tests('server', 'admin')
    Loadbalancer.perform_tests('server', 'admin')
    Loadbalancer_health_monitor.perform_tests('server', 'admin')
    Loadbalancer_listener.perform_tests('server', 'admin')
    Loadbalancer_pool.perform_tests('server', 'admin')
    Metering_label.perform_tests('server', 'admin')
    Metering_label_rule.perform_tests('server', 'admin')
    Qos_policy.perform_tests('server', 'admin')
    Vpn_service.perform_tests('server', 'admin')
    Security_group.perform_tests('server', 'admin')
    Security_group_rule.perform_tests('server', 'admin')
    SFC_flow_classifier.perform_tests('server', 'admin')
    SFC_port_chain.perform_tests('server', 'admin')
    SFC_port_pair.perform_tests('server', 'admin')
    SFC_port_pair_group.perform_tests('server', 'admin')
