import unittest
from unittest.mock import patch

from entities.general_statistics import GeneralStatistics
from entities.user_statistics import UserStatistics
from models.hit import Hit
from models.sprite_info import SpriteInfo
from services.player_service import PlayerService
from utils.game_helpers import (format_high_scores, get_ending_points, get_random_positions_around_center_point,
                                get_random_x,
                                get_random_y,
                                get_player_lives, update_single_field)
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

    def test_player_hearts_without_any_hits(self):
        position = Point(5, 5)
        size = Size(10, 10)
        hit = Hit(0, 3)
        sprite_info = SpriteInfo(position, size, 5, hit)
        player_service = PlayerService(sprite_info=sprite_info)

        hearts, broken_hearts = get_player_lives(player_service)
        self.assertEqual(hearts, 3)
        self.assertEqual(broken_hearts, 0)

    def test_player_hearts_with_hits(self):
        position = Point(5, 5)
        size = Size(10, 10)
        hit = Hit(0, 3)
        sprite_info = SpriteInfo(position, size, 5, hit)
        player_service = PlayerService(sprite_info=sprite_info)
        player_service.add_hit()

        hearts, broken_hearts = get_player_lives(player_service)
        self.assertEqual(hearts, 2)
        self.assertEqual(broken_hearts, 1)

    def test_ending_points_data_returns_3_attributes_if_user_has_statistics(self):
        current_points = 10
        user_statistics = UserStatistics(1, 8, 2, "", "")
        position = Point(20, 20)
        ending_points = get_ending_points(current_points,
                                          user_statistics,
                                          position)
        self.assertEqual(len(ending_points), 3)

    def test_ending_points_data_returns_3_attributes_if_user_has_no_statistics(self):
        current_points = 10
        user_statistics = None
        position = Point(20, 20)
        ending_points = get_ending_points(current_points,
                                          user_statistics,
                                          position)
        self.assertEqual(len(ending_points), 3)

    def test_ending_points_with_new_high_score_returns_correct_text(self):
        current_points = 10
        user_current_high_score = 8
        user_statistics = UserStatistics(1, user_current_high_score, 2, "", "")
        position = Point(20, 20)
        all_time_high_score = 20
        ending_points = get_ending_points(current_points,
                                          user_statistics,
                                          position,
                                          all_time_high_score)
        high_score_text = ending_points["text"]
        self.assertEqual(high_score_text,  f"NEW RECORD: {current_points}")

    def test_ending_points_with_lower_score_returns_correct_text(self):
        current_points = 8
        user_current_high_score = 10
        user_statistics = UserStatistics(1, user_current_high_score, 2, "", "")
        position = Point(20, 20)
        all_time_high_score = 20
        ending_points = get_ending_points(current_points,
                                          user_statistics,
                                          position,
                                          all_time_high_score)
        high_score_text = ending_points["text"]
        self.assertEqual(high_score_text,
                         f"Points / Record: {current_points}  /  {user_current_high_score}")

    def test_ending_points_with_new_all_time_high_score_returns_correct_text(self):
        current_points = 21
        user_current_high_score = 8
        user_statistics = UserStatistics(1, user_current_high_score, 2, "", "")
        position = Point(20, 20)
        all_time_high_score = 20
        ending_points = get_ending_points(current_points,
                                          user_statistics,
                                          position,
                                          all_time_high_score)
        high_score_text = ending_points["text"]
        self.assertEqual(high_score_text,
                         f"NEW HIGH SCORE: {current_points}")

    def test_ending_points_current_points_is_high_score_returns_correct_text(self):
        current_points = 8
        user_current_high_score = 8
        user_statistics = UserStatistics(1, user_current_high_score, 2, "", "")
        position = Point(20, 20)
        all_time_high_score = 20
        ending_points = get_ending_points(current_points,
                                          user_statistics,
                                          position,
                                          all_time_high_score)
        high_score_text = ending_points["text"]
        self.assertEqual(high_score_text,
                         f"NEW RECORD: {current_points}")

    def test_ending_points_current_points_is_all_time_high_score_returns_correct_text(self):
        current_points = 20
        user_current_high_score = 20
        user_statistics = UserStatistics(1, user_current_high_score, 2, "", "")
        position = Point(20, 20)
        all_time_high_score = 19
        ending_points = get_ending_points(current_points,
                                          user_statistics,
                                          position,
                                          all_time_high_score)
        high_score_text = ending_points["text"]
        self.assertEqual(high_score_text,
                         f"NEW HIGH SCORE: {current_points}")

    def test_formatting(self):
        general_stats = GeneralStatistics("elaine", "20", 2)
        rank, high_score, username = format_high_scores(0, general_stats)
        self.assertEqual(rank, "1" + " " * 7)
        self.assertEqual(high_score, "20".zfill(8) + " ")

    def test_update_single_field_with_backspace(self):
        text = update_single_field("brush", True)
        self.assertEqual(text, "brus")

    def test_update_single_field_with_new_char(self):
        text = update_single_field("brus", False, "h")
        self.assertEqual(text, "brush")

    def test_update_single_field_no_change(self):
        text = update_single_field("brush", False)
        self.assertEqual(text, "brush")
