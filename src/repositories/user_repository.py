from werkzeug.security import check_password_hash, generate_password_hash
from entities.user import User
from app_enums import ErrorMessages


class UserRepository:
    """
    Repository class for managing user-related database operations.

    Handles creating users, retrieving users by ID, and validating user login credentials.

    """

    def __init__(self, db):
        """
        Initializes the UserRepository.

        Args:
            db: A database connection
        """
        self._db = db

    def get_user(self, user_id):
        """
        Retrieves a user by their unique ID.

        Args:
            user_id: The retrieved user ID.

        Returns:
            User: A User object if the user exists, otherwise None.
        """
        sql = """SELECT id, username FROM users WHERE id = ?"""
        result = self._db.query(sql, [user_id])
        if result:
            result = result[0]
            return User(user_id=result["id"], username=result["username"])
        return None

    def create_user(self, username, password):
        """
        Creates a new unique username with a given password.

        Args:
            username: A new username.
            password: password associated to the username.

        Returns:
            User: A User object.
        """
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        user_id = self._db.execute(sql, [username, password_hash])
        return User(user_id=user_id, username=username)

    def check_login(self, username, password):
        """
        Verifies a user's login credentials.

        Args:
            username (str): The username entered by the user.
            password (str): The plaintext password entered by the user.

        Returns:
            tuple: A tuple (user_id, None) if credentials are correct, 
            tuple: A tuple (None, ErrorMessages.USER_NOT_FOUND) if user doesn't exist
            tuple: A tuple (None, USERNAME_OR_PASSWORD_FAILED) if login fails.
        """
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = self._db.query(sql, [username])
        if not result:
            return (None, ErrorMessages.USER_NOT_FOUND)

        user_id = result[0]["id"]
        password_hash = result[0]["password_hash"]
        if check_password_hash(password_hash, password):
            return (user_id, None)

        return (None, ErrorMessages.USERNAME_OR_PASSWORD_FAILED)
