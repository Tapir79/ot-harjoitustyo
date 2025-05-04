import unittest
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.hit import Hit
from models.sprite_info import SpriteInfo
from config import UPPER_BOUNDARY, LOWER_BOUNDARY
from utils.ui_helpers import get_buffered_size


def create_bullet_service(y=500, direction="up", speed=5):
    position = Point(100, y)
    size = Size(10, 10)
    hit = Hit(0, 1)
    sprite_info = SpriteInfo(position, size, speed, hit)
    return BulletService(sprite_info, direction=direction)


class TestBulletService(unittest.TestCase):
    def setUp(self):
        self.bullet = create_bullet_service()

    def test_bullet_update(self):
        self.bullet.update()
        self.assertEqual(self.bullet._sprite.y, 495)

    def test_bullet_moves_up(self):
        self.bullet.move()
        self.assertEqual(self.bullet._sprite.y, 495)

    def test_bullet_moves_down(self):
        bullet = create_bullet_service(y=0, direction="down")
        bullet.move()
        self.assertEqual(bullet._sprite.y, 5)

    def test_bullet_cannot_move_out_of_bounds_up(self):
        start_y = UPPER_BOUNDARY - 10
        bullet = create_bullet_service(y=start_y, direction="up")
        bullet.move()
        self.assertEqual(bullet._sprite.y, start_y)

    def test_bullet_cannot_move_out_of_bounds_down(self):
        start_y = LOWER_BOUNDARY + 10
        bullet = create_bullet_service(y=start_y, direction="down")
        bullet.move()
        self.assertEqual(bullet._sprite.y, start_y)

    def test_bullet_invalid_move(self):
        bullet = create_bullet_service(y=0, direction="left")
        bullet.move()
        self.assertEqual(bullet._sprite.y, 0)

    def test_is_bullet_moving_up(self):
        is_moving = self.bullet.is_moving()
        self.assertEqual(is_moving, True)

    def test_is_bullet_not_moving_up(self):
        start_y = UPPER_BOUNDARY - 10
        bullet = create_bullet_service(y=start_y, direction="up")
        bullet.move()
        is_moving = bullet.is_moving()
        self.assertEqual(is_moving, False)

    def test_is_bullet_not_moving_down(self):
        start_y = LOWER_BOUNDARY + 10
        bullet = create_bullet_service(y=start_y, direction="down")
        bullet.move()
        is_moving = bullet.is_moving()
        self.assertEqual(is_moving, False)

    def test_bullet_size_buffer_works_correctly(self):
        bullet = create_bullet_service(y=10, direction="down")
        buffered_size = get_buffered_size(bullet._sprite.size, 10)
        self.assertEqual(buffered_size.height, 30)

    def test_setattr_sprite_info_attribute(self):
        self.bullet._sprite.y = 123
        self.assertEqual(self.bullet._sprite.y, 123)
        self.assertEqual(self.bullet._sprite.y, 123)

    def test_setattr_bullet_service_attribute(self):
        self.bullet._direction = "down"
        self.assertEqual(self.bullet._direction, "down")
        self.assertFalse(hasattr(self.bullet._sprite, "_direction"))

    # collisions don't need tests because they are handled by pygame
