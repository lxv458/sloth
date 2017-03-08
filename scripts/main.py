import ConfigParser
import ast
import copy
import json
import os

import requests


def get_tocken(ip, user, port=8181):
    payload = copy.deepcopy(user)
    payload['grant_type'] = 'password'
    r = requests.post('http://%s:%d/oauth2/token' % (ip, port), data=payload)
    return ast.literal_eval(r.text)


def get_server(servername):
    return get_user(servername)


def get_user(username, filename='cfg.ini'):
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    config = ConfigParser.ConfigParser()
    config.read(file)
    return {option: config.get(username, option) for option in config.options(username)}


class HttpAccessAPI:
    def __init__(self, servername, username, port=8181):
        self.__server = 'http://%s:%d' % (get_server(servername)['ip'], port)
        user = get_user(username)
        self.__auth = (user['username'], user['password'])

    def set_server(self, servername, port=8181):
        self.__server = 'http://%s:%d' % (get_server(servername)['ip'], port)

    def set_user(self, username):
        user = get_user(username)
        self.__auth = (user['username'], user['password'])

    def set_server_user(self, servername, username, port=8181):
        self.__init__(servername, username, port)

    def get(self, path):
        return requests.get(self.__server + path, auth=self.__auth)

    def put(self, path, payload):
        return requests.put(self.__server + path, auth=self.__auth, data=json.dumps(payload))

    def post(self, path, payload):
        return requests.post(self.__server + path, auth=self.__auth, data=json.dumps(payload))

    def delete(self, path):
        return requests.delete(self.__server + path)


if __name__ == '__main__':
    import config

    httpAccessAPI = HttpAccessAPI('server', 'admin')
    print json.dumps(json.loads(httpAccessAPI.get(config.AUTH_USERS).text), indent=4)
    print json.dumps(json.loads(httpAccessAPI.get(config.AUTH_DOMAINS).text), indent=4)
