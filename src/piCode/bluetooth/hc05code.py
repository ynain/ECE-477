import bluetooth
import sys
import time
BD_ADDR = "98:D3:71:FD:50:9E"


def sendMessageTo(message, looped=False):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((BD_ADDR, port))
    print("Connected")

    while True:
        sock.send(message)
        if not looped:
            break

    sock.close()

def receiveMessageFrom(looped=False):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((BD_ADDR, port))
    print("Connected")

    data = sock.recv(1024)
    data = data.decode('utf-8')
    while True:
        print(data)
        if not looped:
            break

    sock.close()


receiveMessageFrom(looped=True)

