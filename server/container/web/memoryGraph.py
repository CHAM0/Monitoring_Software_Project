#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import pygal
from pygal.style import LightStyle
import pyArango.connection as ac
import os

conn = ac.Connection(arangoURL='http://db:8529')
db = conn["monitoring-software-project"]
memoryColl = db["MEMORY"]


# get all hostname
def getHostname():
    hostname = []
    aql = "FOR doc IN CPU RETURN DISTINCT doc.hostname"
    queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
    for key in queryResult:
        hostname.append(str(key))
    return hostname


# Get all hours
def getDates():
    dates = []
    for infos in memoryColl.fetchAll():
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


# ----------- Memory Used -------------- #
def memoryUsed():
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=LightStyle)  # NOQA
    line_chart.title = 'RAM utilisation (in Mo)'
    datesFormated = getFormatedDates()
    line_chart.x_labels = datesFormated
    hostname = getHostname()
    dates = getDates()
    for host in hostname:
        tmp = []
        aql = """
            FOR utilisation IN MEMORY
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
    line_chart.render_to_file("static/images/memory/used.svg")


def deleteOld():
    print "deleting old graph"
    os.remove("./static/images/memory/used.svg")
    os.remove("./static/images/memory/total.svg")


# -----------cores --------------#
def memoryTotal():
    core_chart = pygal.Bar(height=400, fill=True, interpolate='cubic', style=LightStyle) # NOQA
    core_chart.title = "RAM"
    hostname = getHostname()
    core_chart.x_labels = hostname
    cores = []
    for host in hostname:
        aql = """
            FOR ram IN MEMORY
            FILTER ram.hostname == '{0}'
            RETURN DISTINCT ram.total
        """.format(host)

        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
        for q in queryResult:
            cores.append(q)

    core_chart.add("Cores", cores)
    core_chart.render_to_file("static/images/memory/total.svg")


if __name__ == '__main__':
    memoryUsed()
    memoryTotal()
