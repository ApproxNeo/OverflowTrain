#!/usr/bin/env python3

from ev3dev.ev3 import *
from ev3dev2.motor import MoveSteering, LargeMotor, OUTPUT_B, OUTPUT_C
import time
import sys
import random

import commands_parser2 as cp
import api2_sender as api


GREEN = 3
YELLOW = 4
RED = 5
WHITE = 6
BLUE = 2

MOTOR_LEFT = LargeMotor('outB')
MOTOR_RIGHT = LargeMotor('outC')
MOTORS = MoveSteering('outB', 'outC', motor_class=LargeMotor)

COLOUR_LEFT = ColorSensor("in2")
COLOUR_CENTER = ColorSensor("in3")
COLOUR_RIGHT = ColorSensor("in4")


def main():
    COLOUR_LEFT.mode = "COL-COLOR"
    COLOUR_CENTER.mode = "COL-COLOR"
    COLOUR_RIGHT.mode = "COL-COLOR"

    facing = cp.NORTH
    origin = "City Hall"
    order = api.get_new_order()
    destination = order["destination"]

    while True:
        debug_print("from: " + origin + "; going: " + destination)

        commands = cp.get_commands(facing, origin, destination)

        debug_print(commands)

        travel(commands)

        motor_break(MOTOR_LEFT)
        motor_break(MOTOR_RIGHT)

        # api.delete_order(order["id"])

        facing = cp.get_facing()
        origin = destination
        order = api.get_new_order()
        destination = order["destination"]

        Sound.speak(destination)
        time.sleep(4)


def travel(instructions):
    instructions = instructions.split(";")

    step = 0

    for instruction in instructions:
        print(instruction)
        if instruction == "forward":
            while COLOUR_CENTER.value() != WHITE or COLOUR_LEFT.value() != WHITE or COLOUR_RIGHT.value() != WHITE:
                line_follower(12, 5)

            # If it reaches a station but not destination, move forward a little bit.
            if step != len(instructions) - 1:
                Sound.beep()
                move_tank(12, 12, 160)

        if instruction == "turn_left":
            move_tank(-12, 12, 190)

        if instruction == "turn_right":
            move_tank(12, -12, 190)

        if instruction == "turn_back":
            move_tank(-12, 12, 380)

        # if instruction == "hardForwards":
        #     move_tank(6, 6, 170)

        # if instruction == "woodlandsHardForwards":
        #     COLOUR_LEFT.mode = "COL-REFLECT"

        #     while COLOUR_LEFT.value() <= 72:
        #         line_follower(6, 5)

        #     move_tank(6, 6, 40)

        # If it reached destination already, move forward a little bit.
        '''
		if step == len(instructions) - 1:
			move_tank(6, 6, 10)
			motor_break(LEFT_MOTOR)
			motor_break(RIGHT_MOTOR)
			Sound.beep()
		'''

        step += 1

        motor_break(MOTOR_LEFT)
        motor_break(MOTOR_RIGHT)
        time.sleep(0.5)


def line_follower(power1, power2):
    right_value = COLOUR_RIGHT.value()
    left_value = COLOUR_LEFT.value()
    center_value = COLOUR_CENTER.value()
    print(right_value, left_value, center_value)

    if right_value == BLUE and left_value == BLUE:
        MOTOR_LEFT.on(speed=power1)
        MOTOR_RIGHT.on(speed=power1)

    elif (center_value == BLUE or center_value == WHITE) and right_value == WHITE:
        move_tank(0, power1, 60)

    elif (center_value == BLUE or center_value == WHITE) and left_value == WHITE:
        move_tank(power1, 0, 60)

    elif right_value != BLUE:
        MOTOR_LEFT.on(speed=power1)
        MOTOR_RIGHT.on(speed=power2)

    elif left_value != BLUE:
        MOTOR_LEFT.on(speed=power2)
        MOTOR_RIGHT.on(speed=power1)


def p_follower(power, K_VALUE=0.4):
    error = COLOUR_RIGHT.value() - 50
    steer = error * K_VALUE

    MOTOR_LEFT.on(20, brake=False, block=False)
    MOTOR_RIGHT.on(20, brake=False, block=True)


def move_tank(power_left, power_right, value, _brake=False):
    if power_left != 0:
        MOTOR_LEFT.on_for_degrees(
            power_left, value, brake=_brake, block=(power_right == 0))
    if power_right != 0:
        MOTOR_RIGHT.on_for_degrees(
            power_right, value, brake=_brake, block=True)


def motor_break(motor):
    motor.off()


def get_random_station(origin):
    station = random.choice(cp.get_permitted_stations())

    while station == origin:
        station = random.choice(cp.get_permitted_stations())

    return station


def debug_sensor():
    # Green: 3
    # Yellow: 4
    # Red: 5
    # White: 6

    COLOUR_RIGHT.mode = "COL-REFLECT"

    while True:
        debug_print(COLOUR_RIGHT.value())
        time.sleep(0.5)


if __name__ == '__main__':
    debug_print("Started!")
    Sound.beep()
    main()
