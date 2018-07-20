#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import pyArango.connection as ac
import time
import datetime as dt
import analyser
import mailAlert

time.sleep(30)

conn = ac.Connection(arangoURL='http://db:8529')
db = conn["monitoring-software-project"]
cpuColl = db["CPU"]
memoryColl = db["MEMORY"]
diskColl = db["DISK"]
networkColl = db["NETWORK"]
processColl = db["PROCESS"]
sensorsColl = db["SENSORS"]
alertsColl = db["ALERTS"]
notificationsColl = db["NOTIFICATIONS"]


# supprime les anciennes infos des sondes dans la bdd
def clearOldInfos(collection, time):
    for infos in collection.fetchAll():
        current = dt.datetime.now() - dt.timedelta(hours=time)
        added = dt.datetime(current.year, infos['added'][0], infos['added'][1],infos['added'][2],infos['added'][3]) # NOQA

        if added < current:
            print("{} \nDELETING OLD INFORMATION").format(infos._id) # NOQA
            infos.delete()


if __name__ == "__main__":

    while 1 == 1:
        
        analyser.checkCERT()
        time.sleep(30)
        clearOldInfos(cpuColl, 1)
        clearOldInfos(memoryColl, 1)
        clearOldInfos(diskColl, 1)
        clearOldInfos(networkColl, 1)
        clearOldInfos(processColl, 1)
        clearOldInfos(sensorsColl, 1)
        clearOldInfos(alertsColl, 1500)
        clearOldInfos(notificationsColl, 1500)
        time.sleep(30)
        mailAlert.alert()
        time.sleep(30)
