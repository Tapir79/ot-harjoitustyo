import sqlite3
import unittest
from utils.db_setup_helpers import (create_test_database_connection,
                                    get_database,
                                    get_user_repository,
                                    get_user_statistics_repository)


def create_new_user_and_statistics(user_repository, user_statistics_repository):
    user = user_repository.create_user("elaine", "marley")
    user_id = user_statistics_repository.create_user_statistics(
        10, 1, user.user_id)

    return user, user_id


class TestUserStatisticsRepository(unittest.TestCase):
    def setUp(self):
        self.connection = create_test_database_connection()
        self.db = get_database(self.connection)
        self.user_repository = get_user_repository(self.db)
        self.user_statistics_repository = get_user_statistics_repository(
            self.db)

    def tearDown(self):
        self.connection.close()

    def test_create_statistics_for_existing_user(self):
        user, user_id = create_new_user_and_statistics(self.user_repository,
                                                       self.user_statistics_repository)
        user_stats = self.user_statistics_repository.get_user_statistics(
            user_id)
        self.assertEqual(user.user_id, user_id)
        self.assertEqual(user_stats.high_score, 10)
        self.assertEqual(user_stats.level, 1)

    def test_user_statistics_cannot_be_updated_with_create(self):
        user, user_id = create_new_user_and_statistics(self.user_repository,
                                                       self.user_statistics_repository)
        user_id = self.user_statistics_repository.create_user_statistics(
            20, 2, user.user_id)
        user_stats = self.user_statistics_repository.get_user_statistics(
            user_id)
        print("user s:", user_stats)

        self.assertEqual(user_stats.high_score, 10)
        self.assertEqual(user_stats.level, 1)

    def test_create_user_statistics_fails_if_user_not_found(self):
        user = self.user_repository.create_user("elaine", "marley")

        with self.assertRaises(sqlite3.IntegrityError):
            self.user_statistics_repository.create_user_statistics(
                10, 1, user.user_id + 1
            )

    def test_upsert_user_statistics(self):
        _, user_id = create_new_user_and_statistics(self.user_repository,
                                                    self.user_statistics_repository)
        updated_stats_user_id = self.user_statistics_repository.update_user_statistics(
            20, 2, user_id)

        updated_stats = self.user_statistics_repository.get_user_statistics(
            updated_stats_user_id)

        self.assertEqual(updated_stats.high_score, 20)
        self.assertEqual(updated_stats.level, 2)

    def test_upsert_statistics_fails_if_user_not_found(self):
        _, user_id = create_new_user_and_statistics(self.user_repository,
                                                    self.user_statistics_repository)

        updated_stats_user_id = self.user_statistics_repository.update_user_statistics(
            20, 2, user_id + 3)
        updated_stats = self.user_statistics_repository.get_user_statistics(
            updated_stats_user_id)
        self.assertEqual(updated_stats, None)
