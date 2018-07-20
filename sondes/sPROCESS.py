#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import subprocess


def getProcessInfos():
    x = subprocess.check_output("./sPROCESS.sh", shell=True)
    mylist = x.split("\n")

    print("Nombre de processus total : {}").format(mylist[0])
    print("Nombre de processus root : {}").format(mylist[1])
    return mylist[0], mylist[1]


"""
if __name__ == "__main__":
    getProcessInfos()
"""
