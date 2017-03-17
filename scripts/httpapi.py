import requests

import utils


class HttpAPI(object):
    def __init__(self, servername, username):
        server = utils.get_server(servername)
        self.__server = 'http://%s:%d' % (server['ip'], server['port'])
        user = utils.get_user(username)
        self.__auth = (user['username'], user['password'])
        self.__session = requests.Session()

    def set_server(self, servername):
        server = utils.get_server(servername)
        self.__server = 'http://%s:%d' % (server['ip'], server['port'])
        self.__session = requests.Session()

    def set_user(self, username):
        user = utils.get_user(username)
        self.__auth = (user['username'], user['password'])
        self.__session = requests.Session()

    def set_server_user(self, servername, username):
        self.__init__(servername, username)

    def get(self, path):
        return self.__session.get(self.__server + path, auth=self.__auth)

    def put(self, path, payload):
        return self.__session.put(self.__server + path, auth=self.__auth, json=payload)

    def post(self, path, payload):
        return self.__session.post(self.__server + path, auth=self.__auth, json=payload)

    def delete(self, path):
        return self.__session.delete(self.__server + path, auth=self.__auth)

    @staticmethod
    def perform_tests(servername, username):
        raise Exception('perform tests not implemented')
