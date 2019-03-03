#!/usr/bin/env python3

import bluetooth as blt
import socket
import netifaces as ni
import time
import nmap

try:
    from src.piCode.streamwrite import pi_client as pstr
except:
    from piCode.streamwrite import pi_client as pstr

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

# Bluetooth
def sendResBluetooth(passing, bconn, good="p", bad="f"):
    if passing:
        sendBlueMessage(bconn, good) # send "p"ass
    else:
        sendBlueMessage(bconn, bad) # send ""

def lookUpNearbyBluetoothDevices(wanted, printOuts=False):
    res = []

    if printOuts:
        print("Searching for Bluetooth devices...")
    nearby = blt.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
    if printOuts:
        print("There are {} devices nearby:".format(len(nearby)))

    for addr, name in nearby:
        if printOuts:
            print("{} found at {}".format(name, addr)) 
        
        if name == wanted:
            res.append({"address": addr, "name": name})
    
    return res  # None if device wasn't found

# "98:D3:71:FD:50:9E" for HC-05, if not given, find dynamically
def getBlueConnection(mac, dname="HC-05", port=1):
    # BluetoothError raised on Disconnect
    while mac is None:
        mac = lookUpNearbyBluetoothDevices(dname)

    sock = blt.BluetoothSocket( blt.RFCOMM )
    sock.connect((mac, port))

    return sock

def sendBlueMessage(bconn, message):
    bconn.send(message)

def getBlueMessage(bconn):
    data = ' '
    res = ''

    while data[-1] != '\n':
        time.sleep(.1)
        data = sock.recv(1024)

        try:
            data = data.decode('utf-8')
        except:
            continue
        
        # if newline not present, assume bad message
        res += "".join(data.splitlines())
    
    return res

def waitForBlueMessage(bconn, desired):
    data = getBlueMessage(bconn)

    while desired not in data:
        time.sleep(.5)
        print("~~~")
        data = getBlueMessage(bconn)
        print(data)
    
    return desired


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

if __name__ == "__main__":
    # testing Bluetooth
    # a = lookUpNearbyBluetoothDevices("HC-05", printOuts=True)
    a = [{'address': '98:D3:71:FD:50:9E', 'name': 'HC-05'}]

    if len(a):
        a = a[0]
        sock = getBlueConnection(a['address'], dname=a['name'])

        print("sending message...")
        sendBlueMessage(sock, "h")
        print("getting message...")
        mess = waitForBlueMessage(sock, 'boot')
        print(mess)
    else:
        print("Badness, HC-05 not found")
