import serial
import time

DISPLAY = 'D'
SOUND = 'S'


class ArduinoConnector:
    def __init__(self, port, config, baud_rate=9600):
        self.serial = serial.Serial(port, baud_rate)
        self.config = config

        self.last_call = time.time()

    def has_feature(self, feature):
        return "features" in self.config and feature in self.config["features"]

    def print_score(self, home, away):
        """
        Write D{current scores} to the serial port to show current scores on LCD
        :param home:
        :param away:
        :return:
        """

        # make sure to only write to the LCD every few seconds,
        # otherwise the LCD will mix up the received text
        now = time.time()
        if now - self.last_call < 2:
            return

        self.last_call = now

        score_text = f"HOME        AWAY\n     {home} -- {away}"
        self.write(DISPLAY, score_text)

    def goal_scored(self, result):
        """
        Write S{TEAM} to the serial port to play a sound when a goal is scored, e.g. SA, when Away team scores.
        :param result:
        :return:
        """
        team = "H" if result["team"] == 0 else "A"
        self.write(SOUND, team)

    def write(self, write_type, content=""):
        self.serial.write(bytes(f"{write_type}{content}", "utf8"))
