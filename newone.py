from openpyxl import load_workbook
import time
start_time = time.time()

_sepdt = {'TYO': ['HND', 'NRT'],
          'SPK': ['CTS', 'OKD'],
          'OSA': ['ITM', 'KIX']}

wb = load_workbook('skyscanner_search_log_201505_201511.xlsx')

sheet = wb['6months']
start_row = 1
end_row = 12
none_break = True
for index, row in enumerate(sheet.iter_rows()):
    print index
    if index > end_row:
        break
    elif start_row <= index <= end_row:
        routes = row[0].value.split('_')
        print (routes)
    else:
        print ('THAT KHONG THE TIN DUOC')
    # print(row[0].value)
print("--- %s seconds ---" % (time.time() - start_time))
print('==========================================')
