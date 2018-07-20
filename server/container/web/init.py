#!/usr/bin/python2.7
# -*- coding=utf-8 -*-


import pyArango.connection as ac
import time

time.sleep(5)
conn = ac.Connection(arangoURL='http://db:8529')
try:
    db = conn.createDatabase(name="monitoring-software-project")
    db.createCollection(name="CPU")
    db.createCollection(name="MEMORY")
    db.createCollection(name="DISK")
    db.createCollection(name="NETWORK")
    db.createCollection(name="PROCESS")
    db.createCollection(name="SENSORS")
    db.createCollection(name="ALERTS")
    db.createCollection(name="NOTIFICATIONS")

except Exception:
    print("Collection already created")


def init():
    conn = ac.Connection(arangoURL='http://db:8529')

    try:
        db = conn.createDatabase(name="monitoring-software-project")
        db.createCollection(name="CPU")
        db.createCollection(name="MEMORY")
        db.createCollection(name="DISK")
        db.createCollection(name="NETWORK")
        db.createCollection(name="PROCESS")
        db.createCollection(name="SENSORS")
        db.createCollection(name="ALERTS")
        db.createCollection(name="NOTIFICATIONS")

    except Exception:
        print("Collection already created")
