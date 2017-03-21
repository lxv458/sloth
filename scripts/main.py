import logging

from scripts import utils
from scripts.tests.network import Network
from scripts.tests.router import Router
from scripts.tests.subnet import Subnet
from scripts.tests.port import Port
from scripts.tests.trunk import Trunk
from scripts.tests.bgpvpn import Bgpvpn

if __name__ == '__main__':
    logging_config = utils.get_logging_config('logging')
    logging.basicConfig(filename=logging_config['filename'], level=logging_config['level'])
    Network.perform_tests('server', 'admin')
    Router.perform_tests('server', 'admin')
    Subnet.perform_tests('server', 'admin')
    Port.perform_tests('server', 'admin')
    Trunk.perform_tests('server', 'admin')
    Bgpvpn.perform_tests('server', 'admin')
