import ConfigParser
import ast
import copy
import logging
import os

import requests

import config


def get_tocken(ip, user, port=8181):
    payload = copy.deepcopy(user)
    payload['grant_type'] = 'password'
    r = requests.post(('http://%s:%d' + config.OAUTH2_TOCKEN) % (ip, port), data=payload)
    return ast.literal_eval(r.text)


def get_server(servername):
    server = get_user(servername)
    server['port'] = int(server['port'])
    return server


def get_user(username, filename='cfg.ini'):
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    cfg = ConfigParser.ConfigParser()
    cfg.read(f)
    return {option: cfg.get(username, option) for option in cfg.options(username)}


def get_logging_config(logname):
    return get_user(logname)


def assert_status(response, status_code):
    if response.status_code == status_code:
        logging.info('pass')
        return True
    else:
        logging.error('fail, expected: %d, but got: %d' % (status_code, response.status_code))
        logging.error(response.text)
        return False
