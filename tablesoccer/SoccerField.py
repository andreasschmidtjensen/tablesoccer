from PIL import ImageFont, ImageDraw, Image
import numpy as np

from tablesoccer.Ball import Ball
import tablesoccer.Players as Players


class SoccerField:
    def __init__(self):
        self.center = None
        self.corners = None

        self.ball = Ball()
        self.players = None

        self.possession = None

    def update(self, detector):
        self.center = detector.center
        self.corners = detector.corners

        self.ball = detector.ball
        self.players = detector.players

        if self.players is not None:
            calc = self.players.calculate_possession(self.ball.get_position())
            if calc is not None:
                self.possession = calc  # to avoid overwriting an existing value with None if ball is out of sight

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
            draw = ImageDraw.Draw(im, 'RGBA')

            draw.text((0, 0), "Direction: %s" % self.ball.direction, font=font)

            if self.possession is not None:
                draw.text((canvas.shape[1]-100, 0),
                          "Pos.: %.0f%% - %.0f%%" % (self.possession[0][0]*100, self.possession[0][1]*100),
                          font=font)

            center_bb = (self.center[0] - 2, self.center[1] - 2, self.center[0] + 2, self.center[1] + 2)
            draw.ellipse(center_bb, (120, 255, 255, 255))

            ball_pos = self.ball.get_position()
            if ball_pos is not None:
                ball_bb = (ball_pos[0] - 2, ball_pos[1] - 2, ball_pos[0] + 2, ball_pos[1] + 2)
                draw.ellipse(ball_bb, (255, 12, 255, 255))

            players = self.players
            if players is not None:
                for r, row in enumerate(players.players):
                    draw.text((int(row.x_coordinate - 20), 25), "%.2f%%" % (row.rotation * 100), font=font)

                    for p, player in enumerate(row.get_players()):
                        if len(player) > 0:
                            x, y = player[0], player[1]

                            # draw reach
                            opacity = 140
                            if self.possession is not None:
                                player_pos = self.possession[1]
                                if len(player_pos) > r and len(player_pos[r]) > p:
                                    opacity = int(opacity * self.possession[1][r][p])
                            reach = (x - Players.REACH_WIDTH / 2,
                                     y - Players.REACH_HEIGHT / 2,
                                     x + Players.REACH_WIDTH / 2,
                                     y + Players.REACH_HEIGHT / 2)
                            draw.rectangle(reach, fill=(255, 255, 255, opacity), outline=(255, 255, 255, 140), width=2)

                            # draw player location
                            bb = (x - 2, y - 2, x + 2, y + 2)
                            draw.ellipse(bb, (255, 255, 120, 255))

            canvas = np.array(im)

        return canvas
