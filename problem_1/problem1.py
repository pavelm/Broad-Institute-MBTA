import requests
import logging
import time

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)


# returns a list of routes with the specific filter given in the arguments
def filter_subway_routes():
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


# gets the long names of the subway routes
def get_long_names(list_of_subway_routes):
    list_of_subway_routes_long_names = []

    for subway_route in list_of_subway_routes:
        list_of_subway_routes_long_names.append(subway_route['attributes']['long_name'])

    return list_of_subway_routes_long_names


# prints the long_name of subway routes
def print_filtered_subway_routes(list_of_subway_routes_long_names):
    for subway_route_long_name in list_of_subway_routes_long_names:
        logging.info(subway_route_long_name)


def main():
    start = time.time()

    list_of_filtered_subway_routes = filter_subway_routes()

    list_of_filtered_subway_routes_long_names = get_long_names(list_of_filtered_subway_routes)

    print_filtered_subway_routes(list_of_filtered_subway_routes_long_names)

    end = time.time()

    logging.info("Run time: " + str(end - start))


if __name__ == "__main__":
    main()
