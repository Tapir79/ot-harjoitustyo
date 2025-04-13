import time
import unittest
from services.player_service import PlayerService
from models.point import Point
from models.size import Size
from models.hit import Hit
from models.sprite_info import SpriteInfo
from config import RIGHT_BOUNDARY
from services.bullet_service import BulletService


class TestPlayer(unittest.TestCase):
    def setUp(self):
        position = Point(5, 5)
        size = Size(10, 10)
        hit = Hit(0, 3)
        self.sprite_info = SpriteInfo(position, size, 5, hit)
        self.player_service = PlayerService(sprite_info=self.sprite_info)

    def test_player_shoot_creates_new_bullet(self):
        bullet = self.player_service.shoot()

        bullet_width = 5
        bullet_height = 10
        player_x, player_y = self.player_service.get_position()

        # self.player_service.sprite_info.size.width
        player_width = self.player_service.sprite_info.get_width()

        bullet_x = player_x + player_width // 2 - bullet_width // 2
        bullet_y = player_y - bullet_height

        bullet_position = Point(bullet_x, bullet_y)
        bullet_size = Size(bullet_width, bullet_height)
        hit = Hit(0, 1)
        bullet_sprite_info = SpriteInfo(bullet_position, bullet_size, 5, hit)
        expected_bullet = BulletService(
            sprite_info=bullet_sprite_info, direction="up")

        actual_speed = bullet.sprite_info.get_speed()
        expected_speed = expected_bullet.sprite_info.get_speed()

        self.assertEqual(bullet.direction, expected_bullet.direction,
                         "Expected a bullet direction up")
        self.assertEqual(actual_speed, expected_speed,
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
        self.assertEqual(self.player_service.sprite_info.speed, 7,
                         "Player speed should increase")

    def test_player_speed_decreases(self):
        self.player_service.decrease_speed(2)
        self.assertEqual(self.player_service.sprite_info.speed, 3,
                         "Player speed should decrease")

    def test_shooting_after_cooldown(self):
        self.player_service.last_shot = 0
        bullet = self.player_service.try_shoot()
        self.assertIsNotNone(bullet)

    def test_shooting_in_cooldown(self):
        self.player_service.last_shot = time.time()
        bullet = self.player_service.try_shoot()
        self.assertIsNone(bullet)

    def test_player_tries_shooting_after_cooldown(self):
        self.player_service.last_shot = 0
        can_shoot = self.player_service.can_shoot()
        self.assertEqual(can_shoot, True)

    def test_player_cannot_shoot_if_in_cooldown(self):
        self.player_service.last_shot = time.time()
        can_shoot = self.player_service.can_shoot()
        self.assertEqual(can_shoot, False)

    # collisions don't need tests because they are handled by pygame

    def test_player_is_not_dead_if_one_hit(self):
        self.player_service.sprite_info.add_hit()
        is_dead = self.player_service.is_dead()
        self.assertEqual(is_dead, False)

    def test_player_is_dead_if_three_hits(self):
        self.add_player_hits(3)
        is_dead = self.player_service.is_dead()
        self.assertEqual(is_dead, True)

    def test_player_is_dead_with_3_hits(self):
        hits_count = self.add_player_hits(4)
        self.assertEqual(hits_count, 3)

    def add_player_hits(self, n):
        for i in range(0, n):
            hits_count = self.player_service.sprite_info.add_hit()
        return hits_count
