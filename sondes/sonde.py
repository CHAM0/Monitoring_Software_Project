#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import sNetwork as net
import sCPU as cpu
import sMEMORY as mem
import sDISK as disk
import sPROCESS as proc
import sSENSORS as sens
# import requests
import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@ds119129.mlab.com:19129/monitoring-software-project") # NOQA
db = client["monitoring-software-project"]
cpuColl = db["CPU"]
memColl = db["MEMORY"]
diskColl = db["DISK"]
netColl = db["NETWORK"]
procColl = db["PROCESS"]
sensColl = db["SENSOR"]


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
        "percentage": cpuPercent,
        "added": datetime.datetime.now()}

    """
    if cpuColl.find_one({"hostname": hostname}):
        print("Mise a jour des infos du CPU de  {} !").format(hostname)
        cpuColl.find_one_and_replace({"hostname": hostname}, cpuInfos)
    else:
        print("Ajout des infos du CPU de : {}").format(hostname)
        cpuColl.insert_one(cpuInfos)
    """

    print("\n\nAjout des infos du CPU de : {}\n").format(hostname)
    cpuColl.insert_one(cpuInfos)

    # suppression des infos datant de plus d'une heure
    date = datetime.datetime.now() - datetime.timedelta(hours=1)
    cpuColl.delete_many({"added": {"$lt": date}}) # NOQA


def sendMEMORY():
    hostname = cpu.getHostname()
    total = mem.total()
    used = mem.used()
    available = mem.available()

    memInfos = {
        "hostname": hostname,
        "total": total,
        "used": used,
        "available": available,
        "added": datetime.datetime.now()}

    print("\n\nAjout des infos de la RAM de : {}\n").format(hostname)
    memColl.insert_one(memInfos)

    # suppression des infos datant de plus d'une heure
    date = datetime.datetime.now() - datetime.timedelta(hours=1)
    memColl.delete_many({"added": {"$lt": date}})


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
        "percent": percent,
        "added": datetime.datetime.now()}

    print("\n\nAjout des infos de de la partiton / de : {}\n").format(hostname)
    diskColl.insert_one(diskInfos)

    # suppression des infos datant de plus d'une heure
    date = datetime.datetime.now() - datetime.timedelta(hours=1)
    diskColl.delete_many({"added": {"$lt": date}})


def sendNetwork():
    hostname = cpu.getHostname()
    network = net.getInfos()

    networkInfos = {
        "hostname": hostname,
        "sent": network[0],
        "recv": network[1],
        "psent": network[2],
        "precv": network[3],
        "added": datetime.datetime.now()}

    print("\n\nAjout des infos de la carte réseau : {}\n").format(hostname)
    netColl.insert_one(networkInfos)

    # suppression des infos datant de plus d'une heure
    date = datetime.datetime.now() - datetime.timedelta(hours=1)
    netColl.delete_many({"added": {"$lt": date}})


def sendProcess():
    total, root = proc.getProcessInfos()
    hostname = cpu.getHostname()

    procInfos = {
        "hostname": hostname,
        "total": total,
        "root": root,
        "added": datetime.datetime.now()}

    print("\n\nAjout des infos sur les Processus : {}\n").format(hostname)
    procColl.insert_one(procInfos)

    # suppression des infos datant de plus d'une heure
    date = datetime.datetime.now() - datetime.timedelta(hours=1)
    procColl.delete_many({"added": {"$lt": date}})


def sendSensors():
    time = sens.getBootTimes()
    temp = sens.getTemperatures()
    kernel = sens.getKernelInfos()
    hostname = cpu.getHostname()

    procInfos = {
        "hostname": hostname,
        "time": time,
        "temperature": temp,
        "kernel": kernel,
        "added": datetime.datetime.now()}

    print("\n\nAjout des infos diverses : {}\n").format(hostname)
    sensColl.insert_one(procInfos)

    # suppression des infos datant de plus d'une heure
    date = datetime.datetime.now() - datetime.timedelta(hours=1)
    sensColl.delete_many({"added": {"$lt": date}})


if __name__ == "__main__":
    print(datetime.datetime.now())
    sendCPU()
    sendMEMORY()
    sendDISK()
    sendNetwork()
    sendProcess()
    sendSensors()
