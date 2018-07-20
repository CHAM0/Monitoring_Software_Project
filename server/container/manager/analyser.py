#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import parser
import requests


def checkCERT():
    """ maj de la bdd avec le site CERT """

    alerts = parser.getAlerts()
    for a in alerts:
        alert = {
            "date": a[0],
            "name": a[1],
            "obj": a[2],
            "status": a[3]}

        url = 'http://web:80/cert/alerts'
        req = requests.post(url, json=alert)
        print(req.text)

    notifs = parser.getNotifs()
    for n in notifs:
        notif = {
            "date": n[0],
            "name": n[1],
            "obj": n[2]}

        url = 'http://web:/cert/notifications'
        req = requests.post(url, json=notif)
        print(req.text)


