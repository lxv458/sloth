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
    FloatingIP.perform_tests('server', 'admin')
    Gateway.perform_tests('server', 'admin')
    Gateway_Connection.perform_tests('server', 'admin')
