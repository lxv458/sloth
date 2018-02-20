import xlrd
import xlwt
import sys
import numpy


def main(argv):
    print 'python latency_data_processing.py sloth|neutron'
    if argv[1] == 'sloth':
        scope = 'sloth'
    elif argv[1] == 'neutron':
        scope = 'neutron'
    return scope


def average_time(sheet, col_num):
    get_time = 0
    post_time = 0
    put_time = 0
    del_time = 0
    get_num = 0
    post_num = 0
    put_num = 0
    del_num = 0
    cost_time = []
    col_method = sheet.col_values(col_num)
    row_num = 1

    for m in col_method:
        if m == 'GET':
            get_time += float(sheet.cell_value(row_num, col_num + 1))
            get_num += 1
            row_num += 1
        if m == 'POST':
            post_time += float(sheet.cell_value(row_num, col_num + 1))
            post_num += 1
            row_num += 1
        if m == 'PUT':
            put_time += float(sheet.cell_value(row_num, col_num + 1))
            put_num += 1
            row_num += 1
        if m == 'DELETE':
            del_time += float(sheet.cell_value(row_num, col_num + 1))
            del_num += 1
            row_num += 1

    if get_num != 0:
        cost_time.append(get_time / get_num)
    else:
        cost_time.append(0)
    if post_num != 0:
        cost_time.append(post_time / post_num)
    else:
        cost_time.append(0)
    if put_num != 0:
        cost_time.append(put_time / put_num)
    else:
        cost_time.append(0)
    if del_num != 0:
        cost_time.append(del_time / del_num)
    else:
        cost_time.append(0)

    return cost_time


def specific_method_average(sheet, col_num, method):
    cost_time = 0
    col_method = sheet.col_values(col_num)
    for m in col_method:
        if m == method:
            cost_time += sheet.cell_value(col_method.index(m), col_num + 1)
    return cost_time


def read_xl(file_name):
    # file_name = './Latency_' + scope + '_' +  str(round_num) + '_8-6.xls'
    # file_name = '8.xls'
    workbook = xlrd.open_workbook(file_name + '.xls')
    sheet1 = workbook.sheet_by_index(0)
    return sheet1


def write_xl(cost_time, row, col, ws):
    ws.write(row, col, 'GET time:')
    ws.write(row, col + 1, cost_time[0])
    ws.write(row + 1, col, 'POST time:')
    ws.write(row + 1, col + 1, cost_time[1])
    ws.write(row + 2, col, 'PUT time:')
    ws.write(row + 2, col + 1, cost_time[2])
    ws.write(row + 3, col, 'DELETE time:')
    ws.write(row + 3, col + 1, cost_time[3])


def process1(filename, threshold):
    sheet = read_xl(filename)
    get_time = 0
    post_time = 0
    put_time = 0
    del_time = 0
    get_num = 0
    post_num = 0
    put_num = 0
    del_num = 0
    anl_num = 0
    get_max = 0
    get_min = threshold
    post_max = 0
    post_min = threshold
    put_max = 0
    put_min = threshold
    del_max = 0
    del_min = threshold
    col_method = sheet.col_values(0)
    row_num = 0
    cost_time = []

    for m in col_method:
        num = 0
        time = 0
        max = 0
        min = threshold
        for i in range(1, 190):
            tmp = float(sheet.cell_value(row_num, i))
            if (tmp < threshold):
                if (tmp > max):
                    max = tmp
                if (tmp < min):
                    min = tmp
                time += tmp
                num += 1
            else:
                anl_num += 1
        if m == 'GET':
            if (max > get_max):
                get_max = max
            if (min < get_min):
                get_min = min
            get_time += time
            get_num += num
            row_num += 1
        if m == 'POST':
            if (max > post_max):
                post_max = max
            if (min < post_min):
                post_min = min
            post_time += time
            post_num += num
            row_num += 1
        if m == 'PUT':
            if (max > put_max):
                put_max = max
            if (min < put_min):
                put_min = min
            put_time += time
            put_num += num
            row_num += 1
        if m == 'DELETE':
            if (max > del_max):
                del_max = max
            if (min < del_min):
                del_min = min
            del_time += time
            del_num += num
            row_num += 1

    if get_num != 0:
        cost_time.append(get_time / get_num)
    else:
        cost_time.append(0)
    if post_num != 0:
        cost_time.append(post_time / post_num)
    else:
        cost_time.append(0)
    if put_num != 0:
        cost_time.append(put_time / put_num)
    else:
        cost_time.append(0)
    if del_num != 0:
        cost_time.append(del_time / del_num)
    else:
        cost_time.append(0)
    if anl_num != 0:
        cost_time.append(anl_num)
    else:
        cost_time.append(0)
    cost_time.append(get_max)
    cost_time.append(get_min)
    cost_time.append(post_max)
    cost_time.append(post_min)
    cost_time.append(put_max)
    cost_time.append(put_min)
    cost_time.append(del_max)
    cost_time.append(del_min)
    return cost_time


