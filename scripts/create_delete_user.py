from domainuserrole import DomainUserRole
import uuid
import sys


def main(argv):
    if argv[1] == 'delete':
        deleteusers()
    else:
        createusers()


def createusers():
    # create domain named sloth
    domainId = uuid.uuid1()
    dur.create_domain('sloth', domainId, 'create a domain for sloth')

    # create user Lily, Gary, Tom, Jack
    userId_Lily = uuid.uuid1()
    dur.create_user('Lily', userId_Lily, domainId, 'Lily')
    userId_Gary = uuid.uuid1()
    dur.create_user('Gary', userId_Gary, domainId, 'Gary')
    userId_Tom = uuid.uuid1()
    dur.create_user('Tom', userId_Tom, domainId, 'Tom')
    userId_Jack = uuid.uuid1()
    dur.create_user('Jack', userId_Jack, domainId, 'Jack')

    # create role named user
    roleId = uuid.uuid1()
    dur.create_role('user', roleId, domainId)

    # create grant
    grantId_Lily = uuid.uuid1()
    dur.create_grant('grant-Lily', grantId_Lily, domainId, userId_Lily, roleId)
    grantId_Gary = uuid.uuid1()
    dur.create_grant('grant-Gary', grantId_Gary, domainId, userId_Gary, roleId)
    grantId_Tom = uuid.uuid1()
    dur.create_grant('grant-Tom', grantId_Tom, domainId, userId_Tom, roleId)
    grantId_Jack = uuid.uuid1()
    dur.create_grant('grant-Jack', grantId_Jack, domainId, userId_Jack, roleId)


def deleteusers():
    domains = dur.get_domains()
    for domain in domains:
        if domain.name == 'sloth':
            domainId = domain.domainid

    roles = dur.get_roles()
    for role in roles:
        if role.name == 'user':
            roleId = role.roleid

    users = dur.get_users()
    for user in users:
        if user.name == 'Lily':
            userId_Lily = user.userid
        if user.name == 'Gary':
            userId_Gary = user.userid
        if user.name == 'Tom':
            userId_Tom = user.userid
        if user.name == 'Jack':
            userId_Jack = user.userid

    grants = dur.get_grants(domainId, userId_Lily)
    for grant in grants:
        if grant.name == 'grant-Lily':
            grantId_Lily = grant.grantid
            # delete grant and user
            dur.delete_grant(domainId, userId_Lily, grantId_Lily)
            dur.delete_user(userId_Lily)
    grants = dur.get_grants(domainId, userId_Gary)
    for grant in grants:
        if grant.name == 'grant-Gary':
            grantId_Gary = grant.grantid
            # delete grant adn user
            dur.delete_grant(domainId, userId_Gary, grantId_Gary)
            dur.delete_user(userId_Gary)
    grants = dur.get_grants(domainId, userId_Tom)
    for grant in grants:
        if grant.name == 'grant-Tom':
            grantId_Tom = grant.grantid
            # delete grant and user
            dur.delete_grant(domainId, userId_Tom, grantId_Tom)
            dur.delete_user(userId_Tom)
    grants = dur.get_grants(domainId, userId_Jack)
    for grant in grants:
        if grant.name == 'grant-Jack':
            grantId_Jack = grant.grantid
            # delete grant and user
            dur.delete_grant(domainId, userId_Jack, grantId_Jack)
            dur.delete_user(userId_Jack)

    # delete role
    dur.delete_role(roleId)

    # delete domain
    dur.delete_domain(domainId)

if __name__ == "__main__":
    dur = DomainUserRole('server', 'admin')
    main(sys.argv)
