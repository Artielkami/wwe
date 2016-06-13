#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from xlrd import open_workbook
import xlwt
import time
import csv as csv

import sys

start_time = time.time()

book = open_workbook('final_result_2.xlsx')
sheet_xl = book.sheet_by_index(0)
combine_port_dict = {'TYO': ['HND', 'NRT'],
                     'SPK': ['CTS', 'OKD'],
                     'OSA': ['ITM', 'KIX']}
wb = open_workbook('skyscanner_search_log_201505_201511.xlsx')

print("load workbook time --- %s seconds ---" % (time.time() - start_time))

# f = open("sometest.txt", "w")
csv_file = open('result_trial.csv', 'wb')
outputWritter = csv.writer(csv_file, delimiter='\t')
outputWritter.writerow(['TOTAL SEARCH', 'DEPARTURE', 'ARRIVAL', 'LCC_PORT', 'NONE_LCC_PORT'])


def find(dep, arr, num):
    # rs = None
    for rowidx in range(sheet_xl.nrows):
        r = sheet_xl.row(rowidx)
        if r[1].value == dep and r[2].value == arr:
            # outputWritter.writerow('time_search:\t' + str(num) + '\t' + dep + '\t' + arr + '\t' +\
            #     'lcc:\t' + (r[9].value if r[9].value else '') + '\t' +\
            #     'none_lcc:\t' + (r[10].value if r[10].value else ''))
            lcc = r[9].value.replace(',', '_') if r[9].value else ''
            none_lcc = r[10].value.replace(',', '_') if r[10].value else ''
            outputWritter.writerow([num, dep, arr, lcc, none_lcc])
            # f.write(s + '\n')
            break
    # TODO this is sparta


def make_result(value_keyword, num):
    routes = value_keyword.split('_')
    if routes[0] in combine_port_dict and routes[1] in combine_port_dict:
        tmp_lst = combine_port_dict[routes[0]]
        tmp_lst_2 = combine_port_dict[routes[1]]
        for item in tmp_lst:
            find(item, tmp_lst_2[0], num)
            find(item, tmp_lst_2[1], num)
    elif routes[0] in combine_port_dict:
        tmp_lst = combine_port_dict[routes[0]]
        find(tmp_lst[0], routes[1], num)
        find(tmp_lst[1], routes[1], num)
    elif routes[1] in combine_port_dict:
        tmp_lst = combine_port_dict[routes[1]]
        find(routes[0], tmp_lst[0], num)
        find(routes[0], tmp_lst[1], num)
    else:
        find(routes[0], routes[1], num)


sheet = wb.sheet_by_name('6months')
start_row = 1
end_row = 150
none_break = True
for index in range(sheet.nrows):
    print 'runing row --- ', index
    if index > end_row:
        break
    elif start_row <= index <= end_row:
        row = sheet.row(index)
        make_result(row[0].value, row[1].value)
    else:
        print('THAT KHONG THE TIN DUOC')

csv_file.close()
# f.close()
print("--- total runtime: %s seconds ---" % (time.time() - start_time))
print('==========================================')
