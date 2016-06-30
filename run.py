#!/usr/bin/env python
# -*- coding: utf-8 -*-
from main import Main
import time
import datetime


class Run(object):
    """Dung de debug and run don gian hon, khong can thay doi config"""

    if __name__ == '__main__':
        start_time = time.time()
        print '------ program is running ------'
        # dt = datetime.datetime.now()
        # main = Main()
        # main.make_lst()
        # fname = 'result_' + str(dt.date()).replace('-', '') + '_' + str(dt.time()).replace(':', '').replace('.', '_')
        # main.creattion_of_god(fname=fname)
        # main = Main()
        # main.forfun()
        total_time = time.time() - start_time
        print '----- total run time: %s -----' % total_time
