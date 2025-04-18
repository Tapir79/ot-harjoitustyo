import unittest
from services.enemy_service import EnemyService
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.hit import Hit
from models.sprite_info import SpriteInfo
from config import LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY, ENEMY_BULLET_SPEED


class TestEnemy(unittest.TestCase):
    def setUp(self):
        position = Point(5, 5)
        size = Size(10, 10)
        hit = Hit(0, 1)
        self.sprite_info = SpriteInfo(position, size, 1, hit)
        self.enemy_service = EnemyService(sprite_info=self.sprite_info)

    def test_enemy_shoot_creates_new_bullet(self):
        bullet = self.enemy_service.shoot()

        bullet_width = 5
        bullet_height = 10
        player_x, player_y = self.enemy_service.position

        bullet_x = player_x + self.enemy_service.width // 2 - bullet_width // 2
        bullet_y = player_y - bullet_height

        bullet_position = Point(bullet_x, bullet_y)
        bullet_size = Size(bullet_width, bullet_height)
        hit = Hit(0, 1)
        bullet_sprite_info = SpriteInfo(
            bullet_position, bullet_size, ENEMY_BULLET_SPEED, hit)
        expected_bullet = BulletService(
            sprite_info=bullet_sprite_info, direction="down")

        self.assertEqual(bullet.direction, expected_bullet.direction,
                         "Expected a bullet direction down")
        self.assertEqual(bullet.speed, expected_bullet.speed,
                         "Expected a bullet speed 5")

    def test_enemy_moves_right(self):
        self.enemy_service.move()
        new_x, _ = self.enemy_service.position
        new_dir = self.enemy_service.direction
        self.assertEqual(new_x, 6)
        self.assertEqual(new_dir, "right")

    def test_enemy_moves_left(self):
        self.enemy_service.direction = "left"
        self.enemy_service.move()
        new_x, _ = self.enemy_service.position
        new_dir = self.enemy_service.direction
        self.assertEqual(new_x, 4)
        self.assertEqual(new_dir, "left")

    def test_enemy_moves_down_if_hits_right_wall(self):
        self.enemy_service.x = RIGHT_BOUNDARY + 1
        self.enemy_service.move()
        new_x, new_y = self.enemy_service.position
        self.assertEqual(new_x, RIGHT_BOUNDARY - 10)
        self.assertEqual(new_y, 15)

    def test_enemy_moves_down_if_hits_left_wall(self):
        self.enemy_service.x = LEFT_BOUNDARY - 1
        self.enemy_service.direction = "left"
        self.enemy_service.move()
        new_x, new_y = self.enemy_service.position
        self.assertEqual(new_x, 0)
        self.assertEqual(new_y, 15)

    def test_enemy_changes_direction_if_hits_right_wall(self):
        self.enemy_service.x = RIGHT_BOUNDARY + 1
        self.enemy_service.move()
        new_dir = self.enemy_service.direction
        self.assertEqual(new_dir, "left")

    def test_enemy_changes_direction_if_hits_left_wall(self):
        self.enemy_service.x = LEFT_BOUNDARY - 1
        self.enemy_service.direction = "left"
        self.enemy_service.move()
        new_dir = self.enemy_service.direction
        self.assertEqual(new_dir, "right")

    def test_enemy_speed_increases_if_hits_right_wall(self):
        self.enemy_service.x = RIGHT_BOUNDARY + 1
        self.enemy_service.move()
        new_speed = self.enemy_service.speed
        self.assertEqual(new_speed, 2)

    def test_enemy_stops_moving_if_touched_bottom(self):
        height = self.enemy_service.height
        self.enemy_service.y = LOWER_BOUNDARY - height + 5
        self.enemy_service.move()
        self.assertEqual(self.enemy_service.y,
                         LOWER_BOUNDARY - height)

     # collisions don't need tests because they are handled by pygame
