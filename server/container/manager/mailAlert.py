#!/usr/bin/python2.7
# -*- coding=utf-8 -*-


import pyArango.connection as ac
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def alert():

	# ----------- #
	send = 'jarod.duret@alumni.univ-avignon.fr'
	recv = 'jarod8405@gmail.com'
	cpuLimit = 90  # (%)
	ramLimit = 7100  # (Mo)
	# ----------- #

	conn = ac.Connection(arangoURL='http://db:8529')
	db = conn["monitoring-software-project"]
	cpu = db["CPU"]
	ram = db["MEMORY"]

	message = "Alerts has been detected\n"
	haveToSend = False
	for i in cpu.fetchAll():
		if i['percentage'] > cpuLimit:
			message += "\n" + i["hostname"]+" - overused CPU at "+str(i["added"])
			haveToSend = True

	for i in ram.fetchAll():
		if i["used"] > ramLimit:
			message += "\n" + i["hostname"] + " - overused RAM at " + str(i["added"])
			haveToSend = True

	if haveToSend:
		print "sending alert message"
		msg = MIMEMultipart()
		msg['from'] = send
		msg['to'] = recv
		msg['subject'] = 'Probleme parc informatique'
		msg.attach(MIMEText(message))
		mailserver = smtplib.SMTP_SSL('smtpz.univ-avignon.fr:465')
		mailserver.ehlo()
		mailserver.login('jarod.duret@alumni.univ-avignon.fr', 'Moiseul84')
		mailserver.sendmail(send, recv, msg.as_string())
		mailserver.close()
