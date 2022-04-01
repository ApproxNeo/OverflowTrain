import time

from stations import Station
from direction import Direction
from virtual.api.element import Image


STATION_POS = {
    "Jurong East": (99, 424),
    "Woodlands": (101, 184),
    "Bishan": (575, 277),
    "Botanic Gardens": (269, 275),
    "Buona Vista": (270, 639),
    "Clementi": (98, 639),
    "Haw Par Villa": (268, 875),
    "HarbourFront": (99, 876),
    "Jurong East": (98, 425),
    "City Hall": (575, 640),
    "Orchard": (574, 437),
    "Serangoon": (779, 278),
    "Paya Lebar": (779, 639),
    "Changi": (921, 639),
    "Esplanade": (780, 878),
    "Marina Bay": (577, 877),
}


class VirtualTrainRobot:
    def __init__(self, train_element: Image):
        self.train_element = train_element

        self.location: Station = None
        self.direction: Direction = Direction.NONE

    def motor_break(self):
        print("motor_break")

    def action_forward(self):
        print("action_forward")
        self._animate_move(
            *STATION_POS[self.location.get_adj_station(self.direction)])

    def action_turn_left(self):
        print("action_turn_left")
        self._animate_rotate(90)

    def action_turn_right(self):
        print("action_turn_right")
        self._animate_rotate(-90)

    def action_turn_back(self):
        print("action_turn_back")
        self._animate_rotate(180)

    def speak(self, text: str):
        print("speak: '" + text + "'")

    def _animate_rotate(self, angle_change):
        step = -1 if angle_change < 0 else 1
        for _ in range(abs(angle_change)):
            self.train_element.angle += step
            time.sleep(0.008)

    def _animate_move(self, new_x, new_y):
        old_x = self.train_element.rect.centerx
        old_y = self.train_element.rect.centery

        diff_x = new_x - old_x
        step = -1 if diff_x < 0 else 1
        for _ in range(abs(diff_x)):
            self.train_element.rect.move_ip(step, 0)
            time.sleep(0.008)

        diff_y = new_y - old_y
        step = -1 if diff_y < 0 else 1
        for _ in range(abs(diff_y)):
            self.train_element.rect.move_ip(0, step)
            time.sleep(0.008)
