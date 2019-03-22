import numpy as np
import cv2
import os

def rotList(images):
    res = []

    for image in images:
        res.append(rot90(image))
    
    return res

def rot90(image):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    M = cv2.getRotationMatrix2D(image_center,90,1)
    face = cv2.warpAffine(image, M, image.shape[1::-1])

    return face


def rotImage(path):
    for image in os.listdir(path):
        facepath = os.path.join(path, image)

        if os.path.isfile(facepath):
            face = cv2.imread(facepath, cv2.IMREAD_COLOR)
            cv2.imshow('face', face)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            face = rot90(face)

            cv2.imshow('face', face)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.imwrite(facepath, face)

if __name__ == "__main__":
    rotImage("alt_trials/input_images/twoface/")