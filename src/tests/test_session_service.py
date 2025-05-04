import unittest

from services.session_service import SessionService
from utils.db_setup_helpers import (create_test_database_connection,
                                    get_database,
                                    get_user_service, get_user_statistics_service)


class TestSessionService(unittest.TestCase):
    def setUp(self):
        self.connection = create_test_database_connection()
        self.db = get_database(self.connection)
        self.user_service = get_user_service(self.db)
        self.user_statistics_service = get_user_statistics_service(self.db)
        self.session_service = SessionService(
            self.user_service, self.user_statistics_service)

    def test_init_user_with_no_user(self):
        user, user_statistics = self.session_service.init_user(None)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "guest")
        self.assertEqual(user_statistics.high_score, 1)
        self.assertEqual(user_statistics.level, 1)

    def test_init_user_with_new_user(self):
        success, msg, user = self.user_service.register_user(
            "elaine", "elaine")
        self.user_statistics_service.create_user_statistics(user.user_id, 0, 0)
        user, user_statistics = self.session_service.init_user(user)
        self.assertEqual(user.user_id, 2)
        self.assertEqual(user.username, "elaine")
        self.assertEqual(user_statistics.high_score, 0)
        self.assertEqual(user_statistics.level, 0)
