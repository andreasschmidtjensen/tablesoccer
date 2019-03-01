class Ball:
    def __init__(self):
        self.position = None

    def update(self, detections):
        ball = None
        for d in detections:
            if d[0] == 'ball':
                ball = d
                break

        if ball is None:
            # no detection of center
            return

        self.position = (ball[2][0], ball[2][1])
