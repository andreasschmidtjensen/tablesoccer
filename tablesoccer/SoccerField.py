import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

from tablesoccer.Ball import Ball


class SoccerField:
    def __init__(self):
        self.center = None
        self.corners = None

        self.ball = Ball()
        self.players = None

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
            font = ImageFont.truetype("Roboto-Regular.ttf", 12)

            im = Image.fromarray(canvas)
            draw = ImageDraw.Draw(im)

            draw.text((0, 0), "Direction: %s" % self.ball.direction, font=font)

            center_bb = (self.center[0] - 2, self.center[1] - 2, self.center[0] + 2, self.center[1] + 2)
            draw.ellipse(center_bb, (120, 255, 255, 255))

            ball_pos = self.ball.get_position()
            if ball_pos is not None:
                ball_bb = (ball_pos[0] - 2, ball_pos[1] - 2, ball_pos[0] + 2, ball_pos[1] + 2)
                draw.ellipse(ball_bb, (255, 12, 255, 255))

            players = self.players
            if players is not None:
                for i, row in enumerate(players.players):
                    draw.text((int(row.x_coordinate - 20), 25), "%.2f%%" % (row.rotation * 100), font=font)

                    for player in row.get_players():
                        if len(player) > 0:
                            x, y = player[0], player[1]
                            bb = (x - 2, y - 2, x + 2, y + 2)
                            draw.ellipse(bb, (255, 255, 120, 255))

            canvas = np.array(im)

        return canvas
