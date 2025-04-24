from werkzeug.security import check_password_hash, generate_password_hash
from entities.user import User
from app_enums import ErrorMessages


class UserRepository:
    def __init__(self, db):
        self._db = db

    def get_user(self, user_id):
        sql = """SELECT id, username FROM users WHERE id = ?"""
        result = self._db.query(sql, [user_id])
        if result:
            result = result[0]
            return User(result["id"], result["username"])
        return None

    def create_user(self, username, password):
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        user_id = self._db.execute(sql, [username, password_hash])
        return User(user_id, username)

    def check_login(self, username, password):
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = self._db.query(sql, [username])
        if not result:
            return (None, ErrorMessages.USER_NOT_FOUND)

        user_id = result[0]["id"]
        password_hash = result[0]["password_hash"]
        if check_password_hash(password_hash, password):
            return (user_id, None)

        return (None, ErrorMessages.USERNAME_OR_PASSWORD_FAILED)
