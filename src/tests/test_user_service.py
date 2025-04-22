import os
import unittest
import sqlite3
from pathlib import Path
from app_enums import ErrorMessages
from services.user_service import UserService
from repositories import user_repository
import db
from config import PROJECT_ROOT


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.row_factory = sqlite3.Row

        schema_path = Path(PROJECT_ROOT) / "data" / "schema.sql"
        with schema_path.open() as f:
            self.connection.executescript(f.read())

        db.set_connection(self.connection)

        self.service = UserService()

    def tearDown(self):
        self.connection.close()
        db.set_connection(None)

    def test_username_and_password_must_exist(self):
        success, msg = self.service.validate_user_input(None, None)
        self.assertFalse(success)
        self.assertEqual(msg, ErrorMessages.FIELDS_REQUIRED)

    def test_username_too_short(self):
        success, msg = self.service.validate_user_input("ab", "baa")
        self.assertFalse(success)
        self.assertEqual(msg, ErrorMessages.USERNAME_TOO_SHORT)

    def test_password_too_short(self):
        success, msg = self.service.validate_user_input("abb", "ba")
        self.assertFalse(success)
        self.assertEqual(msg, ErrorMessages.PASSWORD_TOO_SHORT)

    def test_register_valid_user(self):
        success, msg = self.service.register_user("guybrush", "threepwood")
        self.assertTrue(success)
        self.assertIn("created", msg.lower())

    def test_invalid_user(self):
        success, msg = self.service.register_user("ab", "ba")
        self.assertFalse(success)

    def test_user_already_created(self):
        success, msg = self.service.register_user("guybrush", "threepwood")
        self.assertTrue(success)
        self.assertIn("created", msg.lower())
        success, msg = self.service.register_user("guybrush", "threepwood")
        self.assertFalse(success)
