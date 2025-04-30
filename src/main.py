"""
This module initializes and starts the Space Invaders game.

It creates a Game instance, runs the main game loop, and handles
clean-up operations like quitting Pygame and exiting the system.
"""
import sys
import pygame
from config import LOWER_BOUNDARY, RIGHT_BOUNDARY
from app_enums import AppState
from entities.user import User
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
        state, user = handle_states(state, screen, game, user)

    pygame.quit()
    sys.exit()


def handle_states(state: AppState, screen, game: Game, user: User):
    """
    Handles transitions between application states.

    Depending on the current AppState, this function:
    - Shows the start screen
    - Forwards to login view
    - Forwards to create user view
    - Starts or resets the game
    - Updates the logged-in user

    Args:
        state (AppState): The current application state.
        screen: The Pygame screen surface.
        game (Game): The main game instance.
        user (User): The logged-in user (or None).

    Returns:
        tuple: (AppState, User)
            - AppState: The next state after handling the current view.
            - User: Updated user if login was successful, otherwise the original user.
    """
    if state == AppState.START_SCREEN:
        state, user = StartScreenView(screen, user).run()
    elif state == AppState.LOGIN_VIEW:
        login_view = LoginView(screen)
        state, user = login_view.run()
    elif state == AppState.CREATE_USER_VIEW:
        state, user = CreateUserView(screen).run()
    elif state == AppState.LOGOUT:
        state, user = StartScreenView(screen, None).run()
    elif state == AppState.RUN_GAME:
        game.set_user(user)
        game.reset_game(screen)
        game.run()
        state = AppState.START_SCREEN
    return state, user


def init_main():
    """
    Initialize the main display screen and window settings.

    Returns:
        Surface: The initialized Pygame screen.
    """
    pygame.init()
    display_width = RIGHT_BOUNDARY
    display_height = LOWER_BOUNDARY
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Alien Attack")

    return screen


if __name__ == "__main__":
    main()
