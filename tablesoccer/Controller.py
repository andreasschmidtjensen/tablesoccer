from threading import Thread, Event

import cv2
import imutils
from imutils.video import WebcamVideoStream, FPS
import numpy as np

from tablesoccer.SoccerField import SoccerField
from tablesoccer import Detector
from util.camera import get_image
from util.transform import four_point_transform

YOLO_SIZE = (416, 416)


class Controller(Thread):
    def __init__(self, source_type, path, debug=False):
        super(Controller, self).__init__()

        self.fps = FPS().start()

        self.field = SoccerField()
        self.detector = Detector()

        self.debug = debug

        if source_type == 'webcam':
            self.source = WebcamVideoStream(int(path)).start()
        elif source_type == 'video':
            self.source = cv2.VideoCapture(path)
        else:
            raise NameError("Unknown source_type: %s" % source_type)

        self.snapshots = {}

        self.recalculate = True

        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            frame = get_image(self.source)
            frame = imutils.resize(frame, width=400)

            # 1) DETECT CORNERS
            if self.detector.corners is None or self.recalculate:
                print("** Recalculating field **")
                self.detector.calculate_field(frame)
                self.recalculate = False

            if self.debug:
                img = cv2.resize(frame.copy(), YOLO_SIZE)
                if self.detector.corners is not None:
                    for c in self.detector.corners:
                        img = cv2.circle(img, (int(c[0]), int(c[1])), 2, (255, 255, 120), 2)
                self.snapshots["RAW_DETECTIONS"] = img

            # 2) TRANSFROM IMAGE AND DO DETECTIONS
            if self.detector.corners is not None:
                if self.debug:
                    self.snapshots["CORNER_CALC"] = self.detector.calc_image

                self.field.update(self.detector)

                transformed = cv2.resize(frame, YOLO_SIZE)
                transformed = four_point_transform(transformed, np.array(self.detector.corners))

                self.detector.detect(transformed)
                self.snapshots["TRANSFORMED"] = cv2.cvtColor(self.detector.raw_image, cv2.COLOR_BGR2RGB)

            env = np.zeros((YOLO_SIZE[0], YOLO_SIZE[1], 3), np.uint8)
            env = self.field.draw(env)
            self.snapshots["ENVIRONMENT"] = env

    def schedule_recalculation(self):
        self.recalculate = True
