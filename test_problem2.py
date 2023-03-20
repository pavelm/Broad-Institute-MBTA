import unittest
import asyncio
from problem2 import *


class TestCase(unittest.TestCase):

    # tests the filtered subway routes and their ids
    def test_filtered_subway_routes_ids(self):
        list_of_subway_route_ids = get_subway_route_ids()

        self.assertTrue("Red" in list_of_subway_route_ids)
        self.assertTrue("Mattapan" in list_of_subway_route_ids)
        self.assertTrue("Orange" in list_of_subway_route_ids)
        self.assertTrue("Blue" in list_of_subway_route_ids)
        self.assertTrue("Green-B" in list_of_subway_route_ids)
        self.assertTrue("Green-C" in list_of_subway_route_ids)
        self.assertTrue("Green-D" in list_of_subway_route_ids)
        self.assertTrue("Green-E" in list_of_subway_route_ids)

    # test to make sure mattapan has the least amount of stops
    def test_route_with_least_amount_of_stops(self):
        # gets the list of subway route ids
        list_of_subway_route_ids = get_subway_route_ids()

        # sort the stops
        sorted_route_stop_dict = sort_route_stops(asyncio.run(get_route_stops(list_of_subway_route_ids)))
        route_with_least_amount_of_stops = list(sorted_route_stop_dict.keys())[0]
        count_of_stops = len(sorted_route_stop_dict[route_with_least_amount_of_stops])
        self.assertEqual(route_with_least_amount_of_stops, "Mattapan")
        self.assertEqual(count_of_stops, 8)

    # test to make sure green-e has the most amount of stops
    def test_route_with_most_amount_of_stops(self):
        # gets the list of subway route ids
        list_of_subway_route_ids = get_subway_route_ids()

        # get the routes and their corresponding stops
        route_stops = asyncio.run(get_route_stops(list_of_subway_route_ids))

        # sort route_stops
        sorted_route_stop_dict = sort_route_stops(route_stops)

        route_with_most_amount_of_stops = list(sorted_route_stop_dict.keys())[-1]

        self.assertTrue(route_with_most_amount_of_stops == "Green-E" or route_with_most_amount_of_stops == "Green-D")

    def test_connecting_stops(self):
        # get all the stops on mbta
        # gets the list of subway route ids
        list_of_subway_route_ids = get_subway_route_ids()

        # get the routes and their corresponding stops
        route_stops = asyncio.run(get_route_stops(list_of_subway_route_ids))

        # sort route_stops
        sorted_route_stop_dict = sort_route_stops(route_stops)

        # get all the stops on mbta
        all_stops = get_all_stops(sorted_route_stop_dict)

        # get stops with > 1 connections
        connecting_stops = get_connecting_stops(all_stops)

        routes_connecting_stop_dict = get_routes_of_connecting_stops(connecting_stops, sorted_route_stop_dict)

        self.assertTrue('Green-D' in routes_connecting_stop_dict['Lechmere'])
        self.assertTrue('Green-E' in routes_connecting_stop_dict['Lechmere'])

        self.assertTrue('Blue' in routes_connecting_stop_dict['Government Center'])
        self.assertTrue('Green-B' in routes_connecting_stop_dict['Government Center'])
        self.assertTrue('Green-C' in routes_connecting_stop_dict['Government Center'])
        self.assertTrue('Green-D' in routes_connecting_stop_dict['Government Center'])
        self.assertTrue('Green-E' in routes_connecting_stop_dict['Government Center'])

        self.assertTrue('Mattapan' in routes_connecting_stop_dict['Ashmont'])
        self.assertTrue('Red' in routes_connecting_stop_dict['Ashmont'])

if __name__ == '__main__':
    unittest.main()
