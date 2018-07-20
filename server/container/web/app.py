#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import init
import flask
import pyArango.connection as ac
import datetime
import time
import cpuGraph
import memoryGraph
import diskGraph
import otherGraph

time.sleep(5)
init.init()

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
conn = ac.Connection(arangoURL='http://db:8529')

try:
    db = conn.createDatabase(name="monitoring-software-project")
    cpuColl = db.createCollection(name="CPU")
    memoryColl = db.createCollection(name="MEMORY")
    diskColl = db.createCollection(name="DISK")
    networkColl = db.createCollection(name="NETWORK")
    processColl = db.createCollection(name="PROCESS")
    sensorsColl = db.createCollection(name="SENSORS")
    alertsColl = db.createCollection(name="ALERTS")
    notificationsColl = db.createCollection(name="NOTIFICATIONS")

except Exception:
    print("erreur dans la matrice")

finally:
    db = conn["monitoring-software-project"]
    cpuColl = db["CPU"]
    memoryColl = db["MEMORY"]
    diskColl = db["DISK"]
    networkColl = db["NETWORK"]
    processColl = db["PROCESS"]
    sensorsColl = db["SENSORS"]
    alertsColl = db["ALERTS"]
    notificationsColl = db["NOTIFICATIONS"]


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0' # NOQA
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/sonde/scpu', methods=['GET', 'POST'])
def cpu():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        doc = cpuColl.createDocument()
        doc["hostname"] = json_dict['hostname']
        doc["count"] = json_dict['count']
        doc["frequence"] = json_dict['frequence']
        doc["average"] = json_dict['min-max']
        doc["percentage"] = json_dict['percentage']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        try:
            cpuGraph.deleteOld()
        except Exception:
            print " no cpu graph "

        cpuGraph.cpuUsage()
        cpuGraph.cpuCores()
        cpuGraph.cpuFrequence()
        cpuGraph.cpuAverage()

        # request response
        key = json_dict['hostname']
        data = {'hostname': key,
                'msg': "cpu info added"}
        return flask.jsonify(data)

    return "No json data sent"


@app.route('/sonde/smemory', methods=['GET', 'POST'])
def memory():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        doc = memoryColl.createDocument()
        doc["hostname"] = json_dict['hostname']
        doc["total"] = json_dict['total']
        doc["used"] = json_dict['used']
        doc["available"] = json_dict['available']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        try:
            memoryGraph.deleteOld()
        except Exception:
            print " no cpu graph "

        memoryGraph.memoryUsed()
        memoryGraph.memoryTotal()

        # request response
        key = json_dict['hostname']
        data = {'hostname': key,
                'msg': "memory info added"}
        return flask.jsonify(data)

    return "No json data send"


@app.route('/sonde/sdisk', methods=['GET', 'POST'])
def disk():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        doc = diskColl.createDocument()
        doc["hostname"] = json_dict['hostname']
        doc["total"] = json_dict['total']
        doc["used"] = json_dict['used']
        doc["free"] = json_dict['free']
        doc["percent"] = json_dict['percent']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        try:
            diskGraph.deleteOld()
        except Exception:
            print " no diskgraph "

        diskGraph.diskPercent()
        diskGraph.diskUsed()
        # request response
        key = json_dict['hostname']
        data = {'hostname': key,
                'msg': "disk info added"}
        return flask.jsonify(data)

    return "No json data send"


@app.route('/sonde/snetwork', methods=['GET', 'POST'])
def network():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        doc = networkColl.createDocument()
        doc["hostname"] = json_dict['hostname']
        doc["sent"] = json_dict['sent']
        doc["recv"] = json_dict['recv']
        doc["psent"] = json_dict['psent']
        doc["precv"] = json_dict['precv']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        try:
            otherGraph.deleteNet()
        except Exception:
            print " no diskgraph "

        otherGraph.networkInfos()

        # request response
        key = json_dict['hostname']
        data = {'hostname': key,
                'msg': "network info added"}
        return flask.jsonify(data)

    return "No json data send"


@app.route('/sonde/sprocess', methods=['GET', 'POST'])
def process():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        doc = processColl.createDocument()
        doc["hostname"] = json_dict['hostname']
        doc["total"] = json_dict['total']
        doc["root"] = json_dict['root']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        try:
            otherGraph.deleteProc()
        except Exception:
            print " no diskgraph "

        otherGraph.processInfos()
        # request response
        key = json_dict['hostname']
        data = {'hostname': key,
                'msg': "process info added"}
        return flask.jsonify(data)

    return "No json data send"


@app.route('/sonde/ssensors', methods=['GET', 'POST'])
def sensors():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        doc = sensorsColl.createDocument()
        doc["hostname"] = json_dict['hostname']
        doc["time"] = json_dict['time']
        doc["temperature"] = json_dict['temperature']
        doc["kernel"] = json_dict['kernel']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        # request response
        key = json_dict['hostname']
        data = {'hostname': key,
                'msg': "sensors info added"}
        return flask.jsonify(data)

    return "No json data send"


@app.route('/cert/alerts', methods=['GET', 'POST'])
def alerts():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        for infos in alertsColl.fetchAll():
            if infos["name"] == json_dict['name']:
                key = json_dict['name']
                data = {'nom': key,
                        'msg': "alert already stocked"}
                return flask.jsonify(data)

        doc = alertsColl.createDocument()
        doc["date"] = json_dict['date']
        doc["name"] = json_dict['name']
        doc["obj"] = json_dict['obj']
        doc["status"] = json_dict['status']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        # request response
        key = json_dict['name']
        data = {'nom': key,
                'msg': "alert added"}
        return flask.jsonify(data)

    return "No json data send"


@app.route('/cert/notifications', methods=['GET', 'POST'])
def notifications():
    if flask.request.method == "POST":
        json_dict = flask.request.get_json()
        date = datetime.datetime.now()

        for infos in notificationsColl.fetchAll():
            if infos["name"] == json_dict['name']:
                key = json_dict['name']
                data = {'nom': key,
                        'msg': "notification already stocked"}
                return flask.jsonify(data)

        doc = notificationsColl.createDocument()
        doc["date"] = json_dict['date']
        doc["name"] = json_dict['name']
        doc["obj"] = json_dict['obj']
        doc["added"] = date.month, date.day, date.hour, date.minute
        # doc._key = json_dict['hostname']
        doc.save()

        # request response
        key = json_dict['name']
        data = {'nom': key,
                'msg': "notification added"}
        return flask.jsonify(data)

    return "No json data send"


@app.route('/bdd')
def bdd():
    return flask.redirect("http://localhost:5002", code=302)


@app.route('/')
def index():
    alerts = alertsColl.fetchAll()
    notifications = notificationsColl.fetchAll()
    return flask.render_template('index.html', alerts=alerts, notifications=notifications) # NOQA


@app.route('/cpu-memory')
def cpuMem():
    return flask.render_template('cpu.html')


@app.route('/disks')
def disks():
    return flask.render_template('disk.html')


@app.route('/others-informations')
def others():
    return flask.render_template('network.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
