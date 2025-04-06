import unittest
from services.player_service import PlayerService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from config import RIGHT_BOUNDARY
from services.bullet_service import BulletService


class TestPlayer(unittest.TestCase):
    def setUp(self):
        position = Point(5, 5)
        size = Size(10, 10)
        self.sprite_info = SpriteInfo(position, size)
        self.player_service = PlayerService(sprite_info=self.sprite_info)

    def test_player_shoot_creates_new_bullet(self):
        bullet = self.player_service.shoot()

        bullet_width = 5
        bullet_height = 10
        player_x, player_y = self.player_service.get_position()

        bullet_x = player_x + self.player_service.sprite_info.size.width // 2 - bullet_width // 2
        bullet_y = player_y - bullet_height

        bullet_position = Point(bullet_x, bullet_y)
        bullet_size = Size(bullet_width, bullet_height)
        bullet_sprite_info = SpriteInfo(bullet_position, bullet_size)
        expected_bullet = BulletService(
            sprite_info=bullet_sprite_info, direction="up")

        self.assertEqual(bullet.direction, expected_bullet.direction,
                         "Expected a bullet direction up")
        self.assertEqual(bullet.speed, expected_bullet.speed,
                         "Expected a bullet speed 5")

    def test_player_moves_left(self):
        self.player_service.move('a')
        self.assertEqual(self.player_service.sprite_info.get_x(),
                         0, "Player should move left")

    def test_player_cannot_move_out_of_bounds_to_left(self):
        self.player_service.set_speed(10)
        self.player_service.move('a')
        self.assertEqual(self.player_service.sprite_info.get_x(), 0,
                         "Player should not move out of bounds to left")

    def test_player_moves_right(self):
        self.player_service.move('d')
        self.assertEqual(self.player_service.sprite_info.get_x(),
                         10, "Player should move right")

    def test_player_cannot_move_out_of_bounds_to_right(self):
        self.player_service.set_speed(RIGHT_BOUNDARY + 1)
        self.player_service.move('d')
        max_x = RIGHT_BOUNDARY - self.player_service.sprite_info.size.width
        self.assertEqual(self.player_service.sprite_info.get_x(), max_x,
                         "Player should not move out of bounds to right")

    def test_invalid_key_does_nothing(self):
        player_pos_x = self.player_service.sprite_info.get_x()
        self.player_service.move('w')
        self.assertEqual(self.player_service.sprite_info.get_x(), player_pos_x,
                         "Player position should not change if a or d is not pressed")

    def test_player_speed_increases(self):
        self.player_service.increase_speed(2)
        self.assertEqual(self.player_service.speed, 7,
                         "Player speed should increase")

    def test_player_speed_decreases(self):
        self.player_service.decrease_speed(2)
        self.assertEqual(self.player_service.speed, 3,
                         "Player speed should decrease")


# TODO collision tests with enemy and bullet
