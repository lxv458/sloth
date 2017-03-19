import logging

from scripts import utils
from scripts.tests.network import Network
from scripts.tests.router import Router
from scripts.tests.subnet import Subnet

if __name__ == '__main__':
    logging_config = utils.get_logging_config('logging')
    logging.basicConfig(filename=logging_config['filename'], level=logging_config['level'])
    Network.perform_tests('server', 'admin')
    Router.perform_tests('server', 'admin')
    Subnet.perform_tests('server', 'admin')
