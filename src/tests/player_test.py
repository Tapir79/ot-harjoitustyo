import unittest
from unittest.mock import patch
import pygame
from player import Player, move_player
from game import Game

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(5,5)
        self.game = Game()

    def test_player_moves_left(self):
        """Test that player moves left"""
        key = 'a'
        speed = 5
        self.player.x = move_player(self.player.x, key, speed)
        self.assertEqual(self.player.x, 0, "Player should move left")

    @patch('pygame.key.get_pressed')
    def test_player_moves_left_pygame(self, mock_get_pressed):
        """Test that player moves left"""
        mock_get_pressed.return_value = {pygame.K_a: True, pygame.K_d: False}
        self.player.handle_input()
        self.assertEqual(self.player.x, 0, "Player should move left.")

    def test_player_cannot_move_out_of_bounds_to_left(self):
        """Test that player cannot move left if x is left boundary"""
        key = 'a'
        speed = 10
        left_boundary = 0
        self.player.x = move_player(self.player.x, key, speed, left_boundary)
        self.assertEqual(self.player.x, 0, "Player should not move out of bounds to left")

    def test_player_moves_right(self):
        """Test that player moves right"""
        key = 'd'
        speed = 5
        self.player.x = move_player(self.player.x, key, speed)
        self.assertEqual(self.player.x, 10, "Player should move right")

    @patch('pygame.key.get_pressed')
    def test_player_moves_right_pygame(self, mock_get_pressed):
        """Test that player moves right"""
        mock_get_pressed.return_value = {pygame.K_a: False, pygame.K_d: True}
        self.player.handle_input()
        self.assertEqual(self.player.x, 10, "Player should move right.")

    def test_player_cannot_move_out_of_bounds_to_right(self):
        """Test that player cannot move right if x is right boundary"""
        key = 'd'
        speed = self.game.display_width + 1
        self.player.x = move_player(self.player.x, key, speed)
        max_x = self.game.display_width - self.player.width
        self.assertEqual(self.player.x, max_x, "Player should not move out of bounds to right")

    def test_invalid_key_does_nothing(self):
        """Test that player does not move if key is not a or d"""
        key = 'w'
        speed = self.game.display_width + 1
        player_pos_x = self.player.x
        self.player.x = move_player(self.player.x, key, speed)
        
        self.assertEqual(self.player.x, player_pos_x, "Player position should not change if a or d is not pressed")
