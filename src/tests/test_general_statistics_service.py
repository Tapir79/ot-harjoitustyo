import unittest
import sqlite3
from pathlib import Path
from entities.general_statistics import GeneralStatistics
from entities.user_statistics import UserStatistics
from repositories.general_statistics_repository import GeneralStatisticsRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.general_statistics_service import GeneralStatisticsService
from services.user_service import UserService
from repositories.user_repository import UserRepository
import db
from config import PROJECT_ROOT
from services.user_statistics_service import UserStatisticsService


class TestGeneralStatisticsService(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.row_factory = sqlite3.Row

        schema_path = Path(PROJECT_ROOT) / "data" / "schema.sql"
        with schema_path.open() as f:
            self.connection.executescript(f.read())

        self.db = db.Database(connection=self.connection)
        self.user_repository = UserRepository(self.db)
        self.service = UserService(self.user_repository)

        self.user_statistics_repository = UserStatisticsRepository(self.db)
        self.user_statistics_service = UserStatisticsService(
            self.user_statistics_repository)

        self.db = db.Database(connection=self.connection)
        self.general_stats_repository = GeneralStatisticsRepository(self.db)
        self.generals_stats_service = GeneralStatisticsService(
            self.general_stats_repository)

    def tearDown(self):
        self.connection.close()

    def test_username_and_password_must_exist(self):
        _, _, user = self.service.register_user("elaine", "marley")
        _, _ = self.user_statistics_service.create_user_statistics(
            user.user_id, 10, 1)

        top_scores = self.generals_stats_service.get_top_scores()
        actual_general_statistics = top_scores[0]
        expected_general_statistics = GeneralStatistics("elaine", 10, 1)

        self.assertEqual(len(top_scores), 1)
        self.assertEqual(actual_general_statistics.username,
                         expected_general_statistics.username)
        self.assertEqual(actual_general_statistics.high_score,
                         expected_general_statistics.high_score)
