"""
This module initializes and starts the Space Invaders game.

It creates a Game instance, runs the main game loop, and handles
clean-up operations like quitting Pygame and exiting the system.
"""
import sys
import pygame
from config import LOWER_BOUNDARY, RIGHT_BOUNDARY
from app_enums import AppState
from ui.game_views.create_user import CreateUserView
from ui.game_views.start_screen import StartScreenView
from ui.game_views.login import LoginView
from ui.game_views.game import Game


def main():
    """
    Main starting point for the game.

    Initializes the Game object, runs the game loop,
    and performs cleanup operations after the game ends.
    """

    screen = init_main()

    state = AppState.START_SCREEN
    game = Game(screen)

    user = None

    while state != AppState.QUIT:
        if state == AppState.START_SCREEN:
            state = StartScreenView(screen, user).run()
        elif state == AppState.LOGIN_VIEW:
            login_view = LoginView(screen)
            state = login_view.run()
            if login_view.user:
                user = login_view.user
        elif state == AppState.CREATE_USER_VIEW:
            state = CreateUserView(screen).run()
        elif state == AppState.RUN_GAME:
            game.set_user(user)
            game.reset_game(screen)
            game.run()
            state = AppState.START_SCREEN

    pygame.quit()
    sys.exit()


def init_main():
    pygame.init()
    display_width = RIGHT_BOUNDARY
    display_height = LOWER_BOUNDARY
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Alien Attack")

    return screen


if __name__ == "__main__":
    main()
