import config
from httpapi import HttpAPI


class DomainUserRole(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_domains(self):
        return self.get(config.AUTH_DOMAINS)

    def get_domain(self, domainid):
        return self.get(config.AUTH_DOMAINS + '/' + domainid)

    def create_domain(self, name, domainId, description='', enabled=False):
        payload = {
            'domainid': domainId,
            'name': name,
            'description': description,
            'enabled': enabled
        }
        return self.post(config.AUTH_DOMAINS, payload)

    def delete_domain(self, domainid):
        return self.delete(config.AUTH_DOMAINS + '/' + domainid)

    def get_roles(self):
        return self.get(config.AUTH_ROLES)

    def get_role(self, roleid):
        return self.get(config.AUTH_ROLES + '/' + roleid)

    def create_role(self, name, roleId, domainid, description=''):
        payload = {
            'roleid': roleId,
            'name': name,
            'description': description,
            'domainid': domainid
        }
        return self.post(config.AUTH_ROLES, payload)

    def delete_role(self, roleid):
        return self.delete(config.AUTH_ROLES + '/' + roleid)

    def get_users(self):
        return self.get(config.AUTH_USERS)

    def get_user(self, userid):
        return self.get(config.AUTH_USERS + '/' + userid)

    def create_user(self, name, userId, domainid, password='changeme', description='', email=''):
        payload = {
            'name': name,
            'userid': userId,
            'password': password,
            'domainid': domainid,
            'description': description,
            'email': email
        }
        return self.post(config.AUTH_USERS, payload)

    def delete_user(self, userid):
        return self.delete(config.AUTH_USERS + '/' + userid)

    def get_grants(self, domainId, userId):
        return self.delete(config.AUTH_DOMAINS + '/' + domainId + '/users' + userId + '/roles')

    def create_grant(self, domainId, userId, role):
        return self.post(config.AUTH_DOMAINS + '/' + domainId + '/users' + userId + '/roles', role)

    def delete_grant(self, domainId, userId, roleId):
        return self.delete(config.AUTH_DOMAINS + '/' + domainId + '/users' + userId + '/roles' + roleId)