def process2(filename, threshold):
    filename = 'data/Latency/' + filename
    sheet = read_xl(filename)

    anl_num = 0
    col_method = sheet.col_values(0)
    row_num = 0
    cost_time = []
    get_mat = []
    post_mat = []
    put_mat = []
    del_mat = []

    for m in col_method:
        for i in range(1, 190):
            tmp = float(sheet.cell_value(row_num, i))
            if (tmp < threshold):
                if m == 'GET':
                    get_mat.append(tmp)
                if m == 'POST':
                    post_mat.append(tmp)
                if m == 'PUT':
                    put_mat.append(tmp)
                if m == 'DELETE':
                    del_mat.append(tmp)
            else:
                anl_num += 1
        row_num += 1

    cost_time.append(numpy.mean(get_mat))
    cost_time.append(numpy.max(get_mat))
    cost_time.append(numpy.min(get_mat))
    cost_time.append(numpy.std(get_mat))

    cost_time.append(numpy.mean(post_mat))
    cost_time.append(numpy.max(post_mat))
    cost_time.append(numpy.min(post_mat))
    cost_time.append(numpy.std(post_mat))

    cost_time.append(numpy.mean(put_mat))
    cost_time.append(numpy.max(put_mat))
    cost_time.append(numpy.min(put_mat))
    cost_time.append(numpy.std(put_mat))

    cost_time.append(numpy.mean(del_mat))
    cost_time.append(numpy.max(del_mat))
    cost_time.append(numpy.min(del_mat))
    cost_time.append(numpy.std(del_mat))

    cost_time.append(anl_num)

    return cost_time


if __name__ == '__main__':
    wb = xlwt.Workbook()

    high_threshold = 20
    output_filename = 'data/Latency/AVE_sloth_100_T%d.xls' % high_threshold
    # output_filename = 'data/Latency/AVE_origin_T%d.xls' % high_threshold

    sheet_name = 'average_time'
    ws = wb.add_sheet(sheet_name)
    file_list = ["Sloth_100_1", "Sloth_100_2", "Sloth_100_3", "Sloth_100_4"]
    # file_list = ['Origin1', 'Origin2', 'Origin3', 'Origin4', 'Origin5', 'Origin6', 'Origin7']
    num_file = len(file_list)

    cost_list = []
    for f in file_list:
        cost_list.append(process2(f, high_threshold))

    for i in range(num_file):
        ws.write(0, i * 3 + 1, file_list[i])

    ws.write(1, 0, 'Get')
    ws.write(2, 0, 'Post')
    ws.write(3, 0, 'Put')
    ws.write(4, 0, 'Delete')
    ws.write(5, 0, 'Anomaly')

    for i in range(num_file):
        ws.write(1, i * 3 + 1, cost_list[i][0])
        ws.write(1, i * 3 + 2, cost_list[i][3])
        ws.write(2, i * 3 + 1, cost_list[i][4])
        ws.write(2, i * 3 + 2, cost_list[i][7])
        ws.write(3, i * 3 + 1, cost_list[i][8])
        ws.write(3, i * 3 + 2, cost_list[i][11])
        ws.write(4, i * 3 + 1, cost_list[i][12])
        ws.write(4, i * 3 + 2, cost_list[i][15])
        ws.write(5, i * 3 + 1, cost_list[i][16])

    wb.save(output_filename)

    # scope = main('neutron')
    # wb = xlwt.Workbook()
    # sheet_name = 'average_time'
    # ws = wb.add_sheet(sheet_name)
    # get_agv_sum = 0
    # post_agv_sum = 0
    # put_agv_sum = 0
    # del_agv_sum = 0
    # for r_num in range(1, 6):
    # 	round_num = r_num # round number, each round has 11 groups, total is 5 round
    # 	row = 6 * round_num - 5
    # 	ws.write(row, 0, 'Round ' + str(round_num))
    # 	get_sum = 0
    # 	post_sum = 0
    # 	put_sum = 0
    # 	del_sum = 0
    # 	for g_num in range(1, 12):
    # 		group_num = g_num # group number in each round
    # 		col = 3 * group_num - 2
    # 		sheet = read_xl(round_num)
    # 		cost_time = average_time(sheet, col)
    # 		write_xl(cost_time, row, col, ws) # row, col, round number of file
    # 		get_sum += cost_time[0]
    # 		post_sum += cost_time[1]
    # 		put_sum += cost_time[2]
    # 		del_sum += cost_time[3]
    # 	get_agv = get_sum / 11
    # 	post_agv = post_sum / 11
    # 	put_agv = put_sum / 11
    # 	del_agv = del_sum /11
    # 	ws.write(row, 34, get_agv)
    # 	ws.write(row+1, 34, post_agv)
    # 	ws.write(row+2, 34, put_agv)
    # 	ws.write(row+3, 34, del_agv)
    # 	get_agv_sum += get_agv
    # 	post_agv_sum += post_agv
    # 	put_agv_sum += put_agv
    # 	del_agv_sum += del_agv
    # ws.write(31, 2, get_agv_sum / 5)
    # ws.write(32, 2, post_agv_sum / 5)
    # ws.write(33, 2, put_agv_sum / 5)
    # ws.write(34, 2, del_agv_sum / 5)
    #
    # wb.save(scope + '_average_time_80.xls')
    print 'Done!'