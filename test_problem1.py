import unittest
from problem1 import *


class TestCase(unittest.TestCase):

    # test to make sure that all the trains are included
    # https://www.mbta.com/schedules/subway
    def testFilteredTrains(self):
        # gets the filtered_subway_routes data
        # unit tests should avoid making side effects such as making http call, db calls etc.
        list_of_filtered_subway_routes = filter_subway_routes()

        # gets the long names of the subway_route
        list_of_filtered_subway_routes_long_names = get_long_names(list_of_filtered_subway_routes)

        self.assertTrue("Red Line" in list_of_filtered_subway_routes_long_names)
        self.assertTrue("Mattapan Trolley" in list_of_filtered_subway_routes_long_names)
        self.assertTrue("Orange Line" in list_of_filtered_subway_routes_long_names)
        self.assertTrue("Blue Line" in list_of_filtered_subway_routes_long_names)
        self.assertTrue("Green Line B" in list_of_filtered_subway_routes_long_names)
        self.assertTrue("Green Line C" in list_of_filtered_subway_routes_long_names)
        self.assertTrue("Green Line D" in list_of_filtered_subway_routes_long_names)
        self.assertTrue("Green Line E" in list_of_filtered_subway_routes_long_names)

    def testGetLongName(self):
        input = [{'attributes' : { 'long_name': 'Red Line'}}, {'attributes' : { 'long_name': 'Orange Line'}} ]
        expected = set(["Red Line", "Orange Line"])
        output = get_long_names(input)
        self.assertSetEqual(set(output),expected)

if __name__ == '__main__':
    unittest.main()
