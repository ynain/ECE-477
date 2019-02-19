#!/usr/bin/env python3

import os
import cv2
import socket
import datetime


from src.alt_trials import mapfaceEncodings as fmap
from src.piCode.streamwrite import computer_server as cstr
import src.rotateImages as rotate

def getKnownFaces(encode_path="./src/alt_trials/known_faces/"):
    return fmap.readFaceEncodings(encode_path=encode_path)

def getConnection():
    # Make a socket connection that can be written to
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    print("Computer server running...")

    # Accept a single connection and make a file-like object out of it
    conn, addr = server_socket.accept()

    print("Device at {} connected!".format(addr))

    return (conn, addr)

def getWriteSocs(conn):
    send = conn.makefile('wb')
    recv = conn.makefile('rb')

    print("Process ready")

    return (send, recv)

def getImages(connect=None, path='./frames/', ipaddress='0.0.0.0', port='8000', printing=False, log=False):
    return cstr.getImages(connect=connect, path=path, ipaddress=ipaddress, port=port, printing=printing, log=log)

def rotList(images):
    return rotate.rotList(images)

def writeImages(images, path):
    if not os.path.exists(path):
        print("Creating path:\n  {}\n".format(path))
        os.makedirs(path)
        
    now = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

    for i in range(len(images)):
        cv2.imwrite(os.path.join(path, "{}_frame{}.jpg".format(now, i)), images[i])
    
    print("{} images written".format(len(images)))

def getResults(images, known):
    return fmap.compareListToKnown(
                fmap.turnImagesToFeats(images),
                known
            )

def sendResults(res, connect=None, ipaddress='0.0.0.0', port='8000', log=False):
    cstr.sendResult(res, connect=connect, ipaddress=ipaddress, port=port, log=log)

def closeConnection(connect):
    connect.close()
    print("Main connection closed")

def closeWriteSocs(send, recv):
    send.close()
    recv.close()
