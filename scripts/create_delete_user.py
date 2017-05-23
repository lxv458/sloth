from domainuserrole import DomainUserRole
import sys
import json


def main(argv):
    if argv[1] == 'delete':
        deleteusers()
    if argv[1] == 'create':
        createusers()
    if argv[1] == 'clear':
        clear()


def createusers():
    # create domain named sloth
    domainId = 'sloth'
    dur.create_domain('sloth', 'create a domain for sloth', True)

    # create user Lily, Gary, Tom, Jack
    dur.create_user('Lily', domainId, 'Lily')
    dur.create_user('Gary', domainId, 'Gary')
    dur.create_user('Tom', domainId, 'Tom')
    dur.create_user('Jack', domainId, 'Jack')

    # create role named user
    dur.create_role('user', domainId)

    # create grant
    roleId = 'user@' + domainId
    role = json.loads(dur.get_role(roleId).text)
    dur.create_grant(domainId, 'Lily@' + domainId, roleId)
    dur.create_grant(domainId, 'Gary@' + domainId, roleId)
    dur.create_grant(domainId, 'Tom@' + domainId, roleId)
    dur.create_grant(domainId, 'Jack@' + domainId, roleId)

    print 'grants-Lily: ' + dur.get_grants(domainId, 'Lily@' + domainId).text
    print 'grants-Gary: ' + dur.get_grants(domainId, 'Gary@' + domainId).text
    print 'grants-Tom: ' + dur.get_grants(domainId, 'Tom@' + domainId).text
    print 'grants-Jack: ' + dur.get_grants(domainId, 'Jack@' + domainId).text

    # validate user
    dur.validate_user(domainId, 'Lily', 'Lily')
    dur.validate_user(domainId, 'Gary', 'Gary')
    dur.validate_user(domainId, 'Tom', 'Tom')
    dur.validate_user(domainId, 'Jack', 'Jack')


def deleteusers():
    domains = dur.get_domains()
    for domain in json.loads(domains.text)['domains']:
        if domain['name'] == 'sloth':
            domainId = domain['domainid']

    roles = dur.get_roles()
    for role in json.loads(roles.text)['roles']:
        if role['roleid'] == 'user@sdn':
            continue
        if role['name'] == 'user':
            roleId = role['roleid']

    users = dur.get_users()
    for user in json.loads(users.text)['users']:
        if user['name'] == 'Lily':
            userId_Lily = user['userid']
        if user['name'] == 'Gary':
            userId_Gary = user['userid']
        if user['name'] == 'Tom':
            userId_Tom = user['userid']
        if user['name'] == 'Jack':
            userId_Jack = user['userid']

    # delete grant and user
    dur.delete_grant(domainId, userId_Lily, roleId)
    dur.delete_user(userId_Lily)

    dur.delete_grant(domainId, userId_Gary, roleId)
    dur.delete_user(userId_Gary)

    dur.delete_grant(domainId, userId_Tom, roleId)
    dur.delete_user(userId_Tom)

    dur.delete_grant(domainId, userId_Jack, roleId)
    dur.delete_user(userId_Jack)

    # delete role
    dur.delete_role(roleId)

    # delete domain
    dur.delete_domain(domainId)


def clear():
    roles = dur.get_roles()
    for role in json.loads(roles.text)['roles']:
        if (role['name'] == 'admin') or (role['roleid'] == 'user@sdn'):
            continue
        dur.delete_role(role['roleid'])

    users = dur.get_users()
    for user in json.loads(users.text)['users']:
        if (user['name'] == 'admin') or (user['userid'] == 'user@sdn'):
            continue
        dur.delete_user(user['userid'])


if __name__ == "__main__":
    dur = DomainUserRole('server', 'admin')
    main(sys.argv)
    print 'domains: ' + dur.get_domains().text
    print 'roles: ' + dur.get_roles().text
    print 'users: ' + dur.get_users().text
