import sqlite3
from repositories.user_repository import create_user

class UserService:
    def validate_user_input(self, username: str, password: str):
        if not username or not password:
            return False, "Both fields are required."
        if len(username) < 3:
            return False, "Username must be at least 3 characters."
        if len(password) < 3:
            return False, "Password must be at least 3 characters."
        return True, None

    def register_user(self, username: str, password: str):
        is_valid, error = self.validate_user_input(username, password)
        if not is_valid:
            return False, error

        try:
            create_user(username, password)
            return True, f"User '{username}' created!"
        except sqlite3.IntegrityError:
            return False, "Username already exists"