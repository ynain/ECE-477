#!/usr/bin/env python3

import io
import time
import socket
import picamera
import picamera.array
import cv2

HOST = '128.46.96.231'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print("Waiting for...")
conn, addr = s.accept()
print("connection on {}:{}".format(HOST, PORT))

with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(0.2)

    start = time.time()
    # for _ in range(24):
    camera.capture(s, 'png')
    
"""
with conn:
    print('Connected by', addr)
    
    conn.sendall(data)
"""
finish = time.time()
s.close()

print("{} seconds for {} fps".format(finish - start, 24.0 / finish-start))

