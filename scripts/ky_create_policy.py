def create_user_file(n):
    user_dict_file_name = 'user_dict.txt'

    f = open(user_dict_file_name, 'w')

    f.write('user_dict = {\n')

    f.write('\tLily:lily,\n')

    for i in range(n-1):
        f.write('\t%s%d:%s%d,\n' % ('Lily', i, 'lily', i))


    # f.write('\tGary:gary,\n')
    # f.write('\tTom:tom,\n')
    # f.write('\tJack:jack\n')
    f.write('}')

    f.close()


def print_global_policy(f):
    f.write(
        '''GLOBAL_POLICY {
    admin_accept_all {
        if (sloth.subject.role == "admin") {
            ACCEPT
        }
    }
    all_can_get {
        if (sloth.action.method == "GET") {
            ACCEPT
        }
    }
}

LOCAL_POLICY {    
    admin, admin {
        no_local_policy {
            ACCEPT
        }
    }
''')


def create_policy_file(n):
    policy_25_file = 'policy/policy_gray_25_ac.txt'
    policy_1000_file = 'policy/policy_create.txt'

    in_f =  open(policy_25_file, 'r')
    policy_25 = in_f.read()
    in_f.close()

    out_f = open(policy_1000_file, 'w')

    print_global_policy(out_f)

    out_f.write('    user, Lily')
    out_f.write(policy_25)
    out_f.write('\n')

    for i in range(n - 1):
        out_f.write('    user, %s%d' % ('Lily', i))
        out_f.write(policy_25)
        out_f.write('\n')

    out_f.write('}')
    out_f.close()


if __name__ == "__main__":
    n = 100  # 100 -1000
    create_user_file(n / 25)
    create_policy_file(n / 25)
