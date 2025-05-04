import unittest
from entities.general_statistics import GeneralStatistics
from utils.db_setup_helpers import (create_test_database_connection,
                                    get_database,
                                    get_general_statistics_repository,
                                    get_user_repository,
                                    get_user_statistics_repository)


class TestGeneralStatisticsRepository(unittest.TestCase):
    def setUp(self):
        self.connection = create_test_database_connection()
        self.db = get_database(self.connection)
        self.user_repository = get_user_repository(self.db)
        self.user_statistics_repository = get_user_statistics_repository(
            self.db)
        self.general_statistics_repository = get_general_statistics_repository(
            self.db)

    def tearDown(self):
        self.connection.close()

    def test_username_and_password_must_exist(self):
        user = self.user_repository.create_user("elaine", "marley")
        user_id = self.user_statistics_repository.create_user_statistics(
            10, 1, user.user_id)

        top_scores = self.general_statistics_repository.get_top_high_scores()
        actual_general_statistics = top_scores[0]
        expected_general_statistics = GeneralStatistics("elaine", 10, 1)

        self.assertEqual(user_id, user.user_id)
        self.assertEqual(len(top_scores), 2)
        self.assertEqual(actual_general_statistics.username,
                         expected_general_statistics.username)
        self.assertEqual(actual_general_statistics.high_score,
                         expected_general_statistics.high_score)
