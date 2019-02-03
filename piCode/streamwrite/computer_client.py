"""
    This file found and edited from documentation for picamera
    https://picamera.readthedocs.io/en/release-1.10/recipes2.html?highlight=socket#rapid-capture-and-streaming
"""

import io
import socket
import struct
import cv2
import numpy as np

def getImages(server_socket=None, ipaddress='0.0.0.0', port='8000'):
    if server_socket is None:
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ipaddress, port))
        server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    conn, addr = server_socket.accept()
    connection = conn.makefile('wb')

    print("connected")

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
        print("{} images received".format(count))
        connection.close()
        server_socket.close()

        for i in range(len(images)):
            cv2.imwrite("frames/frame{}.jpg".format(i), images[i])
        print("Images saved")


if __name__ == "__main__":

    # Make a socket connection that can be written to
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    getImages(server_socket=server_socket)
