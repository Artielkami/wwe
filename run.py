#!/usr/bin/env python
# -*- coding: utf-8 -*-
from main import Main
import time

class Run(object):
    def __init__(self):
        start_time = time.time()
        print '------ program is running ------'
        Main
        print '----- total run time: %s -----' % time.time() - start_time