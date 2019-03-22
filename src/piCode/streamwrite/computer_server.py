"""
    This file found and edited from documentation for picamera
    https://picamera.readthedocs.io/en/release-1.10/recipes2.html?highlight=socket#rapid-capture-and-streaming
"""

import io
import os
import json
import socket
import struct
import cv2
import numpy as np

def getImages(connect=None, path='./frames/', ipaddress='0.0.0.0', port='8000', printing=False, log=False):
    if connect is None:
        # Make a socket connection that can be written to
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ipaddress, port))
        server_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        conn, addr = server_socket.accept()
        connect = conn.makefile('rb')
    
    connection = connect    # Unify paths

    if log:
        print("Receiving files...")

    count = 0
    images = []

    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            images.append(cv2.imdecode(np.asarray(bytearray(image_stream.read(image_len)), dtype=np.uint8), cv2.IMREAD_COLOR))

            # print('Image is %dx%d' % image.shape[0:2])
            count += 1
    finally:
        if log:
            print("{} images received\n".format(count))

        if printing:
            for i in range(len(images)):
                imgname = os.path.join(path,"frame{}.jpg".format(i))
                cv2.imwrite(imgname, images[i])
                # print(imgname)
            print("Images saved")

        if connect is None: # If the connection was made internally, close all
            connection.close()
            conn.close()
            server_socket.close()
    
    return images

def sendResult(jsonpackage, connect=None, ipaddress='0.0.0.0', port='8000', log=False):
    if connect is None:
        # Make a socket connection that can be written to
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ipaddress, port))
        server_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        conn, addr = server_socket.accept()
        connect = conn.makefile('wb')
    
    connection = connect    # Unify paths

    if log:
        print("Sending results...")

    count = 0
    images = []

    try:
        stream = io.BytesIO()
        stream.write(json.dumps(jsonpackage, sort_keys=True).encode('utf-8'))
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()

        stream.seek(0)
        connection.write(stream.read())
        connection.flush()

        if log:
            print("Sent")

    finally:
        if connect is None: # If the connection was made internally, close all
            connection.close()
            conn.close()
            server_socket.close()
    
    return images


if __name__ == "__main__":
    # Make a socket connection that can be written to
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    conn, addr = server_socket.accept()
    connect = conn.makefile('rb')

    getImages(connect=connect, printing=True)

    connect.close()
    conn.close()
    server_socket.close()
