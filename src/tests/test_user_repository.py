import sqlite3
import unittest
from utils.db_setup_helpers import (create_test_database_connection,
                                    get_database,
                                    get_user_repository)


def create_new_user_and_statistics(user_repository, user_statistics_repository):
    user = user_repository.create_user("elaine", "marley")
    user_id = user_statistics_repository.create_user_statistics(
        10, 1, user.user_id)

    return user, user_id


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.connection = create_test_database_connection()
        self.db = get_database(self.connection)
        self.user_repository = get_user_repository(self.db)

    def tearDown(self):
        self.connection.close()

    def test_create_new_user_user_is_found(self):
        created_user = self.user_repository.create_user("elaine", "marley")
        fetched_user = self.user_repository.get_user(created_user.user_id)

        self.assertEqual(created_user.user_id, fetched_user.user_id)

    def test_user_is_not_found_raises_exception(self):
        user = self.user_repository.get_user(3)
        self.assertEqual(user, None)
