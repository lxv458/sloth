import json


if __name__ == '__main__':
    import domainuserrole
    api = domainuserrole.DomainUserRole('server', 'admin')
    print json.dumps(json.loads(api.get_domains().text), indent=4)
    print json.dumps(json.loads(api.get_roles().text), indent=4)
    print json.dumps(json.loads(api.get_users().text), indent=4)
