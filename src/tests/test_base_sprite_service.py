import unittest
from services.base_sprite_service import BaseSpriteService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo


class TestBaseSpriteService(unittest.TestCase):
    def setUp(self):
        position = Point(5, 5)
        size = Size(10, 10)
        sprite_info = SpriteInfo(position, size, 5)
        self.base_sprite_service = BaseSpriteService(sprite_info)

    def test_position(self):
        initial_position = self.base_sprite_service.get_position()
        self.assertEqual(initial_position, (5, 5),
                         "Position should be as initialized")
