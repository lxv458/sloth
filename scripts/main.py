import logging

from scripts import utils
from scripts.tests.network import Network

if __name__ == '__main__':
    logging_config = utils.get_logging_config('logging')
    logging.basicConfig(filename=logging_config['filename'], level=logging_config['level'])
    Network.perform_tests('server', 'admin')
