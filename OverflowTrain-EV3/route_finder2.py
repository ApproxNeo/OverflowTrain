import math
import sys


def route_finder(origin, destination):
    global possible_routes
    global MRT_Lines
    global MRT_Interchange
    global possible_start_line
    global possible_end_line

    MRT_Lines = {}
    MRT_Interchange = ["Paya Lebar", "Buona Vista", "Jurong East", "Bishan",
                       "City Hall", "Marina Bay"]  # "Raffles Place", "Dhoby Ghaut", ;
    possible_routes = []

    MRT_Lines["EW"] = ["Tuas Link", "Tuas West Road", "Tuas Cresent", "Gul Circle", "Joo Koon", "Pioneer", "Boon Lay", "Lakeside", "Chinese Garden", "Jurong East", "Clementi", "Dover", "Buona Vista", "Commonwealth",
                       "Queenstown", "Redhill", "Tiong Bahru", "Outram Park", "Tanjong Pagar", "Raffles Place", "City Hall", "Bugis", "Lavender", "Kallang", "Aljunied", "Paya Lebar", "Eunos", "Kembagan", "Bedok", "Tanah Merah", "Changi"]

    MRT_Lines["NS"] = ["Jurong East", "Bukit Batok", "Bukit Gombak", "Choa Chu Kang", "Yew Tee", "Kranji", "Marsiling", "Woodlands", "Admiralty", "Sembawang", "Yishun", "Khatib",
                       "Yio Chu Kang", "Ang Mo Kio", "Bishan", "Braddell", "Toa Payoh", "Novena", "Newton", "Orchard", "Somerset", "Dhoby Ghaut", "City Hall", "Raffles Place", "Marina Bay", "Marina South Pier"]

    MRT_Lines["CC"] = ["HarbourFront", "Telok Blangah", "Labrador Park", "Pasir Panjang", "Haw Par Villa", "Kent Ridge", "one-north", "Buona Vista", "Holland Village", "Farrer Road", "Botanic Gardens", "Caldecott", "Marymount",
                       "Bishan", "Lorong Chuan", "Serangoon", "Bartley", "Tai Seng", "MacPherson", "Paya Lebar", "Dakota", "Mountbatten", "Stadium", "Nicoll Highway", "Promenade", "Esplanade", "Bras Basah", "Dhoby Ghaut", "Marina Bay"]

    possible_start_line = search_route(origin)
    possible_end_line = search_route(destination)

    one_way(origin, destination)
    two_way(origin, destination)

    '''
	if origin in MRT_Interchange or destination in MRT_Interchange:
		pass
	else:
		three_way(origin, destination)
	'''

    preferred_route = find_shortest_route(possible_routes)

    return preferred_route


def one_way(origin, destination):
    for start_line in possible_start_line:
        if destination in MRT_Lines[start_line]:
            # One step - Direct
            start_pos = MRT_Lines[start_line].index(origin)
            end_pos = MRT_Lines[start_line].index(destination)

            stops = count_stops(start_pos, end_pos)
            route_stations = get_middle_stations(
                MRT_Lines[start_line], start_pos, end_pos)

            possible_routes.append(
                {"start_line": start_line, "stops": stops, "stations": route_stations})


def two_way(origin, destination):
    for start_line in possible_start_line:
        for interchange in MRT_Interchange:
            for end_line in possible_end_line:
                if interchange in MRT_Lines[start_line] and interchange in MRT_Lines[end_line]:
                    # Two Step

                    # Origin to interchange
                    start_pos = MRT_Lines[start_line].index(origin)
                    end_pos = MRT_Lines[start_line].index(interchange)
                    origin_stops = count_stops(start_pos, end_pos)

                    route_stations = get_middle_stations(
                        MRT_Lines[start_line], start_pos, end_pos)

                    # Destination to interchange
                    start_pos = MRT_Lines[end_line].index(interchange)
                    end_pos = MRT_Lines[end_line].index(destination)
                    destination_stops = count_stops(start_pos, end_pos)

                    route_stations += [interchange]
                    route_stations += get_middle_stations(
                        MRT_Lines[end_line], start_pos, end_pos)

                    # Total stops
                    stops = origin_stops + destination_stops

                    possible_routes.append({"start_line": start_line,
                                            "second_line": end_line,
                                            "interchange": interchange,
                                            "stops": stops,
                                            "stations": route_stations})


