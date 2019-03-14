import datetime

import numpy as np

from tablesoccer.Position import Position


class Ball:
    def __init__(self):
        self.position = Position(10)
        self.history = []
        self.direction = ""

    def update(self, detection):
        if detection is None:
            # no detection of center
            self.position.remove_last()
            return

        if len(detection) > 0:
            # save position from detection
            self.position.update_position(detection[0][2][0], detection[0][2][1])
            # update history
            self.history.append({"ts": datetime.datetime.now(), "position": self.get_position()})
            self.history = self.history[-100:]  # keep last 100 positions
            # check if direction has changed
            self.update_direction()

    def get_position(self):
        return self.position.get_position()

    def update_direction(self):
        if len(self.history) > 10:
            # check direction between current and 10 frames ago
            prev = self.history[-10]["position"]
            this = self.history[-1]["position"]

            dX = prev[0] - this[0]
            dY = prev[1] - this[1]

            (dirX, dirY) = ("", "")

            # ensure there is significant movement in the x-direction
            if np.abs(dX) > 10:
                dirX = "Left" if np.sign(dX) == 1 else "Right"

            # ensure there is significant movement in the y-direction
            if np.abs(dY) > 10:
                dirY = "Up" if np.sign(dY) == 1 else "Down"

            # handle when both directions are non-empty
            if dirX != "" and dirY != "":
                self.direction = "{}-{}".format(dirY, dirX)

            # otherwise, only one direction is non-empty
            else:
                self.direction = dirX if dirX != "" else dirY

            if self.direction == "":
                if "dir" in self.history[-2]:
                    # update direction to last known direction if nothing found
                    self.direction = self.history[-2]["dir"]

            self.history[-1]["dir"] = self.direction
