"""
This module defines application-wide enumerations (enums) used throughout the game.

Enums:
    - AppState: Represents different states of the application (start screen, login, game, quit).
    - CurrentField: Represents the current selected input field in forms.
    - ErrorMessages: Predefined error messages used for validation and login/registration feedback.
    - LevelAttributes: Keys for enemy attributes tied to different game levels.
"""

from enum import Enum


class AppState(str, Enum):
    START_SCREEN = "start"
    LOGIN_VIEW = "login"
    CREATE_USER_VIEW = "create_user"
    RUN_GAME = "game"
    QUIT = "quit"


class CurrentField(str, Enum):
    START = "start"
    LOGIN = "login"
    CREATE = "create"
    USERNAME = "username"
    PASSWORD = "password"


class ErrorMessages(str, Enum):
    FIELDS_REQUIRED = "Both fields are required."
    USERNAME_TOO_SHORT = "Username must be at least 3 characters."
    PASSWORD_TOO_SHORT = "Password must be at least 3 characters."
    USERNAME_OR_PASSWORD_FAILED = "Username and/or password failed."
    USERNAME_EXISTS = "Username already exists."
    USER_NOT_FOUND = "Could not find user."
    USER_STATISTICS_EXISTS = "User statistics already exists."


class LevelAttributes(str, Enum):
    ENEMY_COOLDOWN = "enemy_cooldown"
    ENEMY_SHOOT_PROB = "enemy_shoot_prob"
    ENEMY_COLS = "enemy_cols"
    ENEMY_ROWS = "enemy_rows"
    ENEMY_SPEED = "enemy_speed"
    ENEMY_BULLET_SPEED = "enemy_bullet_speed"
    ENEMY_MAX_HITS = "enemy_max_hits"
    ENEMY_IMAGE = "enemy_image"
