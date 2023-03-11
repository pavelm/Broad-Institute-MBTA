import requests


# ----------------------------------------------------------------------------------------------------------------------
# problem 1

# purpose: returns a list of routes with the specific filter given in the arguments
def filter_subway_routes():
    # turns the args into a string and cleans to the string, so it can function with the api string
    filtered = str(args).replace(" ", "").replace("(", "").replace(")", "")

    # Rely on the server API to filter before results are received
    r = requests.get('https://api-v3.mbta.com/routes?filter[type]=0,1',
                     headers={"x-api-key": "40ecaac9490140418fea273b1e447bc4"})

    # gets the data from the api filter
    data = r.json()['data']

    # create empty list
    subway_routes = []

    # looping through the filtered data and appending the routes' long_names to the list
    for route in data:
        subway_routes.append(route)

    return subway_routes


# prints the long_name of subway routes
def print_filtered_subway_routes(list_of_subway_routes):
    for subway_route in list_of_subway_routes:
        print(subway_route['attributes']['long_name'])


# ----------------------------------------------------------------------------------------------------------------------

# gets the stops for each route
def get_route_stops():
    # https://groups.google.com/g/massdotdevelopers/c/WiJUyGIpHdI

    # list of all the subway route id's
    list_of_subway_route_ids = []

    for subway_route in filter_subway_routes(0, 1):
        list_of_subway_route_ids.append(subway_route['id'])

    # I chose a dictionary data type, so I can hold both the name of the route and the list of stops
    route_dict = {}

    # create a dictionary of subway route id and list of the stops
    # for each subway_route_id in list_of_subway_route_ids, get the stops for each subway route
    for subway_route_id in list_of_subway_route_ids:
        r = requests.get('https://api-v3.mbta.com/stops?filter[route]=' + subway_route_id,
                         headers={"x-api-key": "40ecaac9490140418fea273b1e447bc4"})

        stops = r.json()['data']

        # list of stops
        route_stops = []

        # get the stops name
        for stop in stops:
            route_stops.append(stop['attributes']['name'])

        route_dict[subway_route_id] = route_stops

    return route_dict


# sorts the stops in length of stops
def sort_route_stops():
    #  https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    return dict(sorted(get_route_stops().items(), key=lambda x: len(x[1])))


# print the  name of the subway route with the most stops as well as a count of its stops.
def route_with_most_stops():
    # create a dictionary of sorted routes
    sorted_route_dict = sort_route_stops()

    print("Subway route with the most number of stops: " + str(list(sorted_route_dict.keys())[-1]))
    print("Stops: " + str(len(list(sorted_route_dict.values())[-1])))


# print the name of the subway route with the fewest stops as well as a count of its stops.
def route_with_least_stops():
    # create a dictionary of sorted routes
    sorted_route_dict = sort_route_stops()

    print("Subway route with the least number of stops: " + str(list(sorted_route_dict.keys())[0]))
    print("Stops: " + str(len(list(sorted_route_dict.values())[0])))


# get all the subway stops
def get_all_stops():
    # get all the stops
    all_stops = []
    # gets all stops from dictionary
    for stops in get_route_stops().values():
        all_stops.extend(stops)

    return all_stops


# A list of the stops that connect two or more subway routes along with the relevant route names for each of those stops
def get_connecting_stops():
    # list of all subway stops
    all_stops = get_all_stops()

    # list of connecting stops
    connecting_stops = []

    # loop through each stop in all the subway stops
    for stop in all_stops:

        # if there are more than one stop, then it is a connecting stop
        # check if the stop is already in the list (for the purpose of duplication)
        if all_stops.count(stop) > 1 and connecting_stops.count(stop) == 0:
            connecting_stops.append(stop)

    return connecting_stops


# gets the routes of all the connecting stops that travels through it
def get_routes_of_connecting_stops():
    route_stop_dict = get_route_stops()
    connecting_stops = get_connecting_stops()

    connecting_stops_dict = {}

    # for each route
    for route in route_stop_dict.keys():

        # for each connecting stop
        for connecting_stop in connecting_stops:

            # if connecting stop is not accounted for, add connecting stop to dictionary with current route as key
            if connecting_stop in route_stop_dict[route] and connecting_stop not in connecting_stops_dict:
                connecting_stops_dict[connecting_stop] = [route]

            # if connecting stop is accounted for, add current route to list of routes @ connecting stop
            elif connecting_stop in route_stop_dict[route] and connecting_stop in connecting_stops_dict:
                connecting_stops_dict[connecting_stop] = connecting_stops_dict[connecting_stop] + [route]

    return connecting_stops_dict


