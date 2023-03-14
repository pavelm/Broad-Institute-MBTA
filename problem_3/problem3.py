import requests
import time


# Problem 3
# List a rail route you could travel to get from one stop to the other.
# if I wanted to pursue efficiency and the shortest path, I would use Dijkstra's algorithm using longitude / latitude

# using depth first search because it's used for connected components in undirected graphs
# there's a lot of thought and consideration that goes into which graph searching algorithm and I think a

# Why? Considering the searched node or end_location is reachable after some edges from the original source
# considering the edges are lists that we have to see if the end_location is in, we aren't doing as much searching
#


def filter_subway_routes():
    # Rely on the server API to filter before results are received
    start = time.time()
    r = requests.get('https://api-v3.mbta.com/routes?filter[type]=0,1',
                     headers={"x-api-key": "40ecaac9490140418fea273b1e447bc4"})

    end = time.time()

    # gets the data from the api filter
    data = r.json()['data']

    # create empty list
    subway_routes = []

    # looping through the filtered data and appending the routes' long_names to the list
    for route in data:
        subway_routes.append(route)

    return subway_routes


def get_route_stops():
    # https://groups.google.com/g/massdotdevelopers/c/WiJUyGIpHdI

    # list of all the subway route id's
    list_of_subway_route_ids = []

    for subway_route in filter_subway_routes():
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


# get all the subway stops
def get_all_stops():
    # get all the stops
    all_stops = []

    start = time.time()
    # gets all stops from dictionary
    for stops in get_route_stops().values():
        all_stops.extend(stops)

    end = time.time()

    return all_stops


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


def get_line_dict(connecting_stops, route_stops):

    line_dict = {}

    # create dictionary, each key is the route id and each value is the list of lines connected to it
    for route_id in route_stops.keys():
        line_dict[route_id] = []

        # for each connecting_stop list
        for connecting_stops_lists in connecting_stops.values():

            # if the route_id is in the list, we want to add all of the lines except for the id
            if route_id in connecting_stops_lists:

                for stop in connecting_stops_lists:

                    if stop != route_id and stop not in line_dict[route_id]:
                        line_dict[route_id].append(stop)

    return line_dict



graph = get_line_dict(get_routes_of_connecting_stops(), get_route_stops())


# https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/depth-first-search-dfs-algorithm/
def dfs(start, target, path=[], visited=set()):
    path.append(start)
    visited.add(start)

    if start == target:
        return path

    for neighbour in graph[start]:
        if neighbour not in visited:

            if target in graph[start]:
                path.append(target)
                return path

            result = dfs(neighbour, target, path, visited)
            if result is not None:
                return result
    path.pop()
    return None


def find_subway_path(start, finish):
    route_stop_dict = get_route_stops()

    starting_location_subway_line = ""
    end_location_subway_line = ""

    # instead of thinking about stop - stop, thinking about line - line is easier
    for subway_route, subway_stops in route_stop_dict.items():
        if start in subway_stops:
            starting_location_subway_line = subway_route
            break

    for subway_route, subway_stops in route_stop_dict.items():
        if finish in subway_stops:
            end_location_subway_line = subway_route
            break

    return dfs(starting_location_subway_line, end_location_subway_line)



def main():
    print(find_subway_path("Ashmont", "Arlington"))


main()
