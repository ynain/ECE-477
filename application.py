#!/usr/bin/env python3

import traceback
import struct
import sys
import os

# Project is built using Python 3.5+, please comply
if sys.version_info[0] < 3:
    sys.exit('''Project is built using Python 3.5+\n'''
             '''Please comply or this won't work properly'''
             )

compsystem = os.uname()
OnPi = compsystem.nodename == 'raspberrypi'

if OnPi:
    import src.pi_run as pi
else:
    import src.comp_run as cr
    
import src.helpers as h

def runComputer(writeImagePath=None, rot=False):
    known = cr.getKnownFaces()
    while True:
        conn, _ = cr.getConnection()

        while True:
            send = recv = None
            try:
                send, recv = cr.getWriteSocs(conn)
                h.closeSocket(conn, recv, send)

                images = cr.getImages(connect=recv, log=False)

                # For our orientation during testing, images need to be corrected
                # The face_recognition library can't see faces that aren't upright
                if rot:
                    images = cr.rotList(images)

                if not writeImagePath is None:
                    cr.writeImages(images, writeImagePath)
                
                if len(images):
                    res = cr.getResults(images, known)

                    cr.sendResults(res, connect=send, log=False)
            except Exception:
                traceback.print_exc()
                print("Breaking")
                break
            
            if not send is None or not recv is None:
                cr.closeWriteSocs(send, recv)
        
        cr.closeConnection(conn)
    
def runPi(ipaddress='10.3.141.198', port=8000):
    print("Pi Pie Phi guy running")

    command = ''
    while command != 'quit':
        try:
            conn = pi.getConnection(ipaddress=ipaddress)
            while command != 'quit':
                send = recv = None
                try:
                    send, recv = pi.getWriteSocs(conn)
                    pi.sendFrames(connect=send)

                    pi.readResults(connect=recv)
                except Exception:
                    traceback.print_exc()
                    print("Breaking")
                    break
            
                if not send is None or not recv is None:
                    pi.closeWriteSocs(send, recv)
            
                command = input("Type anything to send images again,\n or 'quit' to quit\n")
            pi.closeConnection(conn)
        except Exception as e:
            traceback.print_exc()

        finally:
            command = input("Main connection failure, type 'quit' not to retry\n")

    print("{} entered".format(command))

if __name__ == "__main__":
    if OnPi:
        #runPi(ipaddress='10.3.141.198')
        runPi(ipaddress='10.186.129.210')
    else:
        runComputer(rot=True)
