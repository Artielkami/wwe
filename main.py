# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from geo import Geojp
import requests

# Done this one

# wb = load_workbook('master_data.xlsx')
# sheet1 = wb['DOM_SECTION_MST']
# _lst = {}
# for row in sheet1.iter_rows():
#     if row[5].value == 1:
#         if row[1].value in _lst:
#             _lst[row[1].value].append(row[2].value)
#         else:
#             _lst[row[1].value] = [row[2].value]

# Global variable for mapping
_map = Geojp()


def getprice(departure, arrival, day='20160620'):
    """Get the lowest cost of treval between 2 port"""
    url = 'http://10.10.20.132/best_price/tabicapi_api'
    dp = departure
    ar = arrival
    dp_time = day
    info = {'departure_port': dp, 'arrival_port': ar, 'departure_date': dp_time}
    r = ''
    try:
        r = requests.get(url, params=info)
    except requests.exceptions.ConnectionError:
        print 'Quỳ, ca này khó, bác sĩ bó tay !'
    else:
        while r.status_code != 200:
            r = requests.get(url, params=info)
    try:
        k = r.json()['f_price']
    except KeyError:
        return 666666
    else:
        return k


def get_total_price(dep1, arr1, mid):
    """Get price for all travel path"""
    f1 = getprice(departure=dep1, arrival=mid)
    f2 = getprice(departure=mid, arrival=arr1)
    if f1 and f2:
        return f1 + f2
    else:
        return 0


def get_key(lst):
    rs = []
    if len(lst) <= 3:
        for item in lst:
            rs.append(item[1])
    else:
        for i in range(0, 3):
            rs.append(lst[i][1])
    return rs


def sort_and_filter(start, end, listitem):
    rs = []
    for item in listitem:
        k = get_total_price(dep1=start, arr1=end, mid=item)
        if k:
            tmp = [k, item]
            rs.append(tmp)
    rs.sort(key=lambda x: x[0])
    return get_key(rs)


def get_way(depart, desti, dictaw):
    """Function for calculate continous airport"""
    out = []  # mảng chứ giá trị kết quả
    con = []  # mảng tạm chứa giá trị trung chuyển
    if depart in dictaw:
        con = dictaw[depart]
    des_area, des_id = _map.get_area(desti)
    dep_area, dep_id = _map.get_area(depart)
    if dep_id < des_id:
        for item in con:
            if (dep_id <= _map.get_area_id(item) <= des_id) and (desti in dictaw[item]):
                out.append(item)
            else:
                pass
    elif dep_id > des_id:
        for item in con:
            if (dep_id >= _map.get_area_id(item) >= des_id) and (desti in dictaw[item]):
                out.append(item)
            else:
                pass
    else:
        for item in con:
            if ((des_id - 1) <= _map.get_area_id(item) <= (des_id + 1)) and (desti in dictaw[item]):
                out.append(item)
            else:
                pass
    return out


# dep = 'AOJ'
# des = 'RIS'
print '--------------------------------------------------'
# print dep, _map.get_area_id(dep)
# print des, _map.get_area_id(des)
# print _map.get_area('HND')
# print _map.get_area('NRT')
# for key, value in _lst.iteritems():
#     print key, value
# k = get_way(depart=dep, desti=des, dictaw=_lst)
# print k
# print ','.join(_lst[dep])
# print ','.join(_lst['CTS'])
# print ','.join(get_way(depart=dep, desti=des, dictaw=_lst))
# print 'AKJ -> HSG : ', get_way('AKJ', 'ITM', lst)
# nwb = Workbook()
# sheet = nwb.create_sheet(title='RESULT')
# sheet = wb['DOM_SECTION_MST']

# -------------- THIS ONE DONE ------------

# for row in sheet1.iter_rows():
#     if row[4].value:
#         k = get_way(depart=row[1].value, desti=row[2].value, dictaw=_lst)
#         if k:
#             index = 'I' + str(row[0].value + 1)
#             # sheet1[index].value = k.__str__()
#             sheet1[index].value = ','.join(k)
#
# sheet1['I1'].value = 'RESULT'
# wb.save('result.xlsx')

# -------------------------------------------
# --------------- Run for 100 row in excel ---------------
wb = load_workbook('result.xlsx')
sheet = wb['DOM_SECTION_MST']
start_row = 1
end_row = 2450
sheet['J1'] = 'FINAL_RESULT'
for index, row in enumerate(sheet.iter_rows()):
    if start_row <= index <= end_row:
        print 'row', index, 'run ...'
        ind = 'J' + str(index + 1)
        if row[8].value:
            tmp_lst = list(row[8].value.split(','))
            if len(tmp_lst) != 1:
                sheet[ind].value = ','.join(sort_and_filter(start=row[1].value, end=row[2].value, listitem=tmp_lst))
            else:
                sheet[ind].value = ','.join(tmp_lst)
        print 'finish', index
wb.save('final_result.xlsx')
# --------------------------------------------------------
print 'Successful ! THIS IS SPARTA'
