"""
This module initializes and starts the Space Invaders game.

It creates a Game instance, runs the main game loop, and handles
clean-up operations like quitting Pygame and exiting the system.
"""
import sys
import pygame
from game import Game


def main():
    """
    Main starting point for the game.

    Initializes the Game object, runs the game loop,
    and performs cleanup operations after the game ends.
    """
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
