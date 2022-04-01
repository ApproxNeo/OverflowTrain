from direction import Direction


class TrainDriver:
    def __init__(self, stations, train):
        self.stations = stations
        self.train = train

    def drive(self, stations_path):
        for next_station in stations_path:
            if next_station is None:
                continue
            self.go_next_station(next_station)

        self.train.motor_break()

    def go_next_station(self, next_station):
        current_station = self.train.location
        if current_station == next_station:
            return

        new_direction = current_station.get_direction_to(next_station)
        if new_direction is None or new_direction == Direction.NONE:
            return

        self.turn_to_direction(new_direction)
        self.train.action_forward()
        self.train.location = next_station

    def turn_to_direction(self, new_direction):
        current_direction = self.train.direction
        if current_direction == new_direction:
            return

        turn_diff = new_direction - current_direction
        if turn_diff == -3 or turn_diff == 1:
            self.train.action_turn_right()
        if turn_diff == -1 or turn_diff == 3:
            self.train.action_turn_left()
        if turn_diff == -2 or turn_diff == 2:
            self.train.action_turn_back()

        self.train.direction = new_direction
