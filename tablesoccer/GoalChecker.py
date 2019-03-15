import datetime

import numpy as np

import tablesoccer.Players as Players

GOAL_AREA = (100, 100)


class GoalChecker:

    def __init__(self):
        self.ball_in_goal_area = False, -1  # (In Goal Area, Team)
        self.frames_without_ball = False

        self.ball_history = []
        self.player_history = []

        self.goal_left = None
        self.goal_right = None

    def check_for_goal(self, field):
        """
        We check for goal by checking if the ball disappears in a specific rectangle in front of the goal.
        The process:
        1) Ball is in the field
        2) Ball is in rectangle in front of goal
        3) Ball disappears from field
        4) Ball is gone from the field for 15 frames
        5) Goal is scored!

        We keep the history of the player position and the ball position to be able to figure out who shot.
        We find the player by traversing back in the history until the direction of the ball changes. This time in
        history is assumed to be the time when the shot was taken.

        :param field:
        :return:
        """

        # Get data from the field
        ball = field.ball
        center = field.center
        field_width, _ = field.field_shape
        in_field = ball.get_position() is not None

        # update the goal location based on the center of the field
        self.goal_left = (0, center[1])
        self.goal_right = (field_width, center[1])

        # update history with current frame
        self.ball_history.append({
            "position": ball.get_position(),
            "dir": ball.direction
        })
        self.player_history.append(field.players.players)

        if in_field:
            # the ball is currently in the field so we don't have a goal
            self.frames_without_ball = 0

            # create a rectangle in front of the goal for detecting the ball
            rect_goal_a = [self.goal_left[0] - GOAL_AREA[0] / 2, self.goal_left[1] - GOAL_AREA[1] / 2,
                           self.goal_left[0] + GOAL_AREA[0] / 2, self.goal_left[1] + GOAL_AREA[1] / 2]

            rect_goal_b = [self.goal_right[0] - GOAL_AREA[0] / 2, self.goal_right[1] - GOAL_AREA[1] / 2,
                           self.goal_right[0] + GOAL_AREA[0] / 2, self.goal_right[1] + GOAL_AREA[1] / 2]

            # we check if the ball is in the goal area rectangle
            if rect_goal_a[0] < ball.get_position()[0] < rect_goal_a[2] and rect_goal_a[1] < ball.get_position()[1] < rect_goal_a[3]:
                self.ball_in_goal_area = True, Players.TEAM_AWAY  # Yes, in the away area
            elif rect_goal_b[0] < ball.get_position()[0] < rect_goal_b[2] and rect_goal_b[1] < ball.get_position()[1] < rect_goal_b[3]:
                self.ball_in_goal_area = True, Players.TEAM_HOME  # Yes, in the home area
            else:
                self.ball_in_goal_area = False, -1  # No, no ball in the area

        # Check if the ball has disappeared but was in the goal area just before
        if in_field is False and self.ball_in_goal_area[0]:
            # Count number of frames without a ball detection
            self.frames_without_ball = self.frames_without_ball + 1

            # when more 15 frames has occurred without a ball (and it was in the goal area just before) => goal
            if self.frames_without_ball >= 15:

                team = self.ball_in_goal_area[1]
                self.frames_without_ball = 0
                self.ball_in_goal_area = False, -1

                # find first frame with a different direction, this is when the shot on goal was made
                dir_at_goal = self.ball_history[-1]["dir"]
                direction = dir_at_goal
                i = -1
                while direction == dir_at_goal:
                    i -= 1

                    if len(self.ball_history) < abs(i):
                        # no more moves in history
                        print("> could not see scoring player")
                        i = 0
                        break

                    direction = self.ball_history[i]["dir"]

                player_info = {}
                if i < 0:
                    # scoring player was found
                    pos = self.ball_history[i]["position"]

                    # find the closest player to the shooting position from the player history
                    min_dist = 1000
                    for r, row in enumerate(self.player_history[i]):
                        for p, player in enumerate(row.get_players()):
                            # calc distance between shooting position and player
                            dist = np.linalg.norm(np.array(pos) - np.array(player[0:2]))
                            if dist < min_dist:
                                min_dist = dist
                                player_info["row"] = r
                                player_info["position"] = p

                    player_info["shot_position"] = pos

                # notify field that a goal was scored
                field.goal_scored({
                    "team": team,
                    "ts": datetime.datetime.now(),
                    "player": player_info
                })

    def draw_goal_area(self, draw):
        """
        For debugging purposes, we can draw the area that is used to calculate if a goal is scored.
        :param draw:
        :return:
        """
        rect_goal_a = [self.goal_left[0] - GOAL_AREA[0] / 2, self.goal_left[1] - GOAL_AREA[1] / 2,
                       self.goal_left[0] + GOAL_AREA[0] / 2, self.goal_left[1] + GOAL_AREA[1] / 2]

        rect_goal_b = [self.goal_right[0] - GOAL_AREA[0] / 2, self.goal_right[1] - GOAL_AREA[1] / 2,
                       self.goal_right[0] + GOAL_AREA[0] / 2, self.goal_right[1] + GOAL_AREA[1] / 2]

        draw.rectangle(tuple(rect_goal_a), outline=(255, 255, 255, 140), width=1)
        draw.rectangle(tuple(rect_goal_b), outline=(255, 255, 255, 140), width=1)
