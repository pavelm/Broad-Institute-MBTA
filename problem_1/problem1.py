import requests
import logging

logging.basicConfig(level=logging.INFO)


# purpose: returns a list of routes with the specific filter given in the arguments
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


# prints the long_name of subway routes
def print_filtered_subway_routes(list_of_subway_routes):
    for subway_route in list_of_subway_routes:
        logging.info(" " + subway_route['attributes']['long_name'])


def main():
    print_filtered_subway_routes(filter_subway_routes())


if __name__ == "__main__":
    main()
