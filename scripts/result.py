if __name__ == '__main__':
    id = "4e8e5957-649f-477b-9e5b-f1f75b21c03c"
    l = id.split('-')
    tmp = int(l[4], 16) + 3
    tmp_id = str(hex(tmp))[2:]
    new_id = l[0] + '-' + l[1] + '-' + l[2] + '-' + l[3] + '-' + tmp_id
    print 'new_id :' + new_id
