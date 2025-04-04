import unittest
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from config import UPPER_BOUNDARY, LOWER_BOUNDARY


def create_bullet_service(y=500, direction="up", speed=5):
    position = Point(100, y)
    size = Size(10, 10)
    sprite_info = SpriteInfo(position, size)
    return BulletService(sprite_info, speed=speed, direction=direction)


class TestBulletService(unittest.TestCase):
    def setUp(self):
        self.bullet = create_bullet_service()

    def test_bullet_update(self):
        self.bullet.update()
        self.assertEqual(self.bullet.sprite_info.get_y(), 495)

    def test_bullet_moves_up(self):
        self.bullet.move()
        self.assertEqual(self.bullet.sprite_info.get_y(), 495)

    def test_bullet_moves_down(self):
        bullet = create_bullet_service(y=0, direction="down")
        bullet.move()
        self.assertEqual(bullet.sprite_info.get_y(), 5)

    def test_bullet_cannot_move_out_of_bounds_up(self):
        start_y = UPPER_BOUNDARY - 10
        bullet = create_bullet_service(y=start_y, direction="up")
        bullet.move()
        self.assertEqual(bullet.sprite_info.get_y(), start_y)

    def test_bullet_cannot_move_out_of_bounds_down(self):
        start_y = LOWER_BOUNDARY + 10
        bullet = create_bullet_service(y=start_y, direction="down")
        bullet.move()
        self.assertEqual(bullet.sprite_info.get_y(), start_y)

    def test_bullet_invalid_move(self):
        bullet = create_bullet_service(y=0, direction="left")
        bullet.move()
        self.assertEqual(bullet.sprite_info.get_y(), 0)

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


if __name__ == '__main__':
    unittest.main()
