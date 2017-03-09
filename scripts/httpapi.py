import requests

import utils


class HttpAPI:
    def __init__(self, servername, username):
        server = utils.get_server(servername)
        self.__server = 'http://%s:%d' % (server['ip'], server['port'])
        user = utils.get_user(username)
        self.__auth = (user['username'], user['password'])

    def set_server(self, servername):
        server = utils.get_server(servername)
        self.__server = 'http://%s:%d' % (server['ip'], server['port'])

    def set_user(self, username):
        user = utils.get_user(username)
        self.__auth = (user['username'], user['password'])

    def set_server_user(self, servername, username):
        self.__init__(servername, username)

    def get(self, path):
        return requests.get(self.__server + path, auth=self.__auth)

    def put(self, path, payload):
        return requests.put(self.__server + path, auth=self.__auth, json=payload)

    def post(self, path, payload):
        return requests.post(self.__server + path, auth=self.__auth, json=payload)

    def delete(self, path):
        return requests.delete(self.__server + path)