def three_way(origin, destination):
    global Interchange_line
    global first_interchange
    global second_interchange
    global stop_number

    possible_start_line = search_route(origin)
    possible_end_line = search_route(destination)

    first_interchange = closest_interchange(origin)
    second_interchange = []

    interchange_1 = []
    interchange_2 = []

    for interchange in range(len(MRT_Interchange)):
        for start_line in possible_start_line:
            if MRT_Interchange[interchange] in MRT_Lines[start_line]:
                interchange_1.append(MRT_Interchange[interchange])

    MRT_interchange_line = search_route(first_interchange)
    Interchange_line = []

    for x in MRT_interchange_line:
        Interchange_line.append(x)

    if (len(Interchange_line) == 1):
        pass
    else:
        for station in possible_start_line:
            if station in Interchange_line:
                Interchange_line.remove(station)

    for interchange in MRT_Interchange:
        if interchange in MRT_Lines[Interchange_line[0]]:
            interchange_2.append(interchange)

    interchange_2_stops = []
    interchange_2_pos = []

    for interchange in interchange_2:
        for end_line in possible_end_line:
            if interchange in MRT_Lines[end_line]:
                interchange_2_stops.append(interchange)

    for interchange in interchange_2_stops:
        for end_line in possible_end_line:
            if interchange in MRT_Lines[end_line]:
                p = MRT_Lines[end_line].index(interchange)
                interchange_2_pos.append(p)
    line = []

    for end in possible_end_line:
        for i in MRT_Lines[end]:
            line.append(i)

    second_interchange = line[min(interchange_2_pos)]
    stops = 0

    for start in possible_start_line:
        stops += count_stops(MRT_Lines[start].index(origin),
                             MRT_Lines[start].index(first_interchange))

    for mid in Interchange_line:
        if first_interchange in MRT_Lines[mid] and second_interchange in MRT_Lines[mid]:
            stops += count_stops(MRT_Lines[mid].index(first_interchange),
                                 MRT_Lines[mid].index(second_interchange))

    for end in possible_end_line:
        if second_interchange in MRT_Lines[end] and destination in MRT_Lines[end]:
            stops += count_stops(MRT_Lines[end].index(second_interchange),
                                 MRT_Lines[end].index(destination))

    possible_routes.append({"start_line": start_line,
                            "end_line": end_line,
                            "Interchange_line": Interchange_line[0],
                            "First_interchange": first_interchange,
                            "Second_Interchange": second_interchange,
                            "stops": stops})


def closest_interchange(stop):
    start_line = search_route(stop)

    for start in start_line:
        start_pos = MRT_Lines[start].index(stop)

    new_interchange = []

    for interchange in MRT_Interchange:
        for start in start_line:
            if interchange in MRT_Lines[start]:
                new_interchange.append(interchange)

    stops_interchange = []

    for interchange in new_interchange:
        for start in start_line:
            if interchange in MRT_Lines[start]:
                y = start_pos - MRT_Lines[start].index(interchange)
                stops_interchange.append(y)

    sorted_stops = []

    for stops in range(len(stops_interchange)):
        m = int(
            math.sqrt((stops_interchange[stops]) * (stops_interchange[stops])))
        sorted_stops.append(m)

    for i in range(len(sorted_stops)):
        sorted_stops[i] = start_pos+sorted_stops[i]

    closest_stop = min(sorted_stops) - start_pos
    closest_stop = start_pos - closest_stop

    line = []

    for start in start_line:
        for i in MRT_Lines[start]:
            line.append(i)

    return line[closest_stop]


def search_route(_station):
    global MRT_Lines

    possible_lines = []

    for line in MRT_Lines:
        for station in MRT_Lines[line]:
            if _station == station:
                possible_lines.append(line)

    return possible_lines


def count_stops(start_pos, end_pos):
    return int(math.sqrt((start_pos - end_pos) * (start_pos - end_pos)))


def get_middle_stations(stations, start_pos, end_pos):
    if start_pos < end_pos:
        return stations[start_pos + 1:end_pos + 1]
    else:
        return list(reversed(stations[end_pos:start_pos + 1]))


def find_shortest_route(possible_routes):
    lowest = 100
    key = 0

    for i in range(len(possible_routes)):
        if possible_routes[i]["stops"] < lowest:
            lowest = possible_routes[i]["stops"]
            key = i

    return possible_routes[key]


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.pp0
    '''

    print(*args, **kwargs, file=sys.stderr)
