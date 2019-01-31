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

class ImageStreamer(threading.Thread):
    def __init__(self):
        super(ImageStreamer, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a background thread
        while not self.terminated:
            # Wait for the image to be written to the stream
            if self.event.wait(.5):
                try:
                    with connection_lock:
                        connection.write(struct.pack('<L', self.stream.tell()))
                        connection.flush()
                        self.stream.seek(0)
                        connection.write(self.stream.read())
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    with pool_lock:
                        pool.append(self)

def streams():
    global count, finish
    while finish - start < 2:
        with pool_lock:
            if pool:
                streamer = pool.pop()
            else:
                streamer = None
        if streamer:
            yield streamer.stream
            streamer.event.set()
            count += 1
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)
        finish = time.time()
def runConnect():
    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    conn, addr = server_socket.accept()
    connection = conn.makefile('wb')

    try:
        connection_lock = threading.Lock()
        pool_lock = threading.Lock()
        pool = []

        count = 0
        start = time.time()
        finish = time.time()

        with picamera.PiCamera() as camera:
            pool = [ImageStreamer() for i in range(4)]
            close = copy.copy(pool)
            camera.resolution = (640, 480)
            camera.framerate = 4.4 
            time.sleep(1)
            start = time.time()
            camera.capture_sequence(streams(), 'jpeg', use_video_port=True)

        # Shut down the streamers in an orderly fashion
        while close:
            streamer = close.pop()
            streamer.terminated = True
            streamer.join()

        # Write the terminating 0-length to the connection to let the server
        # know we're done
        with connection_lock:
            connection.write(struct.pack('<L', 0))

    finally:
        connection.close()
        server_socket.close()

    print('Sent %d images in %d seconds at %.2ffps' % (
        count, finish-start, count / (finish-start)))

if __name__ == "__main__":
    runConnect()