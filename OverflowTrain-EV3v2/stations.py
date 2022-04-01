from direction import Direction


class Station:
    def __init__(self, name):
        self.name = name
        self.linked_stations = {}

    def connect(self, linked_stations):
        self.linked_stations = linked_stations
        return self

    def get_linked_stations(self):
        return self.linked_stations.keys()

    def get_direction_to(self, station):
        station_name = station if isinstance(station, str) else station.name
        return self.linked_stations.get(station_name, Direction.NONE)

    def get_adj_station(self, direction):
        for station_name, link_direction in self.linked_stations.items():
            if direction == link_direction:
                return station_name
        return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Station('" + self.name + "')"


class Stations:
    def __init__(self):
        self.stations = {}

    def add_station(self, station):
        self.stations[station.name] = station

    def get_by_name(self, station_name):
        return self.stations.get(station_name)

    def get_stations(self):
        return self.stations.values()

    def __str__(self):
        return self.get_stations()
