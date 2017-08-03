import xlwt
import throughput_test
import logging
import sys
import time
import threading
import os

from scripts import utils


def main(argv):
    if argv[1] == 'mix':
        for i in range(5):
            print('Round ' + str(i))
            logging.info("new round: %d" % (i+1))
            throughput_test_mix()
    else:
        throughput_test_separate()


def throughput_data_transform():
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

    ws.write(0, 0, 'serial number', style)
    ws.write(0, 1, 'request method', style)
    ws.write(0, 2, 'time consuming (ms)', style)

    row_index = 1
    num = 1
    for line in input:
        if 'test GET Request' in line:
            ws.write(row_index, 0, "GET", style)
            row_index += 1
        if 'test POST Request' in line:
            ws.write(row_index, 0, "POST", style)
            row_index += 1
        if 'test PUT Request' in line:
            ws.write(row_index, 0, "PUT", style)
            row_index += 1
        if 'test DELETE Request' in line:
            ws.write(row_index, 0, "DELETE", style)
            row_index += 1
        if 'new round' in line:
            ws.write(row_index, 0, "new round", style)
            num = 1
            row_index += 1
        if 'cost:' in line:
            l = line.split(':')
            ws.write(row_index, 0, num, style)
            ws.write(row_index, 1, l[2].split(' ')[0], style)
            ws.write(row_index, 2, l[3].split(' ')[1], style)
            num += 1
            row_index += 1
        if 'cost time' in line:
            l = line.split(':')
            ws.write(row_index, 0, 'cost time:', style)
            ws.write(row_index, 2, l[3].split(' ')[1], style)
            row_index += 1
        if 'running time' in line:
            l = line.split(':')
            ws.write(row_index, 0, 'running time:', style)
            ws.write(row_index, 2, l[3].split(' ')[1], style)
            row_index += 1

    wb.save('throughput_data_neutron_5_8-3.xls')


def throughput_test_mix():
    logging.info("test throughput wih multiple mixed API Request")
    start_time = time.time()
    logging.info('start_time: %f' % start_time)

    thread = threading.Thread(target=throughput_test.throughput_mix, args=())
    thread.setDaemon(True)
    thread.start()
    thread.join(1)

    end_time = time.time()
    logging.info('end_time: %f' % end_time)
    logging.info('running time: %f ms' % ((end_time - start_time) * 1000))
    logging.info("throughput test end!")


def throughput_test_separate():
    logging.info("test throughput wih multiple API and separated Request")
    logging.info("test GET Request")
    for i in range(50):
        throughput_test.throughput_get_test()

    logging.info("test POST Request")
    for i in range(50):
        throughput_test.throughput_post_test()

    logging.info("test PUT Request")
    for i in range(50):
        throughput_test.throughput_put_test()

    logging.info("test DELETE Request")
    for i in range(50):
        throughput_test.throughput_delete_test()


def log_config():

    logging_config = utils.get_logging_config('logging')
    filename = logging_config['filename']

    if os.path.exists(filename):
        os.remove(filename)

    logging.basicConfig(filename=filename, level=logging_config['level'])


if __name__ == "__main__":
    log_config()
    main(sys.argv)
    throughput_data_transform()
