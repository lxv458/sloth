import xlwt
import throughput_test
import logging
import sys


def main(argv):
    if argv[1] == 'mix':
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
    ws.col(1).width = 256 * 20

    ws.write(0, 0, 'serial number', style)
    ws.write(0, 1, 'time consuming (ms)', style)

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
        if 'cost time' in line:
            l = line.split(':')
            ws.write(row_index, 0, num, style)
            ws.write(row_index, 1, l[3].split(' ')[1], style)
            num += 1
            row_index += 1

    wb.save('throughput_data.xls')


def throughput_test_mix():
    logging.info("test throughput wih multiple API and 780 mixed Request")
    throughput_test.throughput_mix()


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


if __name__ == "__main__":
    throughput_test.log_config()
    main(sys.argv)
    throughput_data_transform()
