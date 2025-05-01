import unittest
from entities.general_statistics import GeneralStatistics
from tests.db_setup_helpers import (create_test_database_connection,
                                    get_database,
                                    get_general_statistics_service,
                                    get_user_service,
                                    get_user_statistics_service)


class TestGeneralStatisticsService(unittest.TestCase):
    def setUp(self):
        self.connection = create_test_database_connection()
        self.db = get_database(self.connection)
        self.user_service = get_user_service(self.db)
        self.user_statistics_service = get_user_statistics_service(self.db)
        self.generals_stats_service = get_general_statistics_service(self.db)

    def tearDown(self):
        self.connection.close()

    def test_username_and_password_must_exist(self):
        _, _, user = self.user_service.register_user("elaine", "marley")
        _, _ = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)

        top_scores = self.generals_stats_service.get_top_scores()
        actual_general_statistics = top_scores[0]
        expected_general_statistics = GeneralStatistics("elaine", 10, 1)

        self.assertEqual(len(top_scores), 2)
        self.assertEqual(actual_general_statistics.username,
                         expected_general_statistics.username)
        self.assertEqual(actual_general_statistics.high_score,
                         expected_general_statistics.high_score)
