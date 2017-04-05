import requests
import logging
import datetime
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
        start_time = datetime.datetime.now().microsecond
        session = self.__session.get(self.__server + path, auth=self.__auth)
        end_time = datetime.datetime.now().microsecond
        logging.info('GET request cost: %f ms' %((end_time - start_time) * 0.001))
        return session

    def put(self, path, payload):
        start_time = datetime.datetime.now().microsecond
        session = self.__session.put(self.__server + path, auth=self.__auth, json=payload)
        end_time = datetime.datetime.now().microsecond
        logging.info('PUT request cost: %f ms' %((end_time - start_time) * 0.001))
        return session

    def post(self, path, payload):
        start_time = datetime.datetime.now().microsecond
        session = self.__session.post(self.__server + path, auth=self.__auth, json=payload)
        end_time = datetime.datetime.now().microsecond
        logging.info('POST request cost: %f ms' %((end_time - start_time) * 0.001))
        return session

    def delete(self, path):
        start_time = datetime.datetime.now().microsecond
        session = self.__session.delete(self.__server + path, auth=self.__auth)
        end_time = datetime.datetime.now().microsecond
        logging.info('DELETE request cost: %f ms' %((end_time - start_time) * 0.001))
        return session

    @staticmethod
    def perform_tests(servername, username):
        raise Exception('perform tests not implemented')
