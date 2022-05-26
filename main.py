import sys
from pathlib import Path
import logging

import cv2

import numpy as np
from PIL import Image

from cmd import to_parts
from history import History, Saver
from video import VideoFeeder


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
            self.__trigger.trigger(self.__camera_id, cropped, frame_number, delta_info)


def avg_metric(image):
    return np.mean(image)


def parse_video(feeder, parsers):
    frame_number = 0
    while True:
        frame = feeder.next()
        if frame is None:
            break
        frame_number += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        logging.info(f"Frame {frame_number} {type(frame)}")
        for parser in parsers:
            parser.check(gray, frame_number)

    if 'gray' in locals():
        for parser in parsers:
            parser.check(gray, frame_number, force=True)


def parts_to_parsers(parts):
    output = Path("output/")
    history = History(output)
    saver = Saver(history, output)

    parsers = []
    for i, part in enumerate(parts):
        parser = Parser(i, avg_metric, 0.08, window=part, trigger=saver)
        parsers.append(parser)
    return parsers


def run(feeder, parts):
    parsers = parts_to_parsers(parts)
    parse_video(feeder, parsers)


def helper():
    print("Proper usage:")
    print("Screenshot: screenshot")
    print("One camera: parse x1:x2:y1:y2")
    print("Multiple cameras: parse x1:x2:y1:y2 x1:x2:y1:y1")
    exit(0)


def screenshot(feeder):
    frame = feeder.next()
    pil_image = Image.fromarray(frame)
    pil_image.save("output/output.jpg", format="jpeg")


def get_feeder():
    from camera import CameraFeeder
    return CameraFeeder()
    # return VideoFeeder('input/20220526_062621.mp4')


def main():
    if len(sys.argv) < 2:
        helper()

    feeder = get_feeder()
    if sys.argv[1] == "screenshot":
        screenshot(feeder)
    elif sys.argv[1] == "parse":
        arg_parts = to_parts(sys.argv[2:])
        run(feeder, arg_parts)
    else:
        helper()


if __name__ == '__main__':
    main()
