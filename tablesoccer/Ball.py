from tablesoccer.Position import Position


class Ball:
    def __init__(self):
        self.position = Position(10)

    def update(self, detection):
        if detection is None:
            # no detection of center
            self.position.remove_last()
            return

        if len(detection) > 0:
            self.position.update_position(detection[0][2][0], detection[0][2][1])

    def get_position(self):
        return self.position.get_position()
