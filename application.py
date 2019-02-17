#!/usr/bin/env python3

import os
import sys
import datetime
import cv2
import socket
import shutil

import rotateImages as rotate

# Project is built using Python 3.5+, please comply
if sys.version_info[0] < 3:
    sys.exit('''Project is built using Python 3.5+\n'''
             '''Please comply or this won't work properly'''
             )


# Imports specific to Pi or Not Pi
compsystem = os.uname()
OnPi = compsystem.nodename == 'raspberrypi'

if OnPi:
    from piCode.streamwrite import pi_client as pi
else:
    from alt_trials import mapfaceEncodings as facecomp
    from piCode.streamwrite import computer_server as comp


def runStuff(writeImagePath=None, rot=False):
    compsystem = os.uname()
    
    if OnPi:
        runPi()
    else:
        runComp(writeImagePath=writeImagePath, rot=rot)

    return compsystem.nodename

def runComp(writeImagePath=None, rot=False):
    
    known = facecomp.readFaceEncodings(encode_path="./alt_trials/known_faces/")
    
    # Make a socket connection that can be written to
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    print("Computer server running")

    # Accept a single connection and make a file-like object out of it
    conn, addr = server_socket.accept()
    connect = conn.makefile('rb')

    # Run as a server and allow for face images to be downloaded
    images = comp.getImages(connect=connect, ipaddress='0.0.0.0', port='8000')
    
    connect.close()
    
    # For our orientation during testing, images need to be corrected
    # The face_recognition library can't see faces that aren't upright
    if rot:
        images = rotate.rotList(images)

    # If we desire to write images to a file location, this writes those files
    if not writeImagePath is None:
        if not os.path.exists(writeImagePath):
            os.makedirs(writeImagePath)
            
        now = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

        for i in range(len(images)):
            cv2.imwrite(os.path.join(writeImagePath, "frame{}_{}.jpg".format(i, now)), images[i])
    
    # get image features (of the largest face)
    img_feats = facecomp.turnImagesToFeats(images)

    # find if it compares to any of the 
    res = facecomp.compareListToKnown(img_feats, compknown=known)

    # Connect to the pi again
    connect = conn.makefile('wb')
    # Send results to Pi
    comp.sendResult(res, connect=connect, ipaddress='0.0.0.0', port='8000')
    connect.close()

    # print(res)
    conn.close()

    server_socket.close()

def runPi(ipaddress='10.3.141.198', port=8000):
    print("Pi Pie Phi guy running")

    command = ''
    while command != 'quit':
        try:
            client_socket = socket.socket()
            client_socket.connect((ipaddress, port))
            pi.runConnect(connect=client_socket, ipaddress='10.3.141.198', port=8000)

            pi.runRead(connect=client_socket, ipaddress='10.3.141.198', port=8000)
        except Exception as e:
            print(e)
        finally:
            command = input("Type 'quit' to exit this process\n")
            client_socket.close()

if __name__ == "__main__":
    print(runStuff(rot=True))
