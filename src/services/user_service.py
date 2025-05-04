import sqlite3
from repositories.user_repository import UserRepository
from app_enums import ErrorMessages


class UserService:
    """
    Service class that handles user-related operations such as validation, registration,
    fetching user information, and authentication (login).
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the UserService with a user repository.

        Args:
            user_repository: Repository for user data operations.
        """
        self.user_repository = user_repository

    def validate_user_input(self, username: str, password: str):
        """
        Validates username and password.
        Both fields must be filled.
        Both strings must be longer or equal to 3 characters.
        Username must be at most 8 characters.
        Both must contain alphanumerical characters a-Ö or 0-9.

        Args:
            username: The username to validate.
            password: The password to validate.

        Returns:
            tuple: (bool, str or None) 
            - Valid:     (True, None) 
            - Non-valid: (False, Error message)
        """
        errors = []

        if not username or not password:
            return False, [ErrorMessages.FIELDS_REQUIRED]

        if len(username) < 3:
            errors.append(ErrorMessages.USERNAME_TOO_SHORT)
        if len(username) > 8:
            errors.append(ErrorMessages.USERNAME_TOO_LONG)
        if len(password) < 3:
            errors.append(ErrorMessages.PASSWORD_TOO_SHORT)
        if not username.isalnum():
            errors.append(ErrorMessages.USERNAME_NOT_ALPHANUM)
        if not password.isalnum():
            errors.append(ErrorMessages.PASSWORD_NOT_ALPHANUM)

        if not errors:
            return True, None
        return False, errors

    def register_user(self, username: str, password: str):
        """
        Registers a new user if the input is valid and the username is available.

        Args:
            username: The username for the new user.
            password: The password for the new user.

        Returns:
            tuple: (bool, str, User or None)
            - Success:            (True, list:str, User)
            - Not valid:          (False, list:str, None)
            - User not available: (False, list:str, None)
        """
        is_valid, errors = self.validate_user_input(username, password)
        if not is_valid:
            return False, errors, None

        try:
            user = self.user_repository.create_user(username, password)
            return True, [f"User '{username}' created!"], user
        except sqlite3.IntegrityError:
            return False, [ErrorMessages.USERNAME_EXISTS], None

    def get_user(self, user_id):
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple: (User or None, str or None)
                - Found:     (User, None)
                - Not found: (None, error message)
        """
        user = self.user_repository.get_user(user_id)
        if user is None:
            return None, ErrorMessages.USER_NOT_FOUND
        return user, None

    def login(self, username, password):
        """
        Authenticates a user with username and password.

        Args:
            username: The username.
            password: The password.

        Returns:
            tuple: (int or None, str or None)
            - success: (User ID, None).
            - fail: (None, error message).
        """
        user_id, msg = self.user_repository.check_login(username, password)
        return user_id, msg
