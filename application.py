#!/usr/bin/env python3

import os
import sys
import socket
import shutil

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


def runStuff():
    compsystem = os.uname()
    
    if OnPi:
        runPi()
    else:
        runComp()

    return compsystem.nodename

def runComp(path="./facenet_trials/runface/", alignface="./facenet_trials/aligned_images/"):
    framepath = os.path.join(os.getcwd(), os.path.join(path, 'frames/'))
    path = os.path.join(os.getcwd(), path)
    alignface = os.path.join(os.getcwd(), alignface)

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
    images = comp.getImages(connect=connect, path=framepath)
    connect.close()
    
    img_feats = facecomp.turnImagesToFeats(images)

    res = facecomp.compareListToKnown(img_feats, compknown=known)

    connect = conn.makefile('wb')
    # Connect to send results to Pi
    facecomp.sendResult(res, connect=connect)
    connect.close()

    print(res)
    conn.close()

    server_socket.close()

def runPi():
    print("Pi Pie Phi guy running")

    command = ''
    while command != 'quit':
        try:
            client_socket = socket.socket()
            pi.runConnect(client_socket=client_socket)
        except Exception as e:
            print(e)
        finally:
            command = input("Type 'quit' to exit this process\n")
            client_socket.close()

if __name__ == "__main__":
    print(runStuff())
