#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import time
import sys
import requests
import datetime
import subprocess
sys.path.insert(0, './sondes')
import sCPU as cpu # NOQA
import sMEMORY as mem # NOQA
import sDISK as disk # NOQA
import sPROCESS as proc # NOQA
import sSENSORS as sens # NOQA
import sNetwork as net # NOQA


def sendCPU():
    hostname = cpu.getHostname()
    cpuCount = cpu.cpuCount()
    cpuFreq = cpu.cpuFreq()
    cpuPercent = cpu.cpuPercent()

    cpuInfos = {
        "hostname": hostname,
        "count": cpuCount,
        "frequence": cpuFreq[2],
        "min-max": [cpuFreq[0], cpuFreq[1]],
        "percentage": cpuPercent}

    url = 'http://localhost:5001/sonde/scpu'
    req = requests.post(url, json=cpuInfos)
    print(req.text)


def sendMEM():
    hostname = cpu.getHostname()
    total = mem.total()
    used = mem.used()
    available = mem.available()

    memInfos = {
        "hostname": hostname,
        "total": total,
        "used": used,
        "available": available}

    url = 'http://localhost:5001/sonde/smemory'
    req = requests.post(url, json=memInfos)
    print(req.text)


def sendDISK():
    hostname = cpu.getHostname()
    total = disk.total()
    used = disk.used()
    free = disk.free()
    percent = disk.percent()

    diskInfos = {
        "hostname": hostname,
        "total": total,
        "used": used,
        "free": free,
        "percent": percent}

    url = 'http://localhost:5001/sonde/sdisk'
    req = requests.post(url, json=diskInfos)
    print(req.text)


def sendNET():
    hostname = cpu.getHostname()
    network = net.getInfos()

    networkInfos = {
        "hostname": hostname,
        "sent": network[0],
        "recv": network[1],
        "psent": network[2],
        "precv": network[3]}

    url = 'http://localhost:5001/sonde/snetwork'
    req = requests.post(url, json=networkInfos)
    print(req.text)


def sendPROCESS():
    x = subprocess.check_output("./sondes/sPROCESS.sh", shell=True)
    hostname = cpu.getHostname()
    mylist = x.split("\n")

    procInfos = {
        "hostname": hostname,
        "total": mylist[0],
        "root": mylist[1]}

    url = 'http://localhost:5001/sonde/sprocess'
    req = requests.post(url, json=procInfos)
    print(req.text)


def sendSENSORS():
    try:
        time = sens.getBootTimes()
        temp = sens.getTemperatures()
        kernel = sens.getKernelInfos()
        hostname = cpu.getHostname()

        sensInfos = {
            "hostname": hostname,
            "time": time,
            "temperature": temp,
            "kernel": kernel}

        url = 'http://localhost:5001/sonde/ssensors'
        req = requests.post(url, json=sensInfos)
        print(req.text)

    except Exception:
        print "no sensors"
        return


if __name__ == "__main__":

    while 1 == 1:
        print(datetime.datetime.now())
        sendCPU()
        sendMEM()
        sendDISK()
        sendNET()
        sendPROCESS()
        sendSENSORS()
        time.sleep(120)
