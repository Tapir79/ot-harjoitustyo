import unittest
from unittest.mock import patch

from utils.game_helpers import (get_random_positions_around_center_point, 
                                get_random_x, 
                                get_random_y)
from models.point import Point
from models.size import Size


class TestPositionsHelpers(unittest.TestCase):

    def test_get_random_x_does_not_go_over_bounds(self):
        center_x = 4
        x_offset = 8
        screen_width = 10
        actual_x = get_random_x(center_x, x_offset, screen_width)
        self.assertGreaterEqual(actual_x, 0)
        self.assertLessEqual(actual_x, 10)

    def test_get_random_x_is_inside_offset_range(self):
        center_x = 4
        x_offset = 2
        screen_width = 10
        actual_x = get_random_x(center_x, x_offset, screen_width)
        self.assertGreaterEqual(actual_x, 2)
        self.assertLessEqual(actual_x, 6)

    def test_get_random_y_does_not_go_over_bounds(self):
        center_y = 4
        y_offset = 8
        screen_height = 10
        actual_y = get_random_y(center_y, y_offset, screen_height)
        self.assertGreaterEqual(actual_y, 0)
        self.assertLessEqual(actual_y, 10)

    def test_get_random_y_is_inside_offset_range(self):
        center_y = 4
        y_offset = 2
        screen_width = 10
        actual_y = get_random_y(center_y, y_offset, screen_width)
        self.assertGreaterEqual(actual_y, 2)
        self.assertLessEqual(actual_y, 6)

    def test_random_positions_around_center_point(self):
        point = Point(4, 4)
        screen_size = Size(10, 10)
        offset = Size(2, 2)

        positions = get_random_positions_around_center_point(
            point, screen_size, offset)

        self.assertEqual(len(positions), 5)
