import time
import unittest
from services.player_service import PlayerService
from models.point import Point
from models.size import Size
from models.hit import Hit
from models.sprite_info import SpriteInfo
from config import RIGHT_BOUNDARY, BULLET_WIDTH, BULLET_HEIGHT
from services.bullet_service import BulletService


def create_player_bullet(player_service):
    player_service.last_shot = 0
    return player_service.try_shoot()


def get_expected_bullet(player_service):
    bullet_width = BULLET_WIDTH
    bullet_height = BULLET_HEIGHT
    player_x, player_y = player_service.get_position()
    player_width = player_service.get_width()

    bullet_x = player_x + player_width // 2 - bullet_width // 2
    bullet_y = player_y - bullet_height

    bullet_position = Point(bullet_x, bullet_y)
    bullet_size = Size(bullet_width, bullet_height)
    hit = Hit(0, 1)
    bullet_sprite_info = SpriteInfo(bullet_position, bullet_size, 5, hit)
    expected_bullet = BulletService(
        sprite_info=bullet_sprite_info, direction="up")
    return expected_bullet


class TestPlayer(unittest.TestCase):
    def setUp(self):
        position = Point(5, 5)
        size = Size(10, 10)
        hit = Hit(0, 3)
        self.sprite_info = SpriteInfo(position, size, 5, hit)
        self.player_service = PlayerService(sprite_info=self.sprite_info)
        self.expected_bullet = get_expected_bullet(self.player_service)

    def test_player_shoot_creates_new_bullet(self):
        bullet = self.player_service.shoot()
        actual_speed = bullet.get_speed()
        actual_height = bullet.get_size().height

        self.assertEqual(bullet.direction, self.expected_bullet.direction,
                         "Expected a bullet direction up")
        self.assertEqual(actual_speed, self.expected_bullet.get_speed(),
                         "Expected a bullet speed 5")
        self.assertEqual(actual_height, self.expected_bullet.get_height(),
                         "Expected a bullet height 20")

    def test_player_moves_left(self):
        self.player_service.move('a')
        self.assertEqual(self.player_service.get_x(),
                         0, "Player should move left")

    def test_player_cannot_move_out_of_bounds_to_left(self):
        self.player_service.set_speed(10)
        self.player_service.move('a')
        self.assertEqual(self.player_service.get_x(), 0,
                         "Player should not move out of bounds to left")

    def test_player_moves_right(self):
        self.player_service.move('d')
        self.assertEqual(self.player_service.get_x(),
                         10, "Player should move right")

    def test_player_cannot_move_out_of_bounds_to_right(self):
        self.player_service.set_speed(RIGHT_BOUNDARY + 1)
        self.player_service.move('d')
        max_x = RIGHT_BOUNDARY - self.player_service.get_width()
        self.assertEqual(self.player_service.get_x(), max_x,
                         "Player should not move out of bounds to right")

    def test_invalid_key_does_nothing(self):
        player_pos_x = self.player_service.get_x()
        self.player_service.move('w')
        self.assertEqual(self.player_service.get_x(), player_pos_x,
                         "Player position should not change if a or d is not pressed")

    def test_player_speed_increases(self):
        self.player_service.increase_speed(2)
        self.assertEqual(self.player_service.get_speed(), 7,
                         "Player speed should increase")

    def test_player_speed_decreases(self):
        self.player_service.decrease_speed(2)
        self.assertEqual(self.player_service.get_speed(), 3,
                         "Player speed should decrease")

    def test_last_shot_time_increases_after_shooting_attempt(self):
        bullet = create_player_bullet(self.player_service)
        self.assertGreaterEqual(self.player_service.last_shot, 0)

    def test_shooting_after_cooldown(self):
        bullet = create_player_bullet(self.player_service)
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
        self.player_service.add_hit()
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
            hits_count = self.player_service.add_hit()
        return hits_count
