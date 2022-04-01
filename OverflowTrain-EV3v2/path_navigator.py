class PathNavigator:
    def __init__(self, stations):
        self.stations = stations

    def route(self, start_station, end_station):
        if start_station == end_station:
            return [end_station]

        stations_to_traverse = set(self.stations.get_stations())
        routers = [[start_station]]

        while stations_to_traverse:
            new_routes = []
            for route in routers:
                adj_stations = route[-1].get_linked_stations()
                for station_name in adj_stations:
                    station = self.stations.get_by_name(station_name)
                    if station not in stations_to_traverse:
                        continue
                    stations_to_traverse.remove(station)
                    new_route = [*route, station]
                    if station == end_station:
                        return new_route
                    new_routes.append(new_route)
                routers.extend(new_routes)
