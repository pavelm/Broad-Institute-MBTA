import logging
import time
from enum import IntEnum
import requests

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

class RailType(IntEnum):
    LIGHT = 0
    HEAVY = 1


# returns a list of routes with the specific filter given in the arguments
# (default to filtering by LIGHT and HEAVY rail types)
def mbta_subway_routes(apiKey, railType=[RailType.LIGHT, RailType.HEAVY]):

    # converts the enum value to it's integer type and joins all by comma
    typeFilter = ",".join(map(lambda x: str(x.value), railType))

    # Rely on the server API to filter before results are received
    r = requests.get(f'https://api-v3.mbta.com/routes?filter[type]={typeFilter}',
                     headers={"x-api-key": apiKey})

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
    return list(map(lambda subway_route: subway_route['attributes']['long_name'], list_of_subway_routes))

def main():
    start = time.time()

    apiKey = "MY_API_KEY"

    list_of_filtered_subway_routes = mbta_subway_routes(apiKey)

    list_of_filtered_subway_routes_long_names = get_long_names(list_of_filtered_subway_routes)


    # prints the long_name of subway routes
    for subway_route_long_name in list_of_filtered_subway_routes_long_names:
        logging.info(subway_route_long_name)

    end = time.time()

    logging.info("Run time: " + str(end - start))


if __name__ == "__main__":
    main()
