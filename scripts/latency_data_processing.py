import xlrd
import xlwt
import openpyxl
import os

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
			get_time += sheet.cell_value(row_num, col_num+1)
			get_num += 1
			row_num += 1
		if m == 'POST':
			post_time += sheet.cell_value(row_num, col_num+1)
			post_num += 1
			row_num += 1
		if m == 'PUT':
			put_time += sheet.cell_value(row_num, col_num+1)
			put_num += 1
			row_num += 1
		if m == 'DELETE':
			del_time += sheet.cell_value(row_num, col_num+1)
			del_num += 1
			row_num += 1

	if get_num != 0:
		cost_time.append(get_time/get_num)
	else:
		cost_time.append(0)
	if post_num != 0:
		cost_time.append(post_time/post_num)
	else:
		cost_time.append(0)
	if put_num !=0:
		cost_time.append(put_time/put_num)
	else:
		cost_time.append(0)
	if del_num != 0:
		cost_time.append(del_time/del_num)
	else:
		cost_time.append(0)
	
	return cost_time

def specific_method_average(sheet, col_num, method):
	cost_time = 0
	col_method = sheet.col_values(col_num)
	for m in col_method:
		if m == method:
			cost_time += sheet.cell_value(col_method.index(m), col_num+1)
	return cost_time

def read_xl(round_num):
	file_name = './Latency_neutron_' + str(round_num) + '_8-3.xls'
	workbook = xlrd.open_workbook(file_name)
	sheet1 = workbook.sheet_by_index(0)
	return sheet1

def write_xl(cost_time, row, col, ws):
	ws.write(row, col, 'GET time:')
	ws.write(row, col+1, cost_time[0])
	ws.write(row+1, col, 'POST time:')
	ws.write(row+1, col+1, cost_time[1])
	ws.write(row+2, col, 'PUT time:')
	ws.write(row+2, col+1, cost_time[2])
	ws.write(row+3, col, 'DELETE time:')
	ws.write(row+3, col+1, cost_time[3])


if __name__ == '__main__':
	wb = xlwt.Workbook()
	sheet_name = 'average_time'
	ws = wb.add_sheet(sheet_name)
	for r_num in range(1, 6):
		round_num = r_num # round number, each round has 5 groups, total is 5 round
		row = 6 * round_num - 5
		ws.write(row, 0, 'Round ' + str(round_num))
		for g_num in range(1, 6):
			group_num = g_num # group number in each round
			col = 3 * group_num - 2
			sheet = read_xl(round_num)
			cost_time = average_time(sheet, col) # first group data
			write_xl(cost_time, row, col, ws) # row, col, round number of file

	wb.save('average_time.xls')
	print 'Done!'