#!/usr/bin/env python3

from src.comp_run import *

def runComputer(writeImagePath=None, rot=False):
    known = getKnownFaces()
    while True:
        conn, recv, send, _ = getConnections()

        while True:
            try:
                images = getImages(connect=recv)

                # For our orientation during testing, images need to be corrected
                # The face_recognition library can't see faces that aren't upright
                if rot:
                    images = rotate.rotList(images)

                if not writeImagePath is None:
                    writeImages(images, writeImagePath)
                
                res = getResults(images, known)

                sendResult(res, connect=send)
            except Exception as e:
                print(e)
                break
        
        closeConnections(connect, recv, send)
