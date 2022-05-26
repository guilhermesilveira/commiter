import cv2


class VideoFeeder:
    def __init__(self, filename):
        self.__cap = cv2.VideoCapture(filename)

        if not self.__cap.isOpened():
            print("Error opening video stream or file")
            exit(1)

    def next(self):
        if not self.__cap.isOpened():
            return None

        ret, frame = self.__cap.read()
        if ret:
            return frame

        self.__cap.release()
        return None
