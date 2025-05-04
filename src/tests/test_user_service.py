import unittest

from app_enums import ErrorMessages

from utils.db_setup_helpers import (create_test_database_connection,
                                    get_database,
                                    get_user_service)


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.connection = create_test_database_connection()
        self.db = get_database(self.connection)
        self.service = get_user_service(self.db)

    def tearDown(self):
        self.connection.close()

    def test_connection(self):
        self.assertIsNotNone(self.connection)

    def test_username_and_password_must_exist(self):
        success, msg = self.service.validate_user_input(None, None)
        self.assertFalse(success)
        self.assertEqual(msg[0], ErrorMessages.FIELDS_REQUIRED)

    def test_username_too_short(self):
        success, msg = self.service.validate_user_input("ab", "baa")
        self.assertFalse(success)
        self.assertEqual(msg[0], ErrorMessages.USERNAME_TOO_SHORT)

    def test_password_too_short(self):
        success, msg = self.service.validate_user_input("abb", "ba")
        self.assertFalse(success)
        self.assertEqual(msg[0], ErrorMessages.PASSWORD_TOO_SHORT)

    def test_register_invalid_user(self):
        success, msg, _ = self.service.register_user("g", "le")
        self.assertFalse(success)
        self.assertEqual(msg[0], ErrorMessages.USERNAME_TOO_SHORT)

    def test_register_invalid_user(self):
        success, msg, _ = self.service.register_user(
            "guybrushthreepwood", "le")
        self.assertFalse(success)
        self.assertEqual(msg[0], ErrorMessages.USERNAME_TOO_LONG)

    def test_register_valid_user(self):
        success, msg, _ = self.service.register_user("mrgp", "lechuck")
        self.assertTrue(success)
        self.assertIn("created", msg[0].lower())

    def test_register_non_alphanumerical_user(self):
        success, msg, _ = self.service.register_user("g.p.", "lechuck")
        self.assertFalse(success)
        self.assertEqual(msg[0], ErrorMessages.USERNAME_NOT_ALPHANUM)

    def test_register_non_alphanumerical_password(self):
        success, msg, _ = self.service.register_user("elaine", "??=")
        self.assertFalse(success)
        self.assertEqual(msg[0], ErrorMessages.PASSWORD_NOT_ALPHANUM)

    def test_user_already_created(self):
        success, msg, _ = self.service.register_user("guybrush", "threepwood")
        self.assertTrue(success)
        self.assertIn("created", msg[0].lower())
        success, msg, _ = self.service.register_user("guybrush", "threepwood")
        self.assertFalse(success)

    def test_get_existing_user(self):
        success, _, user = self.service.register_user("elaine", "marley")
        self.assertTrue(success)
        actual_user, _ = self.service.get_user(user.user_id)
        self.assertEqual(actual_user.username, "elaine")

    def test_get_non_existing_user(self):
        success, _, user = self.service.register_user("elaine", "marley")
        self.assertTrue(success)
        _, msg = self.service.get_user(user.user_id + 1)
        self.assertEqual(msg, ErrorMessages.USER_NOT_FOUND)

    def test_user_login_success(self):
        success, _, user = self.service.register_user("elaine", "marley")
        self.assertTrue(success)
        user_id, msg = self.service.login("elaine", "marley")
        logged_in_user, _ = self.service.get_user(user_id)
        self.assertEqual(logged_in_user.username, user.username)
        self.assertEqual(logged_in_user.user_id, user_id)

    def test_user_login_fails(self):
        success, _, user = self.service.register_user("elaine", "marley")
        self.assertTrue(success)
        user_id, msg = self.service.login("guybrush", "threepwood")
        logged_in_user, msg = self.service.get_user(user_id)
        self.assertEqual(logged_in_user, None)
        self.assertEqual(msg, ErrorMessages.USER_NOT_FOUND)

    def test_passwords_do_not_match(self):
        success, _, user = self.service.register_user("elaine", "marley")
        self.assertTrue(success)
        user_id, msg = self.service.login("elaine", "threepwood")
        self.assertIsNone(user_id)
        self.assertEqual(msg, ErrorMessages.USERNAME_OR_PASSWORD_FAILED)
