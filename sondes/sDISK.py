#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import psutil as ps


def total():
    disk = ps.disk_usage("/")
    total = disk.total / 1024 / 1024 / 1024
    print("Espace de / total : {} Go").format(total)
    return total


def used():
    disk = ps.disk_usage("/")
    used = disk.used / 1024 / 1024 / 1024
    print("Espace de / utilisé : {} Go").format(used)
    return used


def free():
    disk = ps.disk_usage("/")
    free = disk.free / 1024 / 1024 / 1024
    print("Espace de / disponible : {} Go").format(free)
    return free


def percent():
    disk = ps.disk_usage("/")
    percent = disk.percent
    print("Espace de / utilisé en % : {}").format(percent)
    return percent


"""
if __name__ == "__main__":
    print(total())
    print(used())
    print(free())
    print(percent())
"""
