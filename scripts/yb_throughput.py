import xlwt
import yb_throughput_test
import logging
import time
import threading
import os

import utils

def main(threadNum):
    for i in range(1,threadNum+1):
        throughput_mix(i)
        time.sleep(5)

def throughput_data_transform(scope,routnum):
    input = open('sloth-test.log', 'r')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('throughput cost time')

    # set format
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT

    style = xlwt.XFStyle()
    style.font = font
    style.alignment = alignment
    ws.col(0).width = 256 * 20
    ws.col(1).width = 256 * 16
    ws.col(2).width = 256 * 20
    ws.col(3).width = 256 * 20

    ws.write(0, 0, 'thread number', style)
    ws.write(0, 1, 'execute time(ms)', style)
    ws.write(0, 2, 'request number', style)
    ws.write(0, 3, 'packet lost', style)
    ws.write(0, 4, 'lost rate', style)
    ws.write(0, 5, 'throughput(r/s)', style)

    row_index = 1
    col_index = 0
    requestnum = 0
    runtime = 0
    for line in input:
        if 'test throughput with' in line:
            threanum = line.split(' ')[3]
            ws.write(row_index , col_index, threanum)
        if 'running time:' in line:
            runtime = float((line.split(':')[3]).split(' ')[1])
            ws.write(row_index,col_index+1,runtime)
        if 'request cost' in line:
            requestnum +=1
        if 'throughput test end!' in line:
            ws.write(row_index,col_index+2,requestnum)

            base_test_num = 180
            total_round = 64
            time_round = int(total_round / int(threanum))
            num_request_send = base_test_num * time_round * int(threanum)

            ws.write(row_index, col_index + 3, num_request_send - requestnum)
            ws.write(row_index, col_index + 4, (num_request_send - requestnum) * 1.0 / num_request_send)
            ws.write(row_index, col_index + 5, requestnum*1000/runtime)
            requestnum = 0
            row_index += 1

    file_name = 'data/throughput/throughput_'+scope+'_' + str(routnum) + '.xls'
    wb.save(file_name)

def throughput_mix(thread_num):
    task=[]
    print("test throughput with "+str(thread_num)+" thread")
    logging.info("test throughput with "+str(thread_num)+" thread")
    for i in range(thread_num):
        task.append(threading.Thread(target=yb_throughput_test.test_multiple, args=([thread_num])))
    before = time.time()
    logging.info('start_time: %f' % before)
    for t in task:
        t.start()
    for t in task:
        t.join()
    after = time.time()
    logging.info('end_time: %f' % after)
    logging.info('running time: %f ms' % ((after - before) * 1000))
    logging.info("throughput test end!")
    print('test throughput end within %f ms' % ((after - before) * 1000))

def log_config():

    logging_config = utils.get_logging_config('logging')
    filename = logging_config['filename']

    if os.path.exists(filename):
        os.remove(filename)

    logging.basicConfig(filename=filename, level=logging_config['level'])


if __name__ == "__main__":
    log_config()
    threadNum = 30
    main(threadNum)
    throughput_data_transform('origin_test', 31)
