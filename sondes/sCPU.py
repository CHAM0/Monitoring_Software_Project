#!/usr/bin/python2.7

import psutil as ps
import os


def getHostname():
    host = os.uname()[1]
    return host


def cpuCount():
    cpu = ps.cpu_count(logical=True)
    print "\nNombre de Coeur(s) : ", cpu

    return cpu


def cpuFreq():
    cpu = ps.cpu_freq()
    print "\nInformations sur la frequence du CPU : \n"
    try:
        print "\tFrequence minimal : ", cpu.min
        print "\tFrequence maximal : ", cpu.max
        print "\tFrequence actuelle : ", cpu.current

        return cpu.min, cpu.max, cpu.current

    except Exception:
        print "no min and max frequence"
        return 0, cpu.current * 3, cpu.current


def cpuPercent():
    cpu = ps.cpu_percent(interval=2, percpu=True)
    print "\nUtilisation du CPU : \n"
    for i in range(0, len(cpu)):
        print "\tCoeur", i+1, ": ", cpu[i], "%"

    cpu = ps.cpu_percent(interval=2, percpu=False)
    return cpu


"""
if __name__ == "__main__":
    getHostname()
    cpuCount()
    cpuFreq()
    cpuPercent()
"""
