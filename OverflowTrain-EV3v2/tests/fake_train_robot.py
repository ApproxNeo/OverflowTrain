from stations import Station
from direction import Direction


class FakeTrainRobot:
    def __init__(self):
        self.location: Station = None
        self.direction: Direction = Direction.NONE

    def motor_break(self):
        print("motor_break")

    def action_forward(self):
        print("action_forward")

    def action_turn_left(self):
        print("action_turn_left")

    def action_turn_right(self):
        print("action_turn_right")

    def action_turn_back(self):
        print("action_turn_back")

    def speak(self, text: str):
        print("speak: '" + text + "'")
