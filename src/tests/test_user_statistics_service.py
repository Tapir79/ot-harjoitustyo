import os
import unittest
import sqlite3
from pathlib import Path
from app_enums import ErrorMessages
from repositories.user_statistics_repository import UserStatisticsRepository
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService
from repositories.user_repository import UserRepository
import db
from config import PROJECT_ROOT


class TestUserStatisticsService(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.row_factory = sqlite3.Row

        schema_path = Path(PROJECT_ROOT) / "data" / "schema.sql"
        with schema_path.open() as f:
            self.connection.executescript(f.read())

        self.db = db.Database(connection=self.connection)
        self.user_statistics_repository = UserStatisticsRepository(self.db)
        self.user_statistics_service = UserStatisticsService(
            self.user_statistics_repository)
        self.user_repository = UserRepository(self.db)
        self.user_service = UserService(self.user_repository)

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
