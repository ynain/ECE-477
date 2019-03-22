"""
    This file found and edited from documentation for picamera
    https://picamera.readthedocs.io/en/release-1.10/recipes2.html?highlight=socket#rapid-capture-and-streaming

    Pi wifi-hotspot enabled via hostapd and RaspAP
    https://howtoraspberrypi.com/create-a-wi-fi-hotspot-in-less-than-10-minutes-with-pi-raspberry/
"""

import io
import socket
import struct
import json
import copy
import time
import picamera

class writeSingleImage():
    def __init__(self, connection):
        self.stream = io.BytesIO()
        self.connection = connection
    
    def write(self, sendStuff):
        # print(sendStuff)
        try:
            self.stream.write(sendStuff)
            self.connection.write(struct.pack('<L', self.stream.tell()))
            self.connection.flush()
            
            self.stream.seek(0)
            self.connection.write(self.stream.read())
            self.connection.flush()
        finally:
            self.stream.seek(0)
            self.stream.truncate()
    
    def end(self):
        self.connection.write(struct.pack('<L', 0))
        self.connection.flush()

def frameGenerator(connection, frame, sender, captureTime=2):
    while frame['finish'] - frame['start'] < captureTime:
        yield sender
        frame["count"] += 1
        frame['finish'] = time.time()

def runConnect(connect=None, ipaddress='10.3.141.198', port=8000):
    if connect is None:
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        connect = socket.socket()
        connect.connect((ipaddress, port))
        connect = connect.makefile('wb')

    # Instigate a single connection and make a file-like object out of it
    connection = connect

    measure = {
        'start': time.time(),
        'finish': time.time(),
        'count': 0
    }

    try:

        sender = writeSingleImage(connection)

        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 32 
            time.sleep(1)
            camera.capture_sequence(frameGenerator(connection, measure, sender), 'jpeg', use_video_port=True)

        # Write the terminating 0-length to the connection to let the server
        # know we're done
        sender.end()

    finally:
        if connect is None: # If the connection was made internally, close all
            connection.close()
            client_socket.close()

    print('Sent %d images in %d seconds at %.2ffps' % (
        measure['count'], measure['finish']-measure['start'], measure['count'] / (measure['finish']-measure['start'])))

def runRead(connect=None, ipaddress='10.3.141.198', port=8000):
    if connect is None:
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        conn = socket.socket()
        conn.connect((ipaddress, port))
        connect = conn.makefile('rb')

    # Instigate a single connection and make a file-like object out of it
    connection = connect

    res = {}

    try:
        json_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not json_len:
            json_len = 0

        res = connection.read(json_len)
        res = json.loads(res.decode('utf-8'))

    finally:
        if connect is None: # If the connection was made internally, close all
            connection.close()
            conn.close()

    return res


if __name__ == "__main__":
    client_socket = socket.socket()
    client_socket.connect(('10.3.141.198', 8000))
    connect = client_socket.makefile('rb')

    runConnect(client_socket=connect)

    client_socket.close()
    connect.close()

