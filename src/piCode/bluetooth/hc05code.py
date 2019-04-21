import bluetooth
import signal
import sys
import time
#BD_ADDR = "98:D3:71:FD:50:9E"
BD_ADDR = "20:19:02:13:00:89"

def closeSocket(socket):
    def signal_handler(sig, frame):
        print("\nCtrl+C signal sensed!\nClosing the socket...")
        socket.close()
        sys.exit(0)

    return signal_handler


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

def sendAndReceive(message, looped=True):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((BD_ADDR, port))
    print("Connected")

    msg = ''
    signal.signal(signal.SIGINT, closeSocket(sock))

    
    while True:
        data = (sock.recv(16)).decode('utf-8')
        msg += data
        #print(msg)
        if msg[-1] == '\n':
            break

    msg = "".join(msg.splitlines())
    print(msg)


    if message in ['l', 'p', 'f']:
        sock.send(message)
        print("sent " + message)
        return
    
    if msg.strip().find('start') != -1 or msg.strip().find('boot') != -1:
        sock.send('c')
        print('sent c')
        return

    '''
    sock.send(message)
    #print('sent?')
    #time.sleep()
    data = (sock.recv(1024)).decode('utf-8')
    msg = ''

    #while data != '\n':
    while True:
        data = (sock.recv(32)).decode('utf-8')
        msg += data
        #print(msg)
        if msg[-1] == '\n':
            break

    print(msg)
    '''
    sock.close()

        
sendAndReceive(sys.argv[1], looped=False)
#sendMessageTo('0')
#receiveMessageFrom(looped=True)

