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
import re, uuid

def receiveMessages(name="rovian", uuid="d01ca4aa-c79d-43c5-94eb-a7fc4e7fa748"):
    port = bluetooth.get_available_port( bluetooth.RFCOMM )
    server_sock.bind(("", port))
    server_sock.listen(1)
    print("Listening on port {}".format(port))

    print("Listening for connections on {}...".format(
        ':'.join(re.findall('..', '%012x' % uuid.getnode())).encode()
    ))

    bluetooth.advertise_service( server_sock, name, uuid )
    sock, address = server_sock.accept()
    bluetooth.stop_advertising( sock )

    print("Connected!\n   {}".format(address))

    data = sock.recv(1024)
    print("received {}".format(data))

    sock.close()
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
    """
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
    """
    receiveMessages()
