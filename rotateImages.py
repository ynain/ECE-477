import numpy as np
import cv2

for i in range(8):
    facepath = "frame{}.jpg".format(i)
    face = cv2.imread(facepath, cv2.IMREAD_COLOR)
    cv2.imshow('face', face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(face.shape)
    image_center = tuple(np.array(face.shape[1::-1]) / 2)
    M = cv2.getRotationMatrix2D(image_center,90,1)
    face = cv2.warpAffine(face, M, face.shape[1::-1])

    print(type(face))
    cv2.imshow('face', face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(facepath, face)
