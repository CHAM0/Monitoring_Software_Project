#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import psutil as ps
import datetime
import os

def getBootTimes():
    boot = datetime.datetime.fromtimestamp(ps.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    print("Date du dernier boot : {}").format(boot)
    return boot

def getTemperatures():
    temp = ps.sensors_temperatures()
    print("Temperature du CPU : {} ").format(temp["coretemp"][1].current)
    return temp["coretemp"][1].current

def getKernelInfos():
    kernel = os.popen('uname -r').read()
    print("version du kernel : {}").format(kernel)
    return kernel

"""      
if __name__ == "__main__":
    getBootTimes()
    getTemperatures()
"""