def print_all_routes_of_connecting_stops():
    connecting_stops_dict = get_routes_of_connecting_stops()

    for connecting_stop, list_of_route_names in connecting_stops_dict.items():
        print("Connecting Stop: " + connecting_stop)
        print("Routes at " + connecting_stop + ": " + str(list_of_route_names))
        print()


# ----------------------------------------------------------------------------------------------------------------------


# Problem 3
# List a rail route you could travel to get from one stop to the other.
# if I wanted to pursue efficiency and the shortest path, I would use Dijkstra's algorithm using longitude / latitude

# using depth first search because it's used for connected components in undirected graphs
# there's a lot of thought and consideration that goes into which graph searching algorithm and I think a
# Breadth First Search algorithm is a better option rather than Depth First Search.

# Why? Considering the searched node or end_location is reachable after some edges from the original source
# considering the edges are lists that we have to see if the end_location is in, we aren't doing as much searching
#

def find_connecting_route(starting_location, end_location):
    # check to make sure that the starting_location and end_location exist
    all_stops = get_all_stops()

    if all_stops.count(starting_location) == 0 or all_stops.count(end_location) == 0:
        return "starting location or end location does not exist"

    # connecting routes
    connecting_route_list = []

    # get the dictionary of the routes
    route_stop_dict = get_route_stops()

    # get the dictionary of the connecting routes
    connecting_stop_dict = get_routes_of_connecting_stops()

    # gets the route of the first location
    starting_location_route = ""

    for route, route_stops in route_stop_dict.items():
        if starting_location in route_stops:
            starting_location_route = route
            break

    # base case --> are they both on the same lines?
    if route_stop_dict.get(starting_location_route).count(end_location) > 0:
        return connecting_route_list.append(starting_location_route)
    else:
        connecting_route_list.append(starting_location_route)
    # else --> for all he routes on the starting_location_route, get all the connecting stops on route
    routes_connected = []
    for route, route_stops in connecting_stop_dict.items():

        # if the starting_location_route is in the route_stops for connecting trips
        if route_stops.count(starting_location_route) == 1:

            # append o routes_connected only non starting_location_route routes
            for stop in route_stops:
                if stop != starting_location_route:
                    routes_connected.append(stop)

    for connected_route in routes_connected:
        for route, route_stops in route_stop_dict.items():
            if connected_route == route and route_stops.count(end_location) > 0:
                connecting_route_list.append(route)
                return connecting_route_list

        # https://www.educba.com/depth-first-search/


# algorithm:

# if end_location is on starting_location route, return that

# get all the connecting stops on the starting_location route

# traverse through each

def find_connecting_route_2(starting_location, end_location):
    all_stops = get_all_stops()
    route_stop_dict = get_route_stops()
    connecting_stop_dict = get_routes_of_connecting_stops()

    # check if the starting_location or end_location are valid inputs
    if all_stops.count(starting_location) == 0 or all_stops.count(end_location) == 0:
        return "starting location or end location does not exist"

    # all the visited train tracks
    visited = {}

    for subway_line in route_stop_dict.keys():
        visited[subway_line] = False

    print(visited)

    # initialize a queue
    queue = []

    # connecting routes
    connecting_lines = []

    # get the starting subway line
    starting_location_subway_line = ""

    # get the ending subway line
    end_location_subway_line = ""

    # instead of thinking about stop - stop, thinking about line - line is easier
    for subway_route, subway_stops in route_stop_dict.items():
        if starting_location in subway_stops:
            starting_location_subway_line = subway_route
            break

    for subway_route, subway_stops in route_stop_dict.items():
        if end_location in subway_stops:
            end_location_subway_line = subway_route
            break

    # check if they are on the same line
    if starting_location_subway_line == end_location_subway_line:
        connecting_lines.append(starting_location_subway_line)
        return connecting_lines

    # even if they aren't on the same line, we still have to append the starting_location_subway_line, so we can travel
    # to the connecting stops
    connecting_lines.append(starting_location_subway_line)
    visited[starting_location_subway_line] = True

    routes_connected = set()
    for route, route_stops in connecting_stop_dict.items():
        # if the starting_location_route is in the route_stops for connecting trips
        if starting_location_subway_line in route_stops:
            routes_connected.add(route)

    print(routes_connected)


def main():
    # problem 1
    # print_filtered_subway_routes(filter_subway_routes(0, 1))
    # print()

    # problem 2

    # route_with_most_stops()
    # print()
    # route_with_least_stops()
    # print()
    # print_all_routes_of_connecting_stops()

    # problem 3
    #  Davis to Kendall/MIT -> Red Line
    #  Ashmont to Arlington -> Red Line, Green Line B
    #
    print_all_routes_of_connecting_stops()
    # print(find_connecting_route_2("Ashmont", "Arlington"))


main()
