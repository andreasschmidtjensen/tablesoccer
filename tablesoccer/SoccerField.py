import cv2

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
            cv2.putText(canvas, "DIR: %s" % self.ball.direction, (0, 80),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (120, 255, 50), 1)

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
