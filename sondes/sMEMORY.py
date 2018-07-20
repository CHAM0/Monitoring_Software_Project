#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import psutil as ps


def total():
    total = ps.virtual_memory().total
    total = total / 1024 / 1024
    print("RAM total : {} Mo").format(total)
    return total


def used():
    utilisation = ps.virtual_memory().total - ps.virtual_memory().available
    utilisation = utilisation / 1024 / 1024
    print("RAM utilisée : {} Mo").format(utilisation)
    return utilisation


def available():
    available = ps.virtual_memory().available
    available = available / 1024 / 1024
    print("RAM disponible : {} Mo").format(available)
    return available


"""
if __name__ == "__main__":

    memory = ps.virtual_memory()
    active = memory.active
    inactive = memory.inactive
    print("active : {}, inactive : {}").format(active, inactive)
    print("RAM total : {} , utilisée : {} , disponible : {} ").format(total, utilisation, available) # NOQA
"""
