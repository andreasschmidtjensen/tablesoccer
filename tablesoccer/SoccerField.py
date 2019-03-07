import cv2

from tablesoccer.Ball import Ball
from tablesoccer.Players import Players

ACTUAL_RADIUS = 2
ACTUAL_WIDTH = 33
ACTUAL_HEIGHT = 23


class SoccerField:
    def __init__(self):
        self.center = None
        self.corners = None

        self.ball = Ball()
        self.players = None

    def calc_field(self, detections):
        """
        Calculate the location of the field within the image based on the 'field_center' class

        R = actual radius of center
        W = actual length of field
        H = actual height of field

        (x,y) = detected center coordinates
        r_w = detected width of center
        r_h = detected height of center
        w = calculated length of field
        h = calculated height of field

        radius ratio = r / R
        w = r_w / R * W
        h = r_h / R * H

        (0,0) = (x - w / 2, y - h / 2)

        :param detections: The map of all detections in the current frame.
        :return: None - stores field information in class variables
        """

        field_center = None
        for d in detections:
            if d[0] == 'field_center':
                field_center = d
                break

        if field_center is not None:
            # detection of center
            field_x = field_center[2][0]
            field_y = field_center[2][1]
            field_w = field_center[2][2]
            field_h = field_center[2][3]

            self.ratio_width = field_w / ACTUAL_RADIUS
            self.ratio_height = field_h / ACTUAL_RADIUS

            self.board_width = field_w / ACTUAL_RADIUS * ACTUAL_WIDTH
            self.board_height = field_h / ACTUAL_RADIUS * ACTUAL_HEIGHT

            self.top_left = (field_x - self.board_width / 2, field_y - self.board_height / 2)
            self.top_right = (field_x + self.board_width / 2, field_y - self.board_height / 2)
            self.bottom_right = (field_x + self.board_width / 2, field_y + self.board_height / 2)
            self.bottom_left = (field_x - self.board_width / 2, field_y + self.board_height / 2)

            self.center = (field_x, field_y)

            if self.players is None:
                self.players = Players(self.top_left[0], self.top_right[0], rows=4)

        self.ball.update(detections)
        if self.players is not None:
            self.players.update(detections)

    def update(self, detector):
        self.center = detector.center
        self.corners = detector.corners

        self.ball = detector.ball
        self.players = detector.players

    def draw(self, canvas):
        """
        Draw the current state of the environment on a canvas.
        The corners of the field corresponds to the corners of the canvas.

        (0,0) = top_left
        (1,0) = top_right
        (1,1) = bottom_right
        (0,1) = bottom_left

        :param canvas:
        :return:
        """
        if self.center is not None:
            canvas = cv2.circle(canvas, tuple(self.center.astype(int)), 2, (120, 255, 255), 2)

            ball_pos = self.ball.get_position()
            if ball_pos is not None:
                canvas = cv2.circle(canvas, tuple(ball_pos.astype(int)), 2, (255, 120, 255), 2)

            players = self.players
            if players is not None:
                for i, row in enumerate(players.players):
                    for player in row:
                        if len(player) > 0:
                            x, y = player[0], player[1]
                            canvas = cv2.circle(canvas, (int(x), int(y)), 2, (255, 255, 120), 2)

        return canvas
