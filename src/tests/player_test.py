import unittest
from ui.player import PlayerSprite
from ui.game import Game
from services.player_service import PlayerService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo


class TestPlayer(unittest.TestCase):
    def setUp(self):
        position = Point(5, 5)
        size = Size(10, 10)
        sprite_info = SpriteInfo(position, size)
        self.player_service = PlayerService(sprite_info=sprite_info)
        self.player = PlayerSprite(self.player_service)
        self.game = Game()

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
        self.player_service.set_speed(self.game.display_width + 1)
        self.player_service.move('d')
        max_x = self.game.display_width - self.player_service.sprite_info.size.width
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
        
    