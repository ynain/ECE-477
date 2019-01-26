import io
import time
import picamera
import picamera.array
import cv2


with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(0.2)
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format="bgr")

        image = stream.array
        cv2.imwrite("stream_mockup.png", cv2.cvtColor(stream.array, cv2.COLOR_BGR2RGB))
