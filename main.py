# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from geo import Geojp
import requests

# Done this one
# --------- THIS ONE USE FOR CREATE '_lst' AND '_lcc'
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
_lcc = {}


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
        return None


def get_key(lst, get_len=3):
    rs = []
    if len(lst) <= get_len:
        for item in lst:
            rs.append(item[1])
    else:
        for idn in range(0, get_len):
            rs.append(lst[idn][1])
    return rs


def sort_and_filter(start, end, listitem, lcc={}):
    # rs = []
    # frs = []
    rs_lcc = []
    rs_normal = []
    num = len(listitem)
    if num == 1:
        if start in lcc and listitem[0] in lcc and (listitem[0] in lcc[start] or end in lcc[listitem[0]]):
            return ','.join(listitem), None
        else:
            return None, ','.join(listitem)
    else:
        for item in listitem:
            if start in lcc and item in lcc and (item in lcc[start] or end in lcc[item]):
                rs_lcc.append(item)
            else:
                rs_normal.append(item)
    num_lcc = len(rs_lcc)
    if num_lcc >= 3 or num_lcc == num:
        return ','.join(rs_lcc), None
    else:
        if num >= 3:
            remain = 3 - num_lcc
        else:
            remain = num - num_lcc

        if remain == 1:
            return ','.join(rs_lcc), ','.join(rs_normal)
        else:
            rs = []
            for nm in rs_normal:
                k = get_total_price(dep1=start, arr1=end, mid=nm)
                if k:
                    rs.append([k, nm])
            rs.sort(key=lambda x: x[0])
            return ','.join(rs_lcc), ','.join(get_key(rs, remain))

    # elif num == 2:
    #     if start in lcc and listitem[0] in lcc and (listitem[0] in lcc[start] or end in lcc[listitem[0]]):
    #         # if listitem[0] in lcc[start] or end in lcc[listitem[0]]:
    #         return listitem
    #     elif start in lcc and listitem[1] in lcc and (listitem[1] in lcc[start] or end in lcc[listitem[1]]):
    #         # if listitem[1] in lcc[start] or end in lcc[listitem[1]]:
    #         return list(reversed(listitem))
    #     else:
    #         for item in listitem:
    #             k = get_total_price(dep1=start, arr1=end, mid=item)
    #             if k:
    #                 tmp = [k, item]
    #                 rs.append(tmp)
    #         rs.sort(key=lambda x: x[0])
    #         return get_key(rs)
    # else:
    #     lcc_lst = []
    #     for item in listitem:
    #         if start in lcc and item in lcc and (item in lcc[start] or end in lcc[item]):
    #             lcc_lst.append(item)
    #         else:
    #             k = get_total_price(dep1=start, arr1=end, mid=item)
    #             if k:
    #                 tmp = [k, item]
    #                 rs.append(tmp)
    #     num_lcc_list = len(lcc_lst)
    #     if num_lcc_list >= 3:
    #         rs_lcc = []
    #         for it in lcc_lst:
    #             k = get_total_price(dep1=start, arr1=end, mid=it)
    #             if k:
    #                 tmp = [k, it]
    #                 rs_lcc.append(tmp)
    #         rs_lcc.sort(key=lambda x: x[0])
    #         return get_key(rs_lcc)
    #     elif num_lcc_list == 2:
    #         rs_lcc = []
    #         for it in lcc_lst:
    #             k = get_total_price(dep1=start, arr1=end, mid=it)
    #             if k:
    #                 tmp = [k, it]
    #                 rs_lcc.append(tmp)
    #         rs_lcc.sort(key=lambda x: x[0])
    #         frs.append(rs_lcc[0][1])
    #         frs.append(rs_lcc[1][1])
    #         rs.sort(key=lambda x: x[0])
    #         frs.append(rs[0][1])
    #         return frs
    #     else:
    #         rs.sort(key=lambda x: x[0])
    #         lcc_lst.append(rs[0][1])
    #         lcc_lst.append(rs[1][1])
    #         if num_lcc_list == 0:
    #             lcc_lst.append(rs[2][1])
    #         return lcc_lst


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

# --------- MAKE ROUTES BY THIS ONE -------------
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

# -------------- THIS ONE FOR FILTER ---------
# --------------- Run for 100 row in excel ---------------
#
#
# wb = load_workbook('result.xlsx')
# sheet = wb['DOM_SECTION_MST']
# start_row = 1
# end_row = 2450
# sheet['J1'] = 'FINAL_RESULT'
# for index, row in enumerate(sheet.iter_rows()):
#     if start_row <= index <= end_row:
#         print 'row', index, 'run ...'
#         ind = 'J' + str(index + 1)
#         if row[8].value:
#             tmp_lst = list(row[8].value.split(','))
#             if len(tmp_lst) != 1:
#                 sheet[ind].value = ','.join(sort_and_filter(start=row[1].value, end=row[2].value, listitem=tmp_lst))
#             else:
#                 sheet[ind].value = ','.join(tmp_lst)
#         print 'finish', index
# wb.save('final_result.xlsx')
# # --------------------------------------------------------

wb = load_workbook('final_result.xlsx')
sheet = wb['DOM_SECTION_MST']
start_row = 1
end_row = 10

for row in sheet.iter_rows():
    if row[6].value == 1:
        if row[1].value in _lcc:
            _lcc[row[1].value].append(row[2].value)
        else:
            _lcc[row[1].value] = [row[2].value]
# for items in _lcc.iteritems():
#     print(items)
for index, row in enumerate(sheet.iter_rows()):
    if start_row <= index <= end_row:
        print 'row', index, 'run ...'
        inj = 'J' + str(index + 1)
        ink = 'K' + str(index + 1)
        if row[8].value:
            tmp_lst = list(row[8].value.split(','))
            sheet[inj].value, sheet[ink] = sort_and_filter(start=row[1].value, end=row[2].value, listitem=tmp_lst, lcc=_lcc)
        print 'finish', index
sheet['K1'] = 'LCC_RESULTS'
sheet['J1'] = 'NORMAL_RESULTS'
wb.save('final_result_2.xlsx')
print 'Successful ! THIS IS SPARTA'
