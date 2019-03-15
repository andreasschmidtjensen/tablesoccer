from PIL import ImageFont, ImageDraw, Image
import numpy as np

from tablesoccer.Ball import Ball
import tablesoccer.Players as Players
from tablesoccer.GoalChecker import GoalChecker


class SoccerField:
    def __init__(self, field_shape, debug=False):
        self.center = None
        self.corners = None
        self.field_shape = field_shape

        self.ball = Ball()
        self.players = None
        self.goal_checker = GoalChecker()

        self.score = []
        self.possession = None

        self.debug = debug

    def update(self, detector):
        self.center = detector.center
        self.corners = detector.corners

        self.ball = detector.ball
        self.players = detector.players

        if self.players is not None:
            calc = self.players.calculate_possession(self.ball.get_position())
            if calc is not None:
                self.possession = calc  # to avoid overwriting an existing value with None if ball is out of sight

            self.goal_checker.check_for_goal(self)

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
        if self.center is None:
            return canvas

        font = ImageFont.truetype("Roboto-Regular.ttf", 12)

        # Convert canvas to Pillow object
        im = Image.fromarray(canvas)
        draw = ImageDraw.Draw(im, 'RGBA')  # RGBA to allow alpha

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
                                poss = np.nan_to_num(self.possession[1][r][p])
                                opacity = int(opacity * poss)
                        reach = (x - Players.REACH_WIDTH / 2,
                                 y - Players.REACH_HEIGHT / 2,
                                 x + Players.REACH_WIDTH / 2,
                                 y + Players.REACH_HEIGHT / 2)
                        draw.rectangle(reach, fill=(255, 255, 255, opacity), outline=(255, 255, 255, 140), width=2)

                        # draw player location
                        bb = (x - 2, y - 2, x + 2, y + 2)
                        draw.ellipse(bb, (255, 255, 120, 255))

            if self.debug:
                self.goal_checker.draw_goal_area(draw)

        score = [0, 0]
        for goal in self.score:
            score[goal["team"]] += 1

            x = goal["player"]["shot_position"][0]
            y = goal["player"]["shot_position"][1]
            draw.line((x - 2, y - 2, x + 2, y + 2), fill=(255, 120, 120, 255), width=1)
            draw.line((x + 2, y - 2, x - 2, y + 2), fill=(255, 120, 120, 255), width=1)

        draw.text((0, self.field_shape[1]-15), "Home %s - %s Away" % tuple(score), font=font)

        return np.array(im)

    def goal_scored(self, result):
        self.score.append(result)
