import os
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor

from stations import Station
from direction import Direction


BLUE_PT = int(os.getenv("BLUE_PT", "30"))
WHITE_PT = int(os.getenv("WHITE_PT", "80"))
STATION_PT = int(os.getenv("STATION_PT", "85"))
THRESHOLD = (WHITE_PT + BLUE_PT) / 2


class TrainRobot:
    def __init__(self):
        self.motor_left = LargeMotor(OUTPUT_B)
        self.motor_right = LargeMotor(OUTPUT_C)
        self.motors = MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)

        self.colour_left = ColorSensor(INPUT_2)
        self.colour_center = ColorSensor(INPUT_3)
        self.colour_right = ColorSensor(INPUT_4)

        self.sound = Sound()

        self.location = None
        self.direction = Direction.NONE

        self.colour_left.mode = ColorSensor.MODE_COL_REFLECT
        self.colour_center.mode = ColorSensor.MODE_COL_REFLECT
        self.colour_right.mode = ColorSensor.MODE_COL_REFLECT

    def line_trace(self, until, at_least = 10):
        count = 0
        while not until() or count < at_least:
            self.line_follower(14, 10)
            count += 1

    def line_follower(self, power1, power2):
        right_value = self.colour_right.value() > THRESHOLD
        left_value = self.colour_left.value() > THRESHOLD

        if left_value and right_value:
            pass

        elif left_value:
            self.motor_left.on(speed=power1)
            self.motor_right.on(speed=power2)
        
        elif right_value:
            self.motor_left.on(speed=power2)
            self.motor_right.on(speed=power1)

        else:
            self.motor_left.on(speed=power1)
            self.motor_right.on(speed=power1)

    def move_tank(self, power_left, power_right, value, _brake=False):
        if power_left != 0:
            self.motor_left.on_for_degrees(power_left,
                                           value,
                                           brake=_brake,
                                           block=(power_right == 0))
        if power_right != 0:
            self.motor_right.on_for_degrees(power_right,
                                           value,
                                           brake=_brake,
                                           block=True)

    def motor_break(self):
        self.motor_left.off()
        self.motor_right.off()

    def action_forward(self):
        print("action_forward")
        self.line_trace(self.at_station)
        self.speak('beep')
        self.move_tank(12, 12, 210)

    def action_turn_left(self):
        print("action_turn_left")
        self.move_tank(-12, 12, 190)

    def action_turn_right(self):
        print("action_turn_right")
        self.move_tank(12, -12, 190)

    def action_turn_back(self):
        print("action_turn_back")
        self.move_tank(-12, 12, 380)

    def at_station(self):
        return self.colour_center.value() > STATION_PT

    def speak(self, text):
        if text.lower() == 'beep':
            self.sound.beep()
            return
        self.sound.speak(text)
