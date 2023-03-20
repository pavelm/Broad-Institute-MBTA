import unittest
import asyncio

from problem1 import get_long_names, filter_subway_routes
from problem2 import get_subway_route_ids, get_all_stops, get_connecting_stops
from problem3 import get_line_dict, get_routes_of_connecting_stops, get_route_stops


class MyTestCase(unittest.TestCase):

    def test_line_dict(self):
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
        #
        line_dict = get_line_dict(routes_connecting_stop_dict, route_stops)

        print(line_dict)
        self.assertTrue('Green Line B' in line_dict['Red Line'])
        self.assertTrue('Green Line C' in line_dict['Red Line'])
        self.assertTrue('Green Line D' in line_dict['Red Line'])
        self.assertTrue('Green Line E' in line_dict['Red Line'])
        self.assertTrue('Orange Line' in line_dict['Red Line'])
        self.assertTrue('Mattapan Trolley' in line_dict['Red Line'])

        self.assertTrue('Red Line' in line_dict['Mattapan Trolley'])

        self.assertTrue('Red Line' in line_dict['Orange Line'])
        self.assertTrue('Green Line D' in line_dict['Orange Line'])
        self.assertTrue('Green Line E' in line_dict['Orange Line'])
        self.assertTrue('Green Line C' not in line_dict['Orange Line'])

        self.assertTrue('Orange Line' in line_dict['Blue Line'])
        self.assertTrue('Green Line B' in line_dict['Blue Line'])
        self.assertTrue('Green Line C' in line_dict['Blue Line'])
        self.assertTrue('Green Line D' in line_dict['Blue Line'])
        self.assertTrue('Green Line E' in line_dict['Blue Line'])
        self.assertTrue('Red Line' not in line_dict['Blue Line'])


if __name__ == '__main__':
    unittest.main()
