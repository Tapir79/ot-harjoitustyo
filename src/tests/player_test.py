import unittest
from ui.player import PlayerSprite
from ui.game import Game
from services.player_service import PlayerService


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player_service = PlayerService(5, 5)
        self.player = PlayerSprite(self.player_service)
        self.game = Game()

    def test_player_moves_left(self):
        self.player_service.move('a')
        self.assertEqual(self.player_service.x, 0, "Player should move left")

    def test_player_cannot_move_out_of_bounds_to_left(self):
        self.player_service.set_speed(10)
        self.player_service.move('a')
        self.assertEqual(self.player_service.x, 0,
                         "Player should not move out of bounds to left")

    def test_player_moves_right(self):
        self.player_service.move('d')
        self.assertEqual(self.player_service.x, 10, "Player should move right")

    def test_player_cannot_move_out_of_bounds_to_right(self):
        self.player_service.set_speed(self.game.display_width + 1)
        self.player_service.move('d')
        max_x = self.game.display_width - self.player_service.width
        self.assertEqual(self.player_service.x, max_x,
                         "Player should not move out of bounds to right")

    def test_invalid_key_does_nothing(self):
        player_pos_x = self.player_service.x
        self.player_service.move('w')
        self.assertEqual(self.player_service.x, player_pos_x,
                         "Player position should not change if a or d is not pressed")
