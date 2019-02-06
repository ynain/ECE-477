"""
    This file found and edited from documentation for picamera
    https://picamera.readthedocs.io/en/release-1.10/recipes2.html?highlight=socket#rapid-capture-and-streaming

    Pi wifi-hotspot enabled via hostapd and RaspAP
    https://howtoraspberrypi.com/create-a-wi-fi-hotspot-in-less-than-10-minutes-with-pi-raspberry/
"""

import io
import socket
import struct
import copy
import time
import threading
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
        finally:
            self.stream.seek(0)
            self.stream.truncate()
    
    def end(self):
        self.connection.write(struct.pack('<L', 0))

def frameGenerator(connection, frame, sender, captureTime=2):
    while frame['finish'] - frame['start'] < captureTime:
        yield sender
        frame["count"] += 1
        frame['finish'] = time.time()

def runConnect(client_socket=None, ipaddress='10.3.141.198', port=8000):
    if client_socket is None:
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        client_socket = socket.socket()
        client_socket.connect((ipaddress, port))

    # Instigate a single connection and make a file-like object out of it
    connection = client_socket.makefile('wb')

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
        connection.close()

        if connect is None: # If the connection was made internally, close all
            client_socket.close()

    print('Sent %d images in %d seconds at %.2ffps' % (
        measure['count'], measure['finish']-measure['start'], measure['count'] / (measure['finish']-measure['start'])))

def runRead(connect=None, ipaddress='10.3.141.198', port=8000):
    if connect is None:
        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        client_socket = socket.socket()
        client_socket.connect((ipaddress, port))

    # Instigate a single connection and make a file-like object out of it
    connection = connect.makefile('rb')

    try:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            image_len = 0
        

        res = struct.unpack('<s', image_stream.read(image_len))

        print(res)

    finally:
        connection.close()

        if connect is None: # If the connection was made internally, close all
            client_socket.close()

    print('Sent %d images in %d seconds at %.2ffps' % (
        measure['count'], measure['finish']-measure['start'], measure['count'] / (measure['finish']-measure['start'])))

if __name__ == "__main__":
    client_socket = socket.socket()

    runConnect(client_socket=client_socket)

    client_socket.close()

