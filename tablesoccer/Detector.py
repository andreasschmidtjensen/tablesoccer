"""
The Detector holds the core logic of detecting the soccerfield and populating the variables with positions.
It is the core of the environment and will always contain up to date information on:

* center of the field
* ball position
* player position
* player rotation

The center of the field is used to calculate the size of the entire field. If we know the center and the size of its
circle, we can calculate the location of the corners. All coordinates of other information are relative to the top-left
corner of the field.

The resulting calculated field is transferred to the SoccerField class which is the representation of a generic
tablesoccer environment.
"""
import os

import numpy as np
from yolo.test import darknet

from tablesoccer.Ball import Ball
from tablesoccer.Players import Players
from util.corner_finder import calculate_corners

os.chdir(os.environ['YOLO_DIR'])
cwd = os.getcwd()

CONFIG = cwd + "/yolov3-tablesoccer.cfg"
WEIGHTS = cwd + "/model/tablesoccer-v1.weights"
DATA = cwd + "/tablesoccer.data"
THRESH = 0.25


ACTUAL_RADIUS = 2
ACTUAL_WIDTH = 32
ACTUAL_HEIGHT = 22


class Detector:
    def __init__(self):
        self.center = None

        self.board_shape = None
        self.corners = None

        self.ball = Ball()
        self.players = None

        self.raw_image = None
        self.calc_image = None

    @staticmethod
    def create_detection_map(detections):
        detection_map = {}
        for d in detections:
            if d[0] not in detection_map:
                detection_map[d[0]] = []
            detection_map[d[0]].append(d)
        return detection_map

    @staticmethod
    def call_darknet(frame):
        return darknet.performDetect(frame, thresh=THRESH, makeImageOnly=True,
                                     configPath=CONFIG, weightPath=WEIGHTS,
                                     metaPath=DATA)

    def calculate_field(self, frame):
        """
        Calculate the corners of the field using the center and a row of players.
        Requires:
        - raw detection of center and players
        :param frame: Full image from camera
        :return: True if the field was calculated, otherwise False
        """
        detection_result = self.call_darknet(frame)
        raw_image = detection_result["image"]
        detection_map = self.create_detection_map(detection_result["detections"])

        center = None
        players = None

        if 'field_center' in detection_map:
            field_center = detection_map['field_center'][0]  # ignore multiple occurrences

            # detection of center
            field_x = field_center[2][0]
            field_y = field_center[2][1]
            field_w = field_center[2][2]
            field_h = field_center[2][3]

            center = np.array([field_x, field_y])

            # calculate board size based on field center size
            board_width = field_w / ACTUAL_RADIUS * ACTUAL_WIDTH
            board_height = field_h / ACTUAL_RADIUS * ACTUAL_HEIGHT
            self.board_shape = (board_width, board_height)

            raw_top_left = (field_x - board_width / 2, field_y - board_height / 2)
            raw_top_right = (field_x + board_width / 2, field_y - board_height / 2)

            if players is None:
                # initialize players with the raw calculation of board location
                players = Players(raw_top_left[0], raw_top_right[0])

            players.update(detection_map.get('player'))

        if players is None or players.get_row(2) is None or len(players.get_row(2).get_players()) < 2:
            # detection was not successful
            return False

        row = players.get_row(2).get_players()

        # reset image
        self.calc_image = np.zeros((raw_image.shape[0], raw_image.shape[1], 3), np.uint8)
        self.corners = calculate_corners(
            center=center,
            player_row=row,
            board_shape=(self.board_shape[0], self.board_shape[1]),
            image_shape=(frame.shape[1], frame.shape[0]),
            canvas=self.calc_image,
            debug=True)

        return True

    def detect(self, frame):
        detection_result = self.call_darknet(frame)

        self.raw_image = detection_result.get("image")
        detection_map = self.create_detection_map(detection_result["detections"])

        if 'field_center' in detection_map:
            self.center = np.array([
                detection_map['field_center'][0][2][0],
                detection_map['field_center'][0][2][1]
            ])

        self.ball.update(detection_map.get('ball'))

        if self.players is None:
            self.players = Players(0, self.raw_image.shape[1])

        self.players.update(detection_map.get('player'))
