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


class ErrorMessages(str, Enum):
    FIELDS_REQUIRED = "Both fields are required."
    USERNAME_TOO_SHORT = "Username must be at least 3 characters."
    PASSWORD_TOO_SHORT = "Password must be at least 3 characters."
    USERNAME_OR_PASSWORD_FAILED = "Username and/or password failed."
    USERNAME_EXISTS = "Username already exists."
    USER_NOT_FOUND = "Could not find user."
    USER_STATISTICS_EXISTS = "User statistics already exists."
