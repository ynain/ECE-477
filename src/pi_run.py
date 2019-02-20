#!/usr/bin/env python3

import bluetooth as blt
import socket
import netifaces as ni
import nmap

from src.piCode.streamwrite import pi_client as pstr

# WiFi/Internet
def getServerConnection(ipaddress='10.3.141.198', port=8000):
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

# Result Evaluation
def evaluateImages(res, thresh=0.75):
    passing = 0

    for key in res:
        if res[key] > thresh:
            pasing += 1
        
    if passing == 1:    # if one person matches
        return True
    else:               # No matches == multiple matches == doesn't pass
        return False

def sendResBluetooth(passing, bconn, good="p", bad="f"):
    if passing:
        sendBlueMessage(bconn, good) # send "p"ass
    else:
        sendBlueMessage(bconn, bad) # send ""

# Bluetooth
def lookUpNearbyBluetoothDevices(wanted):
    res = []

    print("Searching for Bluetooth devices...")
    nearby = bluetooth.discover_devices(duration=4, lookup_names=True, flush_cache=True, lookup_class=False)
    print("There are {} devices nearby:".format(len(nearby)))

    for addr, name in nearby:
        print("{} found at {}".format(name, addr)) 
        
        if name == wanted:
            res.append({"address": addr, "name": name})
    
    return res  # None if device wasn't found

# "98:D3:71:FD:50:9E" for HC-05, if not given, find dynamically
def getBlueConnection(dname="HC-05", mac=None, port=1):
    # BluetoothError raised on Disconnect
    while mac is None:
        mac = lookUpNearbyBluetoothDevices(dname)

    sock = blt.BluetoothSocket( blt.RFCOMM )
    sock.connect((mac, port))


def sendBlueMessage(bconn, message):
    print(message)

def getBlueMessage(bconn):
    res = ''

    while res[-1] != '\n':


# IP address being dynamic... and slow
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
