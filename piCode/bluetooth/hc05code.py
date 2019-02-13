import bluetooth
import sys
bd_addr = "98:D3:71:FD:50:9E"

port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))
print("Connected")

while True:
    sock.send('hello world!')

'''
count = 0

while count<10:
    data = sock.recv(12)
    print("Received: {}".format(data))

    count += 1
'''
sock.close()
