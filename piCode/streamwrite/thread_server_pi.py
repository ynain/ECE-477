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
        print(sendStuff)
        try:
            self.stream.write(sendStuff)
            self.connection.write(struct.pack('<L', self.stream.tell()))
            self.connection.flush()
            
            self.stream.seek(0)
            connection.write(self.stream.read())
        finally:
            self.stream.seek(0)
            self.stream.truncate()
    
    def end(self):
        self.connection.write(struct.pack('<L', 0))

def frameGenerator(connection, frame, sender, time=2):
    while frame['finish'] - frame['start'] < 2:
        yield sender
        frame["count"] += 1
        frame['finish'] = time.time()

def runConnect():
    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    conn, addr = server_socket.accept()
    connection = conn.makefile('wb')

    measure = {
        'start': time.time(),
        'finish': time.time(),
        'count': 0
    }

    try:

        sender = writeSingleImage(connection)

        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 4.4 
            time.sleep(1)
            camera.capture_sequence(frameGenerator(connection, measure, sender), 'jpeg', use_video_port=True)

        # Write the terminating 0-length to the connection to let the server
        # know we're done
        sender.end()

    finally:
        connection.close()
        server_socket.close()

    print('Sent %d images in %d seconds at %.2ffps' % (
        measure['count'], measure['finish']-measure['start'], measure['count'] / (measure['finish']-measure['start'])))

if __name__ == "__main__":
    runConnect()