"""
Found from https://gist.github.com/keithweaver/3d5dbf38074cee4250c7d9807510c7c3
    1/27/2019
"""

# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

import bluetooth
import time
import cv2

def receiveMessages():
    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 0x1001
    server_sock.bind(("",port))
    server_sock.listen(1)

    print("Listening for connections...")

    import re, uuid 
    print(':'.join(re.findall('..', '%012x' % uuid.getnode())).encode())

    client_sock,address = server_sock.accept()
    print("Accepted connection from {}".format(address))

    data = client_sock.recv(1024)
    print("received {}".format(data))

    client_sock.close()
    server_sock.close()
  
def sendMessageTo(targetBluetoothMacAddress):
    port = 1
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((targetBluetoothMacAddress, port))

    send = "Connected?"
    key = 1

    while not key == ord('q'):
        sock.send(key)

        key = cv2.waitKey(50)
        if key == -1:
            key = "nothing"
        send = "Pressed {}".format(key)
        print(send)


    #sock.send("EVAN+JAMES1234")
    #sock.send("E3")
    #sock.send("ABCDEFGHIJ")
    sock.close()
  
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
    
if __name__ == "__main__":
    # wanted = lookUpNearbyBluetoothDevices("Galaxy Note8")
    wanted = lookUpNearbyBluetoothDevices("HC-05")

    print("\n\n")
    
    if not len(wanted):
        print("No devices found to connect to")
    else:
        for el in wanted:
            try:
                print("Trying to connect to {} at {}".format(el["name"], el["address"]))
                sendMessageTo(el["address"])
            except Exception as e:
                print(e)
                print("Connection unsuccessful?")

#    receiveMessages()
