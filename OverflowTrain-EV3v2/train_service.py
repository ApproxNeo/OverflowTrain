from direction import Direction
from stations import Station


class TrainService:
    def __init__(self, provider, stations, train, driver, navigator):
        self.provider = provider
        self.stations = stations
        self.train = train
        self.driver = driver
        self.navigator = navigator
        self._create_stations()

    def start(self):
        print("Started!")
        self.train.speak('beep')

        self.train.location = self.stations.get_by_name("City Hall")
        self.train.direction = Direction.NORTH

        while True:
            dest_data = self.provider.get_next_destination()
            dest_station = self.stations.get_by_name(dest_data["destination"])
            if dest_station == None:
                print("Invalid destination: " + dest_data)
                continue

            self.train.speak(dest_station.name)
            route = self.navigator.route(self.train.location, dest_station)
            print(route)
            self.driver.drive(route)
            self.train.speak("destination reached")

    def _create_stations(self):
        self.stations.add_station(Station("Jurong East").connect({"Woodlands": Direction.NORTH,
                                                                  "Clementi": Direction.SOUTH}))

        self.stations.add_station(Station("Woodlands").connect({"Jurong East": Direction.SOUTH
                                                                }))  # "Bishan": Direction.EAST

        self.stations.add_station(Station("Bishan").connect({"Orchard": Direction.SOUTH,
                                                             "Botanic Gardens": Direction.WEST,
                                                             "Serangoon": Direction.EAST}))  # 'Woodlands': Direction.NORTH

        self.stations.add_station(Station("Botanic Gardens").connect({"Bishan": Direction.EAST,
                                                                      "Buona Vista": Direction.SOUTH}))

        self.stations.add_station(Station("Buona Vista").connect({"Botanic Gardens": Direction.NORTH,
                                                                  "Haw Par Villa": Direction. SOUTH,
                                                                  "Clementi": Direction.WEST,
                                                                  "City Hall": Direction.EAST}))

        self.stations.add_station(Station("Clementi").connect({"Jurong East": Direction.NORTH,
                                                               "Buona Vista": Direction.EAST}))

        self.stations.add_station(Station("Haw Par Villa").connect({"HarbourFront": Direction.WEST,
                                                                    "Buona Vista": Direction.NORTH}))

        self.stations.add_station(Station("HarbourFront").connect({"Haw Par Villa": Direction.EAST
                                                                   }))

        self.stations.add_station(Station("City Hall").connect({"Orchard": Direction.NORTH,
                                                                "Marina Bay": Direction.SOUTH,
                                                                "Buona Vista": Direction.WEST,
                                                                "Paya Lebar": Direction.EAST}))

        self.stations.add_station(Station("Orchard").connect({"Bishan": Direction.NORTH,
                                                              "City Hall": Direction.SOUTH}))

        self.stations.add_station(Station("Serangoon").connect({"Bishan": Direction.WEST,
                                                                "Paya Lebar": Direction.SOUTH}))

        self.stations.add_station(Station("Paya Lebar").connect({"Serangoon": Direction.NORTH,
                                                                 "Esplanade": Direction.SOUTH,
                                                                 "City Hall": Direction.WEST,
                                                                 "Changi": Direction.EAST}))

        self.stations.add_station(Station("Changi").connect({"Paya Lebar": Direction.WEST
                                                             }))

        self.stations.add_station(Station("Esplanade").connect({"Paya Lebar": Direction.NORTH,
                                                                "Marina Bay": Direction.WEST}))

        self.stations.add_station(Station("Marina Bay").connect({"City Hall": Direction.NORTH,
                                                                 "Esplanade": Direction.EAST}))
