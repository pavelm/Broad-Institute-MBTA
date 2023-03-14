import logging
import requests
import time
import asyncio
import aiohttp

logging.basicConfig(level=logging.INFO)


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


def get_tasks(session, list_of_subway_route_ids):
    tasks = []
    for subway_id in list_of_subway_route_ids:
        tasks.append(asyncio.create_task(
            session.get('https://api-v3.mbta.com/stops?filter[route]=' + str(subway_id),
                        headers={"x-api-key": "40ecaac9490140418fea273b1e447bc4"}, ssl=False)))
    return tasks


async def get_route_stops():
    # https://groups.google.com/g/massdotdevelopers/c/WiJUyGIpHdI

    # list of all the subway route id's
    list_of_subway_route_ids = []

    for subway_route in filter_subway_routes():
        list_of_subway_route_ids.append(subway_route['id'])

    async with aiohttp.ClientSession() as session:

        tasks = get_tasks(session, list_of_subway_route_ids)
        data = await asyncio.gather(*tasks)

        route_stop_dict = {}

        for index in range(len(data)):
            subway_line_data = await (data[index]).json()

            subway_line_data = subway_line_data['data']

            route_stop_dict[list_of_subway_route_ids[index]] = []
            for stops in subway_line_data:
                route_stop_dict[list_of_subway_route_ids[index]].append((stops['attributes']['name']))

        return route_stop_dict


# A list of the stops that connect two or more subway routes along with the relevant route names for each of those stops
def get_connecting_stops(all_stops):
    # list of all subway stops

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
def get_routes_of_connecting_stops(connecting_stops, route_stop_dict):
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


def get_all_stops(route_stops):
    # get all the stops
    all_stops = []

    # gets all stops from dictionary
    for stops in route_stops.values():
        all_stops.extend(stops)

    return all_stops


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


# https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/depth-first-search-dfs-algorithm/
def dfs(start, target, line_dict, path=[], visited=set()):
    path.append(start)
    visited.add(start)

    if start == target:
        return path

    for neighbour in line_dict[start]:
        if neighbour not in visited:

            if target in line_dict[start]:
                path.append(target)
                return path

            result = dfs(neighbour, target, path, visited, line_dict)
            if result is not None:
                return result
    path.pop()
    return None


def find_subway_path(start, finish, route_stops_dict, line_dict):
    starting_location_subway_line = ""
    end_location_subway_line = ""

    # instead of thinking about stop - stop, thinking about line - line is easier
    for subway_route, subway_stops in route_stops_dict.items():
        if start in subway_stops:
            starting_location_subway_line = subway_route
            break

    for subway_route, subway_stops in route_stops_dict.items():
        if finish in subway_stops:
            end_location_subway_line = subway_route
            break


    return dfs(starting_location_subway_line, end_location_subway_line, line_dict)


def main():


    route_stops_dict = asyncio.run(get_route_stops())
    all_stops = get_all_stops(route_stops_dict)
    connecting_stops = get_connecting_stops(all_stops)
    connecting_stops_dict = get_routes_of_connecting_stops(connecting_stops, route_stops_dict)

    line_dict = get_line_dict(connecting_stops_dict,  route_stops_dict)

    # next stage, taking inputs from user and validating 
    logging.info(find_subway_path("Ashmont", "Arlington", route_stops_dict, line_dict))


main()
