import route_finder2 as rf
import sys

NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

PERMITTED_STATIONS = ['Jurong East', 'Clementi', 'Bishan', 'Esplanade', 'Orchard', 'Changi', 'Paya Lebar',
                      'Marina Bay', 'Buona Vista', 'City Hall', 'Botanic Gardens', 'Serangoon', 'Haw Par Villa', 'HarbourFront']


class Station:
    def __init__(self):
        pass

    def connect(self, linked_stations):
        self.linked_station = linked_stations

    def get_direction_to(self, to_station):
        if to_station in self.linked_station:
            return self.linked_station[to_station]

        return False


def get_commands(_facing, _origin, _destination):
    global facing

    STATIONS = create_stations()

    facing = _facing
    current = _origin
    destination = _destination
    commands = ""

    route = rf.route_finder(current, destination)

    route["stations"] = [x for x in route["stations"] if x in PERMITTED_STATIONS]
    route["stations"] = unique_station(route["stations"])

    debug_print(route["stations"])

    for station in route["stations"]:
        new_facing = STATIONS[current].get_direction_to(station)

        if new_facing == False:
            continue

        turns = facing - new_facing

        # Simplify the turns
        if turns == 3:
            turns = -1
        elif turns == -3:
            turns = 1

        # Add turns to commands
        if turns == 2 or turns == -2:
            commands += "turn_back;"
        elif turns > 0:
            for i in range(turns):
                commands += "turn_left;"
        else:
            for i in range(turns * -1):
                commands += "turn_right;"

        # if current == "Bishan" and station == "Yishun":
        #     commands += "hardForwards;"
        # elif current == "Woodlands" and station == "Yishun":
        #     commands += "woodlandsHardForwards;"
        # else:
        #     commands += "forward;"

        commands += "forward;"

        current = station
        facing = new_facing

    return commands


def get_facing():
    global facing

    return facing


def get_permitted_stations():
    return PERMITTED_STATIONS


def unique_station(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def create_stations():
    STATIONS = {}
    STATIONS["Jurong East"] = Station()
    STATIONS["Jurong East"].connect({"Woodlands": NORTH, "Clementi": SOUTH})

    STATIONS["Woodlands"] = Station()
    STATIONS["Woodlands"].connect({"Jurong East": SOUTH, "Bishan": EAST})

    STATIONS["Bishan"] = Station()
    STATIONS["Bishan"].connect({'Woodlands': NORTH, "Orchard": SOUTH, "Botanic Gardens": WEST, "Serangoon": EAST})

    STATIONS["Botanic Gardens"] = Station()
    STATIONS["Botanic Gardens"].connect({"Bishan": EAST, "Buona Vista": SOUTH})

    STATIONS["Buona Vista"] = Station()
    STATIONS["Buona Vista"].connect({"Botanic Gardens": NORTH, "Haw Par Villa": SOUTH, "Clementi": WEST, "City Hall": EAST})

    STATIONS["Clementi"] = Station()
    STATIONS["Clementi"].connect({"Jurong East": NORTH, "Buona Vista": EAST})

    STATIONS["Haw Par Villa"] = Station()
    STATIONS["Haw Par Villa"].connect({"HarbourFront": WEST, "Buona Vista": NORTH})

    STATIONS["HarbourFront"] = Station()
    STATIONS["HarbourFront"].connect({"Haw Par Villa": EAST})

    STATIONS["City Hall"] = Station()
    STATIONS["City Hall"].connect({"Orchard": NORTH, "Marina Bay": SOUTH, "Buona Vista": WEST, "Paya Lebar": EAST})

    STATIONS["Orchard"] = Station()
    STATIONS["Orchard"].connect({"Bishan": NORTH, "City Hall": SOUTH})

    STATIONS["Serangoon"] = Station()
    STATIONS["Serangoon"].connect({"Bishan": WEST, "Paya Lebar": SOUTH})

    STATIONS["Paya Lebar"] = Station()
    STATIONS["Paya Lebar"].connect({"Serangoon": NORTH, "Esplanade": SOUTH, "City Hall": WEST, "Changi": EAST})

    STATIONS["Changi"] = Station()
    STATIONS["Changi"].connect({"Paya Lebar": WEST})

    STATIONS["Esplanade"] = Station()
    STATIONS["Esplanade"].connect({"Paya Lebar": NORTH, "Marina Bay": WEST})

    STATIONS["Marina Bay"] = Station()
    STATIONS["Marina Bay"].connect({"City Hall": NORTH, "Esplanade": EAST})

    return STATIONS


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.pp0
    '''

    print(*args, **kwargs, file=sys.stderr)
