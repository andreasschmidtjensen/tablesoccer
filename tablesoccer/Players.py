class Players:
    def __init__(self, field_x_start, field_x_end, rows=4):
        self.rows = rows
        self.field_x_start = field_x_start
        self.field_x_end = field_x_end

        self.row_size = (self.field_x_end - self.field_x_start) / rows

        self.players = [[] for _ in range(self.rows)]

    def update(self, detections):
        self.players = [[] for _ in range(self.rows)]
        if detections is None:
            return

        for d in detections:
            # calculate row
            x = d[2][0]
            row = int((x - self.field_x_start) / self.row_size)

            # put in players array
            if self.rows > row:
                self.players[row].append(d[2])
            else:
                print("DETECTING PLAYER OUTSIDE ROW: %s" % row)

    def get_row(self, row):
        if self.rows > row:
            return self.players[row]
        else:
            return None
