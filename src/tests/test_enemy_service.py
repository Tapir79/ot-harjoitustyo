import unittest
from services.enemy_service import EnemyService
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.hit import Hit
from models.sprite_info import SpriteInfo
from config import LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY
from level_config import ENEMY_BULLET_SPEED


class TestEnemy(unittest.TestCase):
    def setUp(self):
        position = Point(5, 5)
        size = Size(10, 10)
        hit = Hit(0, 1)
        self.sprite_info = SpriteInfo(position, size, 1, hit)
        self.enemy_service = EnemyService(sprite_info=self.sprite_info)

    def test_enemy_shoot_creates_new_bullet(self):
        bullet = self.enemy_service.try_shoot()

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
        self.assertEqual(bullet._sprite.speed, expected_bullet._sprite.speed,
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
        self.enemy_service._sprite.x = RIGHT_BOUNDARY + 1
        self.enemy_service.move()
        new_x, new_y = self.enemy_service.position
        self.assertEqual(new_x, RIGHT_BOUNDARY - 10)
        self.assertEqual(new_y, 15)

    def test_enemy_moves_down_if_hits_left_wall(self):
        self.enemy_service._sprite.x = LEFT_BOUNDARY - 1
        self.enemy_service.direction = "left"
        self.enemy_service.move()
        new_x, new_y = self.enemy_service.position
        self.assertEqual(new_x, 0)
        self.assertEqual(new_y, 15)

    def test_enemy_changes_direction_if_hits_right_wall(self):
        self.enemy_service._sprite.x = RIGHT_BOUNDARY + 1
        self.enemy_service.direction = "right"
        self.enemy_service.move()
        new_dir = self.enemy_service.direction
        self.assertEqual(new_dir, "left")

    def test_enemy_changes_direction_if_hits_left_wall(self):
        self.enemy_service._sprite.x = LEFT_BOUNDARY - 1
        self.enemy_service.direction = "left"
        self.enemy_service.move()
        new_dir = self.enemy_service.direction
        self.assertEqual(new_dir, "right")

    def test_enemy_speed_increases_if_hits_right_wall(self):
        self.enemy_service._sprite.x = RIGHT_BOUNDARY + 1
        self.enemy_service.move()
        new_speed = self.enemy_service._sprite.speed
        self.assertEqual(new_speed, 2)

    def test_enemy_stops_moving_if_touched_bottom(self):
        height = self.enemy_service.height
        self.enemy_service._sprite.y = LOWER_BOUNDARY - height + 5
        self.enemy_service.move()
        self.assertEqual(self.enemy_service._sprite.y,
                         LOWER_BOUNDARY - height)

    def test_enemy_tries_shooting_after_cooldown(self):
        self.enemy_service._shooter.last_shot = 0
        can_shoot = self.enemy_service.can_shoot()
        self.assertEqual(can_shoot, True)

    def test_enemy_is_dead_if_one_hit(self):
        self.enemy_service.add_hit()
        is_dead = self.enemy_service.is_dead
        self.assertEqual(is_dead, True)

    def test_enemy_is_dead_with_2_hits(self):
        hits_count = self.enemy_service.add_hit()
        self.assertEqual(hits_count, 1)

    def test_enemy_service_creation(self):
        point = Point(1, 2)
        size = Size(200, 400)
        speed = 1
        enemy_max_hits = 2
        enemy_cooldown = 2
        enemy_service = EnemyService.create(point,
                                            size,
                                            speed,
                                            enemy_max_hits,
                                            enemy_cooldown)

        self.assertEqual(enemy_service._shooter.cooldown, enemy_cooldown)
        self.assertEqual(enemy_service._sprite.hitcount, 0)
        self.assertEqual(enemy_service.is_dead, False)
        self.assertEqual(enemy_service.size.width, size.width)

     # collisions don't need tests because they are handled by pygame
