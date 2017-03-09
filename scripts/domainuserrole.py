import config
from httpapi import HttpAPI


class DomainUserRole(HttpAPI):
    def __init__(self, servername, username):
        HttpAPI.__init__(self, servername, username)

    def get_domains(self):
        return self.get(config.AUTH_DOMAINS)

    def get_domain(self, domainid):
        return self.get(config.AUTH_DOMAINS + '/' + domainid)

    def create_domain(self, domainid, name, description, enabled):
        payload = {
            'domainid': domainid,
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

    def create_role(self, roleid, name, description, domainid):
        payload = {
            'roleid': roleid,
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

    def create_user(self, name, userid, password, domainid, description, email):
        payload = {
            'name': name,
            'userid': userid,
            'password': password,
            'domainid': domainid,
            'description': description,
            'email': email
        }
        return self.post(config.AUTH_USERS, payload)

    def delete_user(self, userid):
        return self.delete(config.AUTH_USERS + '/' + userid)


