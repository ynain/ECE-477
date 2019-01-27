"""
Found from
    1/27/2019
"""

# Uses Bluez for Linux
#
# sudo apt-get install bluez python-bluez
# 
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/x232.html
# Taken from: https://people.csail.mit.edu/albert/bluez-intro/c212.html

import bluetooth

def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  
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
  sock.send("hello!!")
  sock.close()
  
def lookUpNearbyBluetoothDevices(wanted):
    print("Searching for Bluetooth devices...")
    nearby = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
    print("There are {} devices nearby:".format(len(nearby)))

    res = None

    for addr, name in nearby:
        if name == wanted:
            res = {"address": addr, "name": name}
    
    return res  # None if device wasn't found
    
if __name__ == "__main__":
    wanted = lookUpNearbyBluetoothDevices("Galaxy Note8")

    print("{} found at {}".format(wanted["name"], wanted["address"])) 
    
    sendMessageTo(wanted["address"])
