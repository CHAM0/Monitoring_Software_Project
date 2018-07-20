#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import requests
from bs4 import BeautifulSoup as bf


def getAlerts():
    """Recuperation des alertes de securite """

    req = requests.get('http://www.cert.ssi.gouv.fr/')
    soup = bf(req.content, "lxml")

    alerts = []

    for idx, heading in enumerate(soup.find_all(
            'div', attrs={'class': 'cert-alert'})):

        if idx == 0:
            continue

        date = heading.find('span', attrs={'class': 'item-date'})
        name = heading.find('span', attrs={'class': 'item-ref'})
        obj = heading.find('span', attrs={'class': 'item-title'})
        status = heading.find('span', attrs={'class': 'item-status'})

        alerts.append([date.text, name.text, obj.text, status.text])

    return alerts


def getNotifs():
    """ Recuperation des avis de securite """

    req = requests.get('http://www.cert.ssi.gouv.fr/')
    soup = bf(req.content, "lxml")

    notifications = []

    for idx, heading in enumerate(soup.find_all(
            'div', attrs={'class': 'cert-avis'})):

        if idx == 0:
            continue

        date = heading.find('span', attrs={'class': 'item-date'})
        name = heading.find('span', attrs={'class': 'item-ref'})
        obj = heading.find('span', attrs={'class': 'item-title'})

        notifications.append([date.text, name.text, obj.text])

    return notifications
