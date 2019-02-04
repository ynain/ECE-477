#!/usr/bin/env python3

import face_recognition as fr
import numpy as np
import json
import cv2
import os

# Use the area of the bounding box as the "largest face" finder
def largestFaceIndex(face):
    face_locations = fr.face_locations(frame)
    area = []

    for top, right, bottom, left in face_locations:
        area.append( (bottom - top) * (right - left) )
    
    return area.index(max(area))

# Assumes subfolders with names of subjects
def getFaceEncodings(folderName="input_images"):
    res = {}

    for person in os.listdir(folderName):
        curpath = os.path.join(folderName, person)
        if os.path.isdir(curpath):
            res[person] = []    # Encodings for each person will be saved in a list

            # Ignore the self generated .npz filess
            names = []
            for image in os.listdir(curpath):
                if not image.endswith(".npz"):
                    names.append(fr.load_image_file(os.path.join(curpath, image)))

            res[person].extend(turnImagesToFeats(names))

        else:
            print("{} isn't a directory...".format(person))
    
    return res

def writeFaceEncodings(encoded, outName="known_faces"):
    for person in encoded:
        encodefile = os.path.join(outName, person, "encodings_"+person+"")
        
        np.savez_compressed(encodefile, encoded[person])

# Assumes a directory with each sub directory being the name of the candidate
def readFaceEncodings(encode_path="known_faces"):
    res = {}

    for person in os.listdir(encode_path):
        encodefile = os.path.join(encode_path, person, "encodings_"+person+".npz")
        res[person] = []

        npzclass = np.load(encodefile)

        for fn in npzclass.files:
            res[person].extend(npzclass[fn])
    
    return res

# Compares a list of features against a list of known vectors
def compareListToKnown(inlist, compknown=None, encode_path="known_faces"):
    if compknown is None:
        compknown = readFaceEncodings(encode_path=encode_path)
    
    res = {}

    for person in compknown:
        temp = []
        for el in inlist:
            temp.extend(fr.compare_faces(compknown[person], el))

        res[person] = temp.count(True) / len(temp)

    return res

# Turns images into the 128 feature list/vector
def turnImagesToFeats(images):
    res = []

    for image in images:
        # Find face encodings
        face_encodings = fr.face_encodings(image)
        index = 0

        # Find the one with the most area (i.e. "biggest")
        if len(face_encodings) > 1:
            index = largestFaceIndex(image)
                
        # Append the biggest/only face encoding, if available
        if len(face_encodings) > 0:
            res.append(face_encodings[index])
        
    return res

if __name__ == "__main__":
    # res = getFaceEncodings()
    # writeFaceEncodings(res)
    known = readFaceEncodings()
    print(known["Ian"])
    print(compareListToKnown(known["Ian"], known))