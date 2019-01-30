"""
    This file found and edited from documentation for picamera
    https://picamera.readthedocs.io/en/release-1.10/recipes2.html?highlight=socket#rapid-capture-and-streaming

    Pi wifi-hotspot enabled via hostapd and RaspAP
    https://howtoraspberrypi.com/create-a-wi-fi-hotspot-in-less-than-10-minutes-with-pi-raspberry/
"""

import io
import socket
import struct
import time
import threading
import picamera

class ImageStreamer(threading.Thread):
    def __init__(self, pool, pool_lock, connection_lock, connection):
        super(ImageStreamer, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

        # Initializing shared variables (shallow copies... hopefully. Fingers crossed)
        self.pool = pool
        self.pool_lock = pool_lock
        self.connection_lock = connection_lock
        self.connection = connection

    def run(self):
        # This method runs in a background thread
        while not self.terminated:
            # Wait for the image to be written to the stream
            if self.event.wait(.5):
                try:
                    with self.connection_lock:
                        self.connection.write(struct.pack('<L', self.stream.tell()))
                        self.connection.flush()
                        self.stream.seek(0)
                        self.connection.write(self.stream.read())
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    with pool_lock:
                        self.pool.append(self)

class connectToClient():
    def __init__(self, ip='0.0.0.0', port=8000, framerate=4.4, seconds=2):
        self.framerate = framerate
        self.seconds = seconds

        # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
        # all interfaces)
        self.server_socket = socket.socket()
        self.server_socket.bind((ip, port))
        self.server_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        self.conn, self.addr = server_socket.accept()
        self.connection = self.conn.makefile('wb')

        # Initialize blank variables for later
        self.connection_lock = None
        self.pool_lock = None
        self.pool = None

        self.count = None
        self.start = None
        self.finish = None

        self.runLoad()

    # Process to run the streams 
    def streams(self):
        while self.finish - self.start < self.seconds:
            with self.pool_lock:
                if self.pool:
                    streamer = self.pool.pop()
                else:
                    streamer = None
            if streamer:
                yield streamer.stream
                streamer.event.set()
                self.count += 1
            else:
                # When the pool is starved, wait a while for it to refill
                time.sleep(0.1)
            self.finish = time.time()
    
    def runLoad(self):
        try:
            self.connection_lock = threading.Lock()
            self.pool_lock = threading.Lock()
            self.pool = []

            self.count = 0
            self.start = time.time()
            self.finish = time.time()

            # Load the camera and run the streaming process
            with picamera.PiCamera() as camera:
                self.pool = [ImageStreamer(self.pool, self.pool_lock, self.connection_lock, self.connection) for _ in range(4)]
                camera.resolution = (640, 480)
                camera.framerate = self.framerate 
                time.sleep(1)
                self.start = time.time()
                camera.capture_sequence(self.streams(), 'jpeg', use_video_port=True)

            # Shut down the streamers in an orderly fashion
            while self.pool:
                streamer = self.pool.pop()
                streamer.terminated = True
                streamer.join()

            # Write the terminating 0-length to the connection to let the server
            # know we're done
            with self.connection_lock:
                self.connection.write(struct.pack('<L', 0))
        
        finally:
            self.connection.close()
            self.server_socket.close()

        print('Sent %d images in %d seconds at %.2ffps' % (
            self.count, self.finish-self.start, self.count / (self.finish-self.start)))




if __name__ == "__main__":
    goDo = connectToClient()
    