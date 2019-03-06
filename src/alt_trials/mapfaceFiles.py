

import face_recognition
import numpy as np
import cv2
import os

def largestFaceIndex(face_locations):
    area = []

    for top, right, bottom, left in face_locations:
        area.append( (bottom - top) * (right - left) )
    
    return area.index(max(area))

# Assumes subfolders with names of subjects
def getCropFaces(folderName="input_images", outName="known_faces"):
    res = {}

    for person in os.listdir(folderName):
        curpath = os.path.join(folderName, person)
        if os.path.isdir(curpath):
            res[person] = []
            # print(person)
            for image in os.listdir(curpath):
                try:
                    frame = face_recognition.load_image_file(os.path.join(curpath, image))


                    face_locations = face_recognition.face_locations(frame)
                    if len(face_locations):
                        index = largestFaceIndex(face_locations)
                        
                        # print("{} faces found".format(len(face_locations)))
                        
                        top, right, bottom, left = face_locations[index]
                        vert_pad = (bottom - top) // 7
                        horiz_pad = (right - left) // 7

                        bottom += vert_pad
                        top -= vert_pad
                        left -= horiz_pad
                        right += horiz_pad

                        # Draw a box around the face
                        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                        # Only works with image extensions of 3 letters!
                        name = image[:-4] + "_{}_{}".format(top, left) + image[-4:]

                        res[person].append((name, frame[top:bottom, left:right]))
                        """
                        cv2.imshow(person, res[person][-1][:, :, ::-1]) # color adjust for OpenCV
                        cv2.waitKey(300)
                        cv2.destroyAllWindows()
                        """


                except Exception as e:
                    print(e)

        else:
            print("{} isn't a directory...".format(person))
    # print(len(res["twoface"]))
    return res

def writeCropFaces(cropped, outName="known_faces"):
    for person in cropped:
        print(person)
        personpath = os.path.join(outName, person)
        
        if not os.path.isdir(personpath):
            os.makedirs(personpath)

        for name, img in res[person]:
            cv2.imwrite(os.path.join(personpath, name), img[:, :, ::-1])

if __name__ == "__main__":
    res = getCropFaces()
    writeCropFaces(res)