import xlrd
import xlwt
import sys

def main(argv):
	print 'python throughput_data_processing.py sloth|neutron'
	if argv[1] == 'sloth':
		scope = 'sloth'
	elif argv[1] == 'neutron':
		scope = 'neutron'
	return scope

def throughput(sheet, col_num):
	throughput = []
	row_num = 0
	sum = 0
	total = 11
	num = sheet.col_values(col_num)
	for no in num:
		if no == 'running time:':
			tp_num = sheet.cell_value(row_num-1, col_num)
			if tp_num != 'new round':
				sum += tp_num
				throughput.append(tp_num)
			else:
				sum += 0
				total -= 1
				throughput.append(0)
		row_num += 1
	avg = sum / total
	throughput.append(avg)
	return throughput

def read_xl(scope, round_num):
	file_name = './throughput_data_' + scope + '_' + str(round_num) + '_8-6.xls'
	workbook = xlrd.open_workbook(file_name)
	sheet1 = workbook.sheet_by_index(0)
	return sheet1

def write_xl(throughput, row, col, ws):
	for g_num in range(0, 12):
		ws.write(row, col+g_num, throughput[g_num])

if __name__ == '__main__':
	scope = main(sys.argv)
	wb = xlwt.Workbook()
	sheet_name = 'request_number'
	ws = wb.add_sheet(sheet_name)
	col_num = 0
	
	for round_num in range(1, 6):
		ws.write(round_num, 0, 'Round ' + str(round_num))
		sheet = read_xl(scope, round_num)
		tp_num = throughput(sheet, col_num)
		write_xl(tp_num, round_num, 1, ws) # row, col, round number of file
	
	wb.save(scope + '_throughput_80.xls')
	print 'Done!'