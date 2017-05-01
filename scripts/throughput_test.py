import threading
import logging
import time
import utils
from scripts.tests.network import Network
from scripts.tests.network import NETWORK_ONE

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


def log_config():
    logging_config = utils.get_logging_config('logging')
    logging.basicConfig(filename=logging_config['filename'], level=logging_config['level'])


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


if __name__ == '__main__':
    throughput_get_test()
    throughput_post_test()
    # throughput_put_test()
    throughput_delete_test()

