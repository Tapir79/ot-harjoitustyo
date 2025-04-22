import sqlite3
from repositories.user_repository import UserRepository
from app_enums import ErrorMessages


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

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
            return False, error, None

        try:
            user = self.user_repository.create_user(username, password)
            return True, f"User '{username}' created!", user
        except sqlite3.IntegrityError:
            return False, ErrorMessages.USERNAME_EXISTS, None

    def get_user(self, user_id):
        user = self.user_repository.get_user(user_id)
        if user is None:
            return None, ErrorMessages.USER_NOT_FOUND
        return user, None

    def login(self, username, password):
        user_id, msg = self.user_repository.check_login(username, password)
        return user_id, msg
