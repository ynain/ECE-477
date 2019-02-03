#!/usr/bin/env python3

import os
import socket
import shutil

compsystem = os.uname()
OnPi = compsystem.nodename == 'raspberrypi'

if OnPi:
    from piCode.streamwrite import pi_client as pi
else:
    from facenet_trials import teststart as fn
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
    
    # Make a socket connection that can be written to
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    
    for el in [framepath, alignface]:
        try:
            shutil.rmtree(el)
        except Exception as e:
            print(e)
        finally:
            os.makedirs(el)

    print("Computer server running")

    # Accept a single connection and make a file-like object out of it
    conn, addr = server_socket.accept()
    connect = conn.makefile('rb')

    # Run as a server and allow for face images to be downloaded
    comp.getImages(connect=connect, path=framepath)
    
    # Align faces and then run face recognition on them
    fn.align(infaces=path, aligned=alignface)

    # Check that faces were able to be found
    found = os.listdir(os.path.join(alignface, "frames/"))

    if len(found):
        # If faces found, classify them
        fn.testClass(aligned=alignface)
    else:
        print("Face acquisition failed, try again")
    print(found)

    connect.close()
    conn.close()

    server_socket.close()

def runPi():
    client_socket = socket.socket()

    print("Pi Pie Phi guy running")

    command = ''
    while command != 'quit':
        try:
            pi.runConnect(client_socket=client_socket)
        finally:
            command = input("Type 'quit' to exit this process\n")

    client_socket.close()

if __name__ == "__main__":
    print(runStuff())
