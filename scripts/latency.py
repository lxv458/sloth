import xlwt


def latency_data_transform(filename):
    input = open(filename, 'r')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('HTTP request cost time')

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
    ws.col(0).width = 256 * 26
    ws.col(1).width = 256 * 16
    ws.col(2).width = 256 * 20

    ws.write(0, 0, 'object', style)
    ws.write(0, 1, 'request method', style)
    ws.write(0, 2, 'time consuming (ms)', style)

    row_index = 1
    column_index = -3
    for line in input:
        if 'perform' in line:
            ws.write(row_index, 0 + column_index, line.split(':')[2].split(' ')[1], style)
        if 'cost' in line:
            l = line.split(':')
            ws.write(row_index, 1 + column_index, l[2].split(' ')[0], style)
            ws.write(row_index, 2 + column_index, l[3].split(' ')[1], style)
            row_index += 1
        if 'Test Round' in line:
            row_index = 1
            column_index += 3

    wb.save(filename + '.xls')

if __name__ == "__main__":
    latency_data_transform()
