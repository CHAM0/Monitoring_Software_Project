#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import psutil as ps

Network = ps.net_io_counters()


def getInfos():
    sent = Network.bytes_sent / 1024 / 1024
    recv = Network.bytes_recv / 1024 / 1024
    psent = Network.packets_sent / 1024 / 1024
    precv = Network.packets_recv / 1024 / 1024

    print("Bytes envoyés {} Mo, Bytes reçus : {} Mo, Paquets envoyés : {} , Paquets reçus : {}").format(sent, recv, psent, precv) # NOQA
    return [sent, recv, psent, precv]


"""
if __name__ == "__main__":


print("snetio :: Bytes envoyés {} Mo, Bytes reçus : {} Mo, Paquets envoyés : {} , Paquets reçus : {}").format(sent, recv, psent, precv) # NOQA
"""
