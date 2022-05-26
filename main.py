import os
import sys
from pathlib import Path
from datetime import datetime

from PIL import Image
import cv2

import numpy as np


class Saver:
    def __init__(self, folder):
        os.makedirs(folder, exist_ok=True)
        self.__current_count = 0
        self.__folder = Path(folder)

    def trigger(self, image, frame_number, delta_info):
        self.__current_count += 1
        timestamp = str(datetime.now())

        path = self.__folder / f"output_{timestamp}_{self.__current_count}_{frame_number}.jpg"
        # print(f"Triggered {path} {delta_info}")
        pil_image = Image.fromarray(image)
        pil_image.save(str(path), format="jpeg")


class Parser:
    def __init__(self, camera_id, metric, threshold, window, trigger: Saver):
        self.__camera_id = camera_id
        self.__avg = 0
        self.__metric = metric
        self.__threshold = threshold
        self.__trigger = trigger
        self.__window = window
        print(f"Camera {camera_id} loaded at {window}")

    def check(self, image: np.array, frame_number, force: bool = False):
        cropped = image[self.__window[2]:self.__window[3], self.__window[0]:self.__window[1]]
        new_value = self.__metric(cropped)
        if self.__avg == 0 or force:
            trigger = True
        else:
            delta = abs(new_value - self.__avg) / self.__avg
            trigger = delta > self.__threshold
        if trigger:
            delta_info = f"current={new_value} previous={self.__avg}"
            self.__avg = new_value
            self.__trigger.trigger(cropped, frame_number, delta_info)


def avg_metric(image):
    return np.mean(image)


def parse_video(parsers):
    cap = cv2.VideoCapture('input/20220526_062621.mp4')

    if not cap.isOpened():
        print("Error opening video stream or file")
        exit(1)

    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_number += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # print(f"Frame {frame_number} {type(frame)}")
            # cv2.imshow('Frame', frame)
            for parser in parsers:
                parser.check(gray, frame_number)
        else:
            break
    if 'gray' in locals():
        for parser in parsers:
            parser.check(gray, frame_number, force=True)

    cap.release()
    # cv2.destroyAllWindows()


def to_int(params):
    return [int(p) for p in params]


def main(args):
    parts = [to_int(arg.split(":")) for arg in args]
    parsers = []

    for i, part in enumerate(parts):
        saver = Saver(f"output/camera_{i}/")
        parser = Parser(i, avg_metric, 0.08, window=part, trigger=saver)
        parsers.append(parser)

    parse_video(parsers)
    # parse_camera()


def help():
    print("Proper usage:")
    print("Screenshot: screenshot")
    print("One camera: parse x1:x2:y1:y2")
    print("One camera: parse x1:x2:y1:y2 x1:x2:y1:y1")
    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
    if sys.argv[1] == "screenshot":
        pass
    elif sys.argv[1] == "parse":
        main(sys.argv[2:])
    else:
        help()

# TODO read pipy camera
