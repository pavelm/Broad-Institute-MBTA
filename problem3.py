from problem1 import get_long_names
from problem2 import *

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


def get_tasks(session, list_of_subway_route_ids):
    tasks = []
    for subway_id in list_of_subway_route_ids:
        tasks.append(asyncio.create_task(
            session.get('https://api-v3.mbta.com/stops?filter[route]=' + str(subway_id),
                        headers={"x-api-key": "40ecaac9490140418fea273b1e447bc4"}, ssl=False)))
    return tasks


async def get_route_stops(list_of_subway_route_ids, list_of_subway_route_long_names):
    # https://groups.google.com/g/massdotdevelopers/c/WiJUyGIpHdI
    # https://docs.python.org/3/library/asyncio-task.html#coroutines

    async with aiohttp.ClientSession() as session:

        tasks = get_tasks(session, list_of_subway_route_ids)
        data = await asyncio.gather(*tasks)

        route_stop_dict = {}

        for index in range(len(data)):
            subway_line_data = await (data[index]).json()

            subway_line_data = subway_line_data['data']

            route_stop_dict[list_of_subway_route_long_names[index]] = []
            for stops in subway_line_data:
                route_stop_dict[list_of_subway_route_long_names[index]].append((stops['attributes']['name']))

        return route_stop_dict


# gets a dictionary of each route name corresponding to the routes' connected
def get_line_dict(connecting_stops, route_stops):
    line_dict = {}

    # create dictionary, each key is the route id and each value is the list of lines connected to it
    for route_id in route_stops.keys():
        line_dict[route_id] = []

        # for each connecting_stop list
        for connecting_stops_lists in connecting_stops.values():

            # if the route_id is in the list, we want to add all the lines except for the id
            if route_id in connecting_stops_lists:

                # for each stop in the connecting_stop_lists
                for stop in connecting_stops_lists:

                    # if the stop does not equal to the route_id and the stop is not in the line_dict for the route id
                    if stop != route_id and stop not in line_dict[route_id]:
                        line_dict[route_id].append(stop)

    return line_dict


# https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/depth-first-search-dfs-algorithm/
# depth first search graph searching algorithm traverses as far as it can go down one branch until it has to backtrack
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

            result = dfs(neighbour, target, line_dict, path, visited)
            if result is not None:
                return result

    path.pop()
    return None


# finds the path of a starting and final destination
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

    if starting_location_subway_line == "" or end_location_subway_line == "":
        logging.ERROR("Starting or Finish location does not exist")
        return ""

    return dfs(starting_location_subway_line, end_location_subway_line, line_dict)


def main():
    start_location = input("Starting point station: ")

    finish_location = input("Final point station: ")

    start = time.time()

    # gets the list of subway route ids
    list_of_subway_route_ids = get_subway_route_ids()

    # get the list of subway route long names
    list_of_subway_route_long_names = get_long_names(filter_subway_routes())

    # get the routes and their corresponding stops
    route_stops = asyncio.run(get_route_stops(list_of_subway_route_ids, list_of_subway_route_long_names))

    # get all the stops on mbta
    all_stops = get_all_stops(route_stops)

    # get stops with > 1 connections
    connecting_stops = get_connecting_stops(all_stops)

    # stops on route line that are connecting to other route lines
    routes_connecting_stop_dict = get_routes_of_connecting_stops(connecting_stops, route_stops)

    # line dictionary
    line_dict = get_line_dict(routes_connecting_stop_dict, route_stops)

    logging.info(find_subway_path(start_location, finish_location, route_stops, line_dict))

    end = time.time()

    logging.info("Run time: " + str(end - start))


if __name__ == '__main__':
    main()
