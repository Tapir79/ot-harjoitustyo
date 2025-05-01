import unittest
import pygame
from app_enums import GameAttributes
from config import LOWER_BOUNDARY, RIGHT_BOUNDARY
from ui.game_views.game.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((RIGHT_BOUNDARY, LOWER_BOUNDARY))
        self.game = Game(self.screen)

    def test_game_is_initialized_correctly(self):
        self.assertEqual(self.game.gameover_data[GameAttributes.RUNNING], True)
