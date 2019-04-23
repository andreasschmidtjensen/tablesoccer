import datetime

import numpy as np

from util.motion_detection import MotionDetector

GOAL_AREA = (100, 100)


class GoalChecker:
    def __init__(self, paths):
        self.ball_in_goal_area = False, -1  # (In Goal Area, Team)
        self.frames_without_ball = False

        self.goal_checkers = {
            0: MotionDetector(paths["camera_home"]),
            #1: MotionDetector(paths["camera_away"])
        }

        self.ball_history = []
        self.player_history = []

        self.goal_left = None
        self.goal_right = None

        self.goal_scored = True

    def check_for_motion(self, field, team):
        """
        1) Check if there is motion and if goal_scored==False
        2) Check that ball is not in field
        3) If 1 & 2 are True, set flag goal_scored=True and return True
        :param field:
        :param team
        :return: True if motion, False otherwise
        """
        if team not in self.goal_checkers:
            return False

        ball_gone = field.ball.get_position() is None
        motion = self.goal_checkers[team].motion_detected()

        if motion and not self.goal_scored and ball_gone:
            self.goal_scored = True
            return True

        if not ball_gone:
            self.goal_scored = False
            self.goal_checkers[team].update_baseline()

        return False

    def check_for_goal(self, field):
        # Get data from the field
        ball = field.ball
        center = field.center
        field_width, _ = field.field_shape

        # update the goal location based on the center of the field
        self.goal_left = (0, center[1])
        self.goal_right = (field_width, center[1])

        # update history with current frame
        self.ball_history.append({
            "position": ball.get_position(),
            "dir": ball.direction
        })
        self.player_history.append(field.players.players)

        # check for goals
        home_scored = self.check_for_motion(field, 0)
        away_scored = self.check_for_motion(field, 1)

        if home_scored or away_scored:
            self.handle_goal_scored(field, 0 if home_scored else 1)

    def handle_goal_scored(self, field, team):
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

        player_info = None
        if i < 0:
            # scoring player was found
            pos = self.ball_history[i]["position"]

            # find the closest player to the shooting position from the player history
            min_dist = 1000
            for r, row in enumerate(self.player_history[i]):
                for p, player in enumerate(row.get_players()):
                    # calc distance between shooting position and player
                    if pos is None or player[0:2] is None:
                        continue

                    dist = np.linalg.norm(np.array(pos) - np.array(player[0:2]))
                    if dist < min_dist:
                        min_dist = dist
                        player_info = {"row": r, "position": p, "shot_position": pos}

        # notify field that a goal was scored
        result = {
            "team": team,
            "ts": datetime.datetime.now()
        }
        if player_info is not None:
            result["player"] = player_info
        field.goal_scored(result)

    def update_baselines(self):
        for _, goal_checker in self.goal_checkers.items():
            goal_checker.update_baseline()

    def update_snapshots(self, snapshots):
        if 0 in self.goal_checkers:
            snapshots["CAM_HOME_BASELINE"] = self.goal_checkers[0].baseline
            snapshots["CAM_HOME"] = self.goal_checkers[0].latest_frame
            snapshots["CAM_HOME_DIFF"] = self.goal_checkers[0].latest_diff
        if 1 in self.goal_checkers:
            snapshots["CAM_AWAY_BASELINE"] = self.goal_checkers[1].baseline
            snapshots["CAM_AWAY"] = self.goal_checkers[1].latest_frame
            snapshots["CAM_AWAY_DIFF"] = self.goal_checkers[1].latest_diff

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
