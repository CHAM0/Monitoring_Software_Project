#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import pygal
from pygal.style import LightStyle
import pyArango.connection as ac
import os

conn = ac.Connection(arangoURL='http://db:8529')
db = conn["monitoring-software-project"]
netColl = db["NETWORK"]
procColl = db["PROCESS"]
sensColl = db["SENSORS"]


# get all hostname
def getHostname():
    hostname = []
    aql = "FOR doc IN NETWORK RETURN DISTINCT doc.hostname"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for key in queryResult:
        hostname.append(str(key))
    return hostname


# Get all hours
def getDates():
    dates = []
    for infos in netColl.fetchAll():
        if infos["added"] not in dates:
            dates.append(infos["added"])
    dates.sort()
    return dates


# formate dates hh:mm for dispay
def getFormatedDates():
    datesFormated = []
    dates = getDates()
    for i in dates:
        datesFormated.append(str(i[2])+":"+str(i[3]))
    return datesFormated


# ----------- recv / sent --------------#
def networkInfos():
    minMax_chart = pygal.Bar(height=400, fill=True, interpolate='cubic', style=LightStyle) # NOQA
    minMax_chart.title = "Data sent and receive (in Mo)"
    hostname = getHostname()
    minMax_chart.x_labels = hostname

    recv = []
    sent = []

    for host in hostname:
        aql = """
            FOR i IN NETWORK
            FILTER i.hostname == '{0}'
            RETURN DISTINCT i.recv
        """.format(host)

        aql2 = """
            FOR i IN NETWORK
            FILTER i.hostname == '{0}'
            RETURN DISTINCT i.sent
        """.format(host)

        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
        queryResult2 = db.AQLQuery(aql2, rawResults=True, batchSize=1, count=True) # NOQA
        for q in queryResult:
            recv.append(q)
        for z in queryResult2:
            sent.append(z)

        minMax_chart.add("Paquet receive", recv)
        minMax_chart.add("Paquet sent", sent)

    minMax_chart.render_to_file("static/images/network/network.svg")


# ----------- process / root --------------#
def processInfos():
    minMax_chart = pygal.Bar(height=400, fill=True, interpolate='cubic', style=LightStyle) # NOQA
    minMax_chart.title = "PROCESS"
    hostname = getHostname()
    minMax_chart.x_labels = hostname
    x = 0
    recv = []
    sent = []

    for host in hostname:
        aql = """
            FOR i IN PROCESS
            FILTER i.hostname == '{0}'
            RETURN DISTINCT i.total
        """.format(host)

        aql2 = """
            FOR i IN PROCESS
            FILTER i.hostname == '{0}'
            RETURN DISTINCT i.root
        """.format(host)

        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
        queryResult2 = db.AQLQuery(aql2, rawResults=True, batchSize=1, count=True) # NOQA
        for q in queryResult:
            recv.append(int(q))
            x = int(q)
        for z in queryResult2:
            add = x / 3
            sent.append(add)

    minMax_chart.add("Total", recv[len(recv)-1])
    minMax_chart.add("Root", sent)

    minMax_chart.render_to_file("static/images/process/process.svg")


def deleteProc():
    print "deleting old graph"
    os.remove("./static/images/process/process.svg")


def deleteNet():
    print "deleting old graph"
    os.remove("./static/images/network/network.svg")


if __name__ == '__main__':
    networkInfos()
    processInfos()
