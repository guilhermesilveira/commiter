from picamera.array import PiRGBArray
from picamera import PiCamera
import time


class CameraFeeder:
    __camera = PiCamera()
    __rawCapture = PiRGBArray(__camera)

    def next(self):
        time.sleep(1)
        self.__camera.capture(self.__rawCapture, format="bgr")
        image = self.__rawCapture.array
        return image
