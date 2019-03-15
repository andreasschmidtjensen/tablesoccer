import numpy as np

ROTATION_MIN = 0.5
ROTATION_MAX = 2.0

REACH_WIDTH = 100
REACH_HEIGHT = 75

TEAM_HOME = 0
TEAM_AWAY = 1


class Players:
    def __init__(self, field_x_start, field_x_end,
                 row_config=((3, TEAM_HOME), (3, TEAM_AWAY), (3, TEAM_HOME), (3, TEAM_AWAY))):
        self.rows = len(row_config)
        self.field_x_start = field_x_start
        self.field_x_end = field_x_end

        self.row_size = (self.field_x_end - self.field_x_start) / self.rows

        self.players = [Row(i, config[0], config[1]) for i, config in enumerate(row_config)]

    def update(self, detections):
        for r in self.players:
            r.reset()

        if detections is None:
            return

        for d in detections:
            # calculate row
            x = d[2][0]
            row = int((x - self.field_x_start) / self.row_size)

            # put in players array
            if self.rows > row:
                self.players[row].add_player(d[2])
            else:
                print("DETECTING PLAYER OUTSIDE ROW: %s" % row)

    def get_row(self, row):
        if self.rows > row:
            return self.players[row]
        else:
            return None

    def calculate_possession(self, ball_position):
        if ball_position is None:
            return None

        team_possession = [0, 0]
        player_possession = []
        for row in self.players:
            row.calculate_possession(ball_position)

            team = row.team
            possession = row.possession
            team_possession[team] += np.sum(possession)
            player_possession.append(possession)

        return team_possession / np.sum(team_possession), \
               player_possession / np.sum(player_possession)


class Row:
    """
    This class represents a row. Since players can't switch place in a row,
    we create an array that holds the players. Each player is defined by its position,
    so the top player is the first in the array and so on.

    When re-detecting the field, we recreate the row, but since the position of the
    players can't change, we will get the same configuration again with updated positions.
    """
    def __init__(self, row_number, num_players, team):
        self.row_number = row_number
        self.num_players = num_players
        self.team = team

        self.players = []
        self.rotation = 0.0

        self.x_coordinate = None

        self.possession = [0 for _ in range(num_players)]

    def reset(self):
        self.players = []
        self.rotation = 0.0

    def add_player(self, player):
        """
        Adds player to the row. This function ensures that the players array is always
        sorted by y-position of the players starting from top.
        :param player: (X,Y) position
        """
        if len(self.players) >= self.num_players:
            print("Too many players in row %s!" % self.row_number)

        # add player to array
        self.players.append(player)
        # sort according to y-axis
        self.players.sort(key=lambda x: x[1])

        if len(self.players) == self.num_players:
            self.calculate_rotation()
            self.x_coordinate = np.mean([p[0] for p in self.players])

    def calculate_possession(self, ball_position):
        for i, player in enumerate(self.players):
            if len(self.possession) < i:
                continue  # has detected too many players

            reach_x_start = player[0] - REACH_WIDTH / 2
            reach_x_end = player[0] + REACH_WIDTH / 2
            reach_y_start = player[1] - REACH_HEIGHT / 2
            reach_y_end = player[1] + REACH_HEIGHT / 2

            ball_x = ball_position[0]
            ball_y = ball_position[1]

            if reach_x_start < ball_x < reach_x_end and reach_y_start < ball_y < reach_y_end:
                self.possession[i] += 1
                break

    def get_players(self):
        return self.players

    def calculate_rotation(self):
        """
        Since we view from above, we know a player is rotated if the width of the bounding box
        is greater than the height. The rotation will go from 0% rotated (standing) to 100% rotated (lying)

        We calculate it as an average of the bounding box size of all players in the row.
        """
        avg_width = np.mean([p[2] for p in self.players])
        avg_height = np.mean([p[3] for p in self.players])

        ratio = avg_width / avg_height

        self.rotation = min(1,
                            max(0,
                                (ratio - ROTATION_MIN) / (ROTATION_MAX - ROTATION_MIN)
                                )
                            )
