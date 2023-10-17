import logging
import time
import asyncio
import aiohttp

from problem1 import mbta_subway_routes

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


# gets the subway route ids of the filtered subway routes
def get_subway_route_ids(subway_routes):
    return map(lambda subway_route: subway_route['id'], subway_routes)


# Coroutines are computer program components that allow execution
# to be suspended and resumed, generalizing subroutines for cooperative multitasking
# https://en.wikipedia.org/wiki/Coroutine

# we can get a set of all scheduled and running tasks
def get_tasks(session, list_of_subway_route_ids):
    tasks = []
    for subway_id in list_of_subway_route_ids:
        tasks.append(asyncio.create_task(
            # I would create a class that abstracts away all of the querying from mbta.com
            session.get('https://api-v3.mbta.com/stops?filter[route]=' + str(subway_id),
                        headers={"x-api-key": "40ecaac9490140418fea273b1e447bc4"}, ssl=False)))
    return tasks


# gets a dictionary of routes and their corresponding stops
# https://www.youtube.com/watch?v=nFn4_nA_yk8
# https://groups.google.com/g/massdotdevelopers/c/WiJUyGIpHdI
async def get_route_stops(list_of_subway_route_ids):
    async with aiohttp.ClientSession() as session:

        tasks = get_tasks(session, list_of_subway_route_ids)
        data = await asyncio.gather(*tasks)

        # create an empty dictionary
        route_stop_dict = {}

        for index in range(len(data)):
            # get teh subway line data
            subway_line_data = await (data[index]).json()

            subway_line_data = subway_line_data['data']

            route_stop_dict[list_of_subway_route_ids[index]] = []

            for stops in subway_line_data:
                route_stop_dict[list_of_subway_route_ids[index]].append((stops['attributes']['name']))

        return route_stop_dict


# sorts the stops in length of stops
def sort_route_stops(route_stops):
    #  https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
    return dict(sorted(route_stops.items(), key=lambda x: len(x[1])))


# print the  name of the subway route with the most stops as well as a count of its stops.
def route_with_most_stops(sorted_route_dict):
    logging.info("Subway route with the most number of stops: " + str(list(sorted_route_dict.keys())[-1]))
    logging.info("Stops: " + str(len(list(sorted_route_dict.values())[-1])) + "\n")


# print the name of the subway route with the fewest stops as well as a count of its stops.
def route_with_least_stops(sorted_route_dict):
    logging.info("Subway route with the least number of stops: " + str(list(sorted_route_dict.keys())[0]))
    logging.info("Stops: " + str(len(list(sorted_route_dict.values())[0])) + "\n")


# get all the subway stops
def get_all_stops(route_stops):
    # get all the stops
    all_stops = []

    # gets all stops from dictionary
    for stops in route_stops.values():
        all_stops.extend(stops)

    return all_stops


# A list of the stops that connect two or more subway routes along with the relevant route names for each of those stops
def get_connecting_stops(all_stops):
    # list of connecting stops
    connecting_stops = set()

    # loop through each stop in all the subway stops
    for stop in all_stops:

        # if there are more than one stop, then it is a connecting stop
        # check if the stop is already in the list (for the purpose of duplication)
        if all_stops.count(stop) > 1:
            connecting_stops.add(stop)

    return list(connecting_stops)


# gets the routes of all the connecting stops that travels through it
def get_routes_of_connecting_stops(connecting_stops, route_stop_dict):
    connecting_stops_dict = {}

    # for each route
    for route in route_stop_dict.keys():

        # for each connecting stop
        for connecting_stop in connecting_stops:

            # if connecting stop is not accounted for, set connecting stop to dictionary with current route as key
            if connecting_stop in route_stop_dict[route] and connecting_stop not in connecting_stops_dict:
                connecting_stops_dict[connecting_stop] = [route]

            # if connecting stop is accounted for, add current route to list of routes @ connecting stop
            elif connecting_stop in route_stop_dict[route] and connecting_stop in connecting_stops_dict:
                connecting_stops_dict[connecting_stop] = connecting_stops_dict[connecting_stop] + [route]

    return connecting_stops_dict


# prints the routes and their connecting stops
def print_all_routes_of_connecting_stops(connecting_stops_dict):
    for connecting_stop, list_of_route_names in connecting_stops_dict.items():
        logging.info("Connecting Stop: " + connecting_stop)
        logging.info("Routes at " + connecting_stop + ": " + str(list_of_route_names) + "\n")


def main():
    start = time.time()

    # gets the list of subway route ids

    # pass in the api key here
    list_of_subway_route_ids = get_subway_route_ids()

    # get the routes and their corresponding stops
    route_stops = asyncio.run(get_route_stops(list_of_subway_route_ids))

    # sort route_stops
    sorted_route_stop_dict = sort_route_stops(route_stops)

    # get all the stops on mbta
    all_stops = get_all_stops(sorted_route_stop_dict)

    # get stops with > 1 connections
    connecting_stops = get_connecting_stops(all_stops)

    # route with the most stops
    route_with_most_stops(sorted_route_stop_dict)

    # route with the least stops
    route_with_least_stops(sorted_route_stop_dict)

    # stops on route line that are connecting to other route lines
    routes_connecting_stop_dict = get_routes_of_connecting_stops(connecting_stops, sorted_route_stop_dict)

    # print routes and their connecting stops
    print_all_routes_of_connecting_stops(routes_connecting_stop_dict)

    end = time.time()

    logging.info("Run time: " + str(end - start))


if __name__ == "__main__":
    main()
