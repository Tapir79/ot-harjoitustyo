import unittest
from ui.game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_game_is_initialized_correctly(self):
        self.assertEqual(self.game.running, True)
