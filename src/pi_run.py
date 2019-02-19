#!/usr/bin/env python3

import socket
import netifaces as ni
import nmap

from src.piCode.streamwrite import pi_client as pstr

def getConnection(ipaddress='10.3.141.198', port=8000):
    connect = socket.socket()
    connect.connect((ipaddress, port))

    return connect

def getWriteSocs(conn):
    send = conn.makefile('wb')
    recv = conn.makefile('rb')

    return (send, recv)

def sendFrames(connect=None, ipaddress='10.3.141.198', port=8000):
    pstr.runConnect(connect=connect, ipaddress=ipaddress, port=port)

def readResults(connect=None, ipaddress='10.3.141.198', port=8000):
    return pstr.runRead(connect=connect, ipaddress=ipaddress, port=8000)

def closeWriteSocs(send, recv):
    send.close()
    recv.close()

def closeConnection(connection):
    connection.close()

def findConnectedIPaddress():
    if not WIFI is None:
        ip = ni.ifaddresses(WIFI)[ni.AF_INET][0]['addr']
        nm = nmap.PortScanner()

        nm.scan(ip+"/24")
        hosts = nm.all_hosts()
        print(hosts)

        while ip in hosts:
            hosts.remove(ip)
        
        print(hosts)
        if len(hosts):
            return hosts[0] # No good way to tell if > 1... cross fingers

    # If here, no idea what to do, default to Ian's Ubuntu?    
    return '10.3.141.198'
