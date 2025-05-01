import unittest
from app_enums import ErrorMessages
from tests.db_setup_helpers import (create_test_database_connection,
                                    get_database, get_user_service,
                                    get_user_statistics_service)


class TestUserStatisticsService(unittest.TestCase):
    def setUp(self):
        self.connection = create_test_database_connection()
        self.db = get_database(self.connection)
        self.user_service = get_user_service(self.db)
        self.user_statistics_service = get_user_statistics_service(self.db)

    def tearDown(self):
        self.connection.close()

    def test_create_statistics_for_existing_user(self):
        success, _, user = self.user_service.register_user("elaine", "marley")
        success, _ = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)
        self.assertTrue(success)

    def test_create_user_statistics_fails_if_already_created(self):
        success, _, user = self.user_service.register_user("elaine", "marley")
        success, msg = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)
        self.assertTrue(success)
        success, msg = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)
        self.assertFalse(success)
        self.assertEqual(msg, ErrorMessages.USER_STATISTICS_EXISTS)

    def test_create_user_statistics_fails_if_user_not_found(self):
        success, _, user = self.user_service.register_user("elaine", "marley")
        success, msg = self.user_statistics_service.create_user_statistics(
            user.user_id + 1, 10, 1)
        self.assertFalse(success)
        self.assertEqual(msg, ErrorMessages.USER_NOT_FOUND)

    def test_upsert_user_statistics(self):
        _, _, user = self.user_service.register_user("elaine", "marley")
        _, _ = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)
        updated_stats, msg = self.user_statistics_service.upsert_user_statistics(
            user.user_id, 50, 2)

        self.assertEqual(updated_stats.high_score, 50)
        self.assertEqual(updated_stats.level, 2)

    def test_upsert_with_lower_high_score_will_not_change(self):
        _, _, user = self.user_service.register_user("elaine", "marley")
        _, _ = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)
        updated_stats, msg = self.user_statistics_service.upsert_user_statistics(
            user.user_id, 5, 2)

        self.assertEqual(updated_stats.high_score, 10)
        self.assertEqual(updated_stats.level, 1)

    def test_upsert_with_non_existing_user_fails(self):
        _, _, user = self.user_service.register_user("elaine", "marley")
        _, _ = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)
        user_statistics, msg = self.user_statistics_service.upsert_user_statistics(
            user.user_id + 1, 50, 2)
        self.assertEqual(user_statistics, None)
        self.assertEqual(msg, ErrorMessages.USER_NOT_FOUND)
