#!/usr/bin/env python3

import socket
import netfaces as ni
import nmap

from src.piCode.streamwrite import pi_client as pstr

def getConnection(ipaddress='10.3.141.198', port=8000):
        connect = socket.socket()
        connect.connect((ipaddress, port))

def getWriteSocs(connection):
    send = connect.makefile('wb')
    recv = connect.makefile('rb')

    return (send, recv)

def sendFrames(connect=None):
    pass

def readResults(connect=None):
    pass

def closeWriteFiles(send, recv):
    send.close()
    recv.close()

def closeConnection(connection):
    connection.close()

def findIPaddress():
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