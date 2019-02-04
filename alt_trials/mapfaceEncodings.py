#!/usr/bin/env python3

import face_recognition
import numpy as np
import json
import cv2
import os

# Use the area of the bounding box as the "largest face" finder
def largestFaceIndex(face):
    face_locations = face_recognition.face_locations(frame)
    area = []

    for top, right, bottom, left in face_locations:
        area.append( (bottom - top) * (right - left) )
    
    return area.index(max(area))

# Assumes subfolders with names of subjects
def getFaceEncodings(folderName="input_images", outName="known_faces"):
    res = {}

    for person in os.listdir(folderName):
        curpath = os.path.join(folderName, person)
        if os.path.isdir(curpath):
            res[person] = []    # Encodings for each person will be saved in a list

            for image in os.listdir(curpath):
                frame = face_recognition.load_image_file(os.path.join(curpath, image))

                # Find face encodings
                face_encodings = face_recognition.face_encodings(frame)
                index = 0

                # Find the one with the most area (i.e. "biggest")
                if len(face_encodings) > 1:
                    index = largestFaceIndex(frame)
                
                # Append the biggest/only face encoding, if available
                if len(face_encodings) > 0:
                    res[person].append(face_encodings[index])


        else:
            print("{} isn't a directory...".format(person))
    
    return res

def writeFaceEncodings(encoded, outName="known_faces"):
    for person in encoded:
        encodefile = os.path.join(outName, person, "encodings_"+person+"")
        
        np.savez_compressed(encodefile, encoded[person])

def readFaceEncodings(encode_path="known_faces"):
    res = {}

    for person in os.listdir(encode_path):
        encodefile = os.path.join(encode_path, person, "encodings_"+person+".npz")
        res[person] = []

        npzclass = np.load(encodefile)

        for fn in npzclass.files:
            res[person].extend(npzclass[fn])
        
        print(type(res[person]))
        print(res[person][0].shape)



if __name__ == "__main__":
    # res = getFaceEncodings()
    # writeFaceEncodings(res)
    readFaceEncodings()