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
    LOGOUT = "logout"
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
    USERNAME_TOO_LONG = "Username can be at most 8 characters."
    PASSWORD_TOO_SHORT = "Password must be at least 3 characters."
    USERNAME_OR_PASSWORD_FAILED = "Username and/or password failed."
    USERNAME_EXISTS = "Username already exists."
    USER_NOT_FOUND = "Could not find user."
    USER_STATISTICS_EXISTS = "User statistics already exists."
    USERNAME_NOT_ALPHANUM = "Username must contain only letters a-Ö or numbers 0-9."
    PASSWORD_NOT_ALPHANUM = "Password must contain only letters a-Ö or numbers 0-9."


class LevelAttributes(str, Enum):
    ENEMY_COOLDOWN = "enemy_cooldown"
    ENEMY_SHOOT_PROB = "enemy_shoot_prob"
    ENEMY_COLS = "enemy_cols"
    ENEMY_ROWS = "enemy_rows"
    ENEMY_SPEED = "enemy_speed"
    ENEMY_BULLET_SPEED = "enemy_bullet_speed"
    ENEMY_MAX_HITS = "enemy_max_hits"
    ENEMY_IMAGE = "enemy_image"


class GameAttributes(str, Enum):
    LEVEL = "level"
    LEVEL_STARTED = "level_started"
    TRANSITION_TIMER = "level transition timer"
    TICKS_REMAINING = "level ticks remaining"
    LEVEL_COUNTDOWN = "level_countdown"
    HEARTS = "hearts"
    BROKEN = "broken_hearts"
    RUNNING = "running"
    GAMEOVER = "gameover"
    GAMEOVER_TEXT = "gameover_text"
    COOLDOWN = "cooldown"
    SHOOT_PROB = LevelAttributes.ENEMY_SHOOT_PROB
    COLS = LevelAttributes.ENEMY_COLS
    ROWS = LevelAttributes.ENEMY_ROWS
    SPEED = LevelAttributes.ENEMY_SPEED
    BULLET_SPEED = LevelAttributes.ENEMY_BULLET_SPEED
    MAX_HITS = LevelAttributes.ENEMY_MAX_HITS
    IMAGE = LevelAttributes.ENEMY_IMAGE
    PLAYER_BULLETS = "player_bullets"
    ENEMY_BULLETS = "enemy_bullets"
    ENEMIES = "enemies"
    HITS = "hits"
    THICK_BORDER = "thick"
    THIN_BORDER = "thin"
