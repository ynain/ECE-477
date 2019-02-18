#!/usr/bin/env python3

def runComputer(writeImagePath=None, rot=False):
    known = getKnownFaces()
    while True:
        connect, recv, send, addr = getConnections_Known()

        print("Device at {} connected!")
        while True:
            try:
                images = comp.getImages(connect=connect)

                # For our orientation during testing, images need to be corrected
                # The face_recognition library can't see faces that aren't upright
                if rot:
                    images = rotate.rotList(images)

                if not writeImagePath is None:
                    writeImages(images)
                
                res = facecomp.compareListToKnown(
                    facecomp.turnImagesToFeats(images),
                    known
                )

                comp.sendResult(res, connect=connect)
            except Exception as e:
                print(e)
                break
        
        closeConnections(connect, recv, send)
