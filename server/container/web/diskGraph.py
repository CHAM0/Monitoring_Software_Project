#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import pygal
from pygal.style import LightStyle
import pyArango.connection as ac
import os

conn = ac.Connection(arangoURL='http://db:8529')
db = conn["monitoring-software-project"]
Coll = db["DISK"]


# get all hostname
def getHostname():
    hostname = []
    aql = "FOR doc IN DISK RETURN DISTINCT doc.hostname"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for key in queryResult:
        hostname.append(str(key))
    return hostname


# Get all hours
def getDates():
    dates = []
    for infos in Coll.fetchAll():
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


def diskPercent():
    gauge = pygal.SolidGauge(inner_radius=0.70, fill=True, interpolate='cubic', style=LightStyle) # NOQA
    percent_formatter = lambda x: '{:.10g}%'.format(x) # NOQA
    gauge.value_formatter = percent_formatter

    hostname = getHostname()
    infos = []
    for host in hostname:
        aql = """
            FOR i IN DISK
            FILTER i.hostname == '{0}'
            RETURN DISTINCT i.percent
        """.format(host)

        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
        for q in queryResult:
            infos.append(q)

        gauge.add(host, [{'value': infos[len(infos)-1], 'max_value': 100}])
    gauge.render_to_file("./static/images/disk/percent.svg")


def diskUsed():
    line_chart = pygal.Line(fill=True, interpolate='cubic', style=LightStyle)
    line_chart.title = 'Disk utilisation (in Mo)'
    datesFormated = getFormatedDates() # NOQA
    line_chart.x_labels = datesFormated
    hostname = getHostname()
    dates = getDates()
    for host in hostname:
        tmp = []
        aql = """
            FOR utilisation IN DISK
            FILTER utilisation.hostname == '{0}'
            RETURN utilisation.used
            """.format(host, dates)

        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
        if len(queryResult) == 0:
            tmp.append(None)
        else:
            for q in queryResult:
                tmp.append(q)

        line_chart.add(host, tmp)
    line_chart.render_to_file("static/images/disk/used.svg")


def deleteOld():
    print "deleting old graph"
    os.remove("./static/images/disk/percent.svg")
    os.remove("./static/images/disk/used.svg")


if __name__ == '__main__':
    diskPercent()
    diskUsed()
