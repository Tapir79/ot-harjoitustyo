import sqlite3
from repositories.user_repository import create_user, get_user
from app_enums import ErrorMessages


class UserService:
    def validate_user_input(self, username: str, password: str):
        if not username or not password:
            return False, ErrorMessages.FIELDS_REQUIRED
        if len(username) < 3:
            return False, ErrorMessages.USERNAME_TOO_SHORT
        if len(password) < 3:
            return False, ErrorMessages.PASSWORD_TOO_SHORT
        return True, None

    def register_user(self, username: str, password: str):
        is_valid, error = self.validate_user_input(username, password)
        if not is_valid:
            return False, error

        try:
            create_user(username, password)
            return True, f"User '{username}' created!"
        except sqlite3.IntegrityError:
            return False, ErrorMessages.USERNAME_EXISTS
