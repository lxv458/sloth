import config
from httpapi import HttpAPI


class DomainUserRole(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_domains(self):
        return self.get(config.AUTH_DOMAINS)

    def get_domain(self, domainid):
        return self.get(config.AUTH_DOMAINS + '/' + domainid)

    def create_domain(self, name, description='', enabled=False, domainId=''):
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

    def create_role(self, name, domainid, description='', roleId=''):
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

    def create_user(self, name, domainid, password='changeme', description='', email='', userId=''):
        payload = {
            'name': name,
            'password': password,
            'domainid': domainid,
            'description': description,
            'email': email
        }
#        'userid': userId,
        return self.post(config.AUTH_USERS, payload)

    def delete_user(self, userid):
        return self.delete(config.AUTH_USERS + '/' + userid)

    def get_grants(self, domainId, userId):
        return self.get(config.AUTH_DOMAINS + '/' + domainId + '/users/' + userId + '/roles')

    def create_grant(self, domainId, userId, roleId, grantId=None):
        payload = {
            'domainid': domainId,
            'userid': userId,
            'roleid': roleId
        }
#       'grantid': grantId
        return self.post(config.AUTH_DOMAINS + '/' + domainId + '/users/' + userId + '/roles', payload)

    def delete_grant(self, domainId, userId, roleId):
        return self.delete(config.AUTH_DOMAINS + '/' + domainId + '/users/' + userId + '/roles' + roleId)

    def validate_user(self, domainId, username, password):
        payload = {
            'username': username,
            'userpwd': password
        }
        #userpwd
        return self.post(config.AUTH_DOMAINS + '/' + domainId + '/users/roles', payload)
