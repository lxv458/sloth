import ConfigParser
import ast
import copy
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
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    config = ConfigParser.ConfigParser()
    config.read(file)
    return {option: config.get(username, option) for option in config.options(username)}
