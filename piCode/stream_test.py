#!/usr/bin/env python3

import io
import time
import socket
import picamera
import picamera.array
import cv2

HOST = '128.46.96.231'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(0.2)
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format="bgr")

        image = stream.array
        cv2.imwrite("stream_mockup.png", cv2.cvtColor(stream.array, cv2.COLOR_BGR2RGB))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST< PORT))
    s.listen()

    print("Waiting for...")
    conn, addr = s.accept()
    print("connection on {}:{}".format(HOST, PORT))

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

