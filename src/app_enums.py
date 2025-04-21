from enum import Enum


class AppState(str, Enum):
    START_SCREEN = "start"
    LOGIN_VIEW = "login"
    CREATE_USER_VIEW = "create_user"
    GAME_RUNNING = "game"
    QUIT = "quit"


class CurrentField(str, Enum):
    START = "start"
    LOGIN = "login"
    CREATE = "create"
    USERNAME = "username"
    PASSWORD = "password"
