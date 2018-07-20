#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import pygal
from pygal.style import LightStyle
import pyArango.connection as ac
import os

conn = ac.Connection(arangoURL='http://db:8529')
db = conn["monitoring-software-project"]
cpuColl = db["CPU"]


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
    for infos in cpuColl.fetchAll():
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


# ----------- Frequence -------------- #
def cpuFrequence():
    line_chart = pygal.Line(fill=True, interpolate='cubic', style=LightStyle)
    line_chart.title = 'CPU usage evolution (in Hz)'
    datesFormated = getFormatedDates()
    line_chart.x_labels = datesFormated
    hostname = getHostname()
    dates = getDates()
    for host in hostname:
        tmp = []
        for date in dates:
            aql = """
                FOR freq IN CPU
                FILTER freq.hostname == '{0}'
                FILTER freq.added == {1}
                RETURN freq.frequence
                """.format(host, date)

            queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
            if len(queryResult) == 0:
                tmp.append(None)
            else:
                for q in queryResult:
                    tmp.append(q)

        line_chart.add(host, tmp)
        line_chart.render_to_file("static/images/cpu/frequence.svg")


# ----------- Usage -------------- #
def cpuUsage():
    line_chart = pygal.Line(fill=True, interpolate='cubic', style=LightStyle)
    line_chart.title = 'CPU usage evolution (in %)'
    datesFormated = getFormatedDates()
    line_chart.x_labels = datesFormated
    line_chart.y_labels = map(int, {0, 25, 50, 75, 100})
    hostname = getHostname()
    dates = getDates()
    for host in hostname:
        tmp = []
        for date in dates:
            aql = """
                FOR usage IN CPU
                FILTER usage.hostname == '{0}'
                FILTER usage.added == {1}
                RETURN usage.percentage
                """.format(host, date)

            queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
            if len(queryResult) == 0:
                tmp.append(None)
            else:
                for q in queryResult:
                    tmp.append(q)

        line_chart.add(host, tmp)
        line_chart.render_to_file("static/images/cpu/usage.svg")


# -----------cores --------------#
def cpuCores():
    core_chart = pygal.Bar(height=400, fill=True, interpolate='cubic', style=LightStyle)# NOQA
    core_chart.title = "Cores"
    hostname = getHostname()
    core_chart.x_labels = hostname
    hostname = getHostname()
    cores = []
    for host in hostname:
        aql = """
            FOR core IN CPU
            FILTER core.hostname == '{0}'
            RETURN DISTINCT core.count
        """.format(host)

        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
        for q in queryResult:
            cores.append(q)

    core_chart.add("Cores", cores)
    core_chart.render_to_file("static/images/cpu/core.svg")


# ----------- Min / max --------------#
def cpuAverage():
    minMax_chart = pygal.Bar(height=400, fill=True, interpolate='cubic', style=LightStyle) # NOQA
    minMax_chart.title = "Frequence Min et Max (Hz)"
    hostname = getHostname()
    minMax_chart.x_labels = hostname

    mins = []
    maxs = []

    for host in hostname:
        aql = """
            FOR core IN CPU
            FILTER core.hostname == '{0}'
            RETURN DISTINCT core.average
        """.format(host)

        queryResult = db.AQLQuery(aql, rawResults=True, batchSize=1, count=True) # NOQA
        for q in queryResult:
            mins.append(q[0])
            maxs.append(q[1])

    minMax_chart.add("Min", mins)
    minMax_chart.add("Max", maxs)

    minMax_chart.render_to_file("static/images/cpu/average.svg")


def deleteOld():
    print "deleting old graph"
    os.remove("./static/images/cpu/average.svg")
    os.remove("./static/images/cpu/frequence.svg")
    os.remove("./static/images/cpu/usage.svg")
    os.remove("./static/images/cpu/core.svg")


if __name__ == '__main__':
    cpuFrequence()
    cpuUsage()
    cpuCores()
    cpuAverage()
