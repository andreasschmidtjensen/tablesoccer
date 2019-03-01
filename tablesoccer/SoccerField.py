"""
The SoccerField represents the field of the tablesoccer. It is the core of the environment and will always contain up
to date information on:

* center of the field
* ball position
* player position
* player rotation

The center of the field is used to calculate the size of the entire field. If we know the center and the size of its
circle, we can calculate the location of the corners. All coordinates of other information are relative to the top-left
corner of the field.
"""
import cv2

from tablesoccer.Ball import Ball

ACTUAL_RADIUS = 2
ACTUAL_WIDTH = 20
ACTUAL_HEIGHT = 10


class SoccerField:
    def __init__(self):
        self.center = None

        self.top_left = None
        self.top_right = None
        self.bottom_right = None
        self.bottom_left = None

        self.ball = Ball()

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

            print("Field center: %s" % (field_center,))

            field_x = field_center[2][0]
            field_y = field_center[2][1]
            field_w = field_center[2][2]
            field_h = field_center[2][3]

            w = field_w / ACTUAL_RADIUS * ACTUAL_WIDTH
            h = field_h / ACTUAL_RADIUS * ACTUAL_HEIGHT
            self.top_left = (field_x - w / 2, field_y - h / 2)
            self.top_right = (field_x + w / 2, field_y - h / 2)
            self.bottom_right = (field_x + w / 2, field_y + h / 2)
            self.bottom_left = (field_x - w / 2, field_y + h / 2)

            self.center = (field_x, field_y)

        self.ball.update(detections)

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
        canvas_width = canvas.shape[1]
        canvas_height = canvas.shape[0]

        if self.center is not None:
            center_x = (self.center[0] - self.top_left[0]) / (self.top_right[0] - self.top_left[0]) * canvas_width
            center_y = (self.center[1] - self.top_left[1]) / (self.bottom_left[1] - self.top_left[1]) * canvas_height

            canvas = cv2.circle(canvas, (int(center_x), int(center_y)), 2, (120, 255, 255), 2)

            ball_pos = self.ball.position
            if ball_pos is not None:
                center_x = (ball_pos[0] - self.top_left[0]) / (self.top_right[0] - self.top_left[0]) * canvas_width
                center_y = (ball_pos[1] - self.top_left[1]) / (self.bottom_left[1] - self.top_left[1]) * canvas_height

                canvas = cv2.circle(canvas, (int(center_x), int(center_y)), 2, (255, 120, 255), 2)

        return canvas



