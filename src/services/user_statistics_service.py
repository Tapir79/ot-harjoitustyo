import sqlite3
from repositories.user_statistics_repository import UserStatisticsRepository
from app_enums import ErrorMessages


class UserStatisticsService:
    def __init__(self, user_statistic_repository: UserStatisticsRepository):
        self.user_statistics_repository = user_statistic_repository

    def get_user_statistics(self, user_id):
        user_statistics = self.user_statistics_repository.get_user_statistics(
            user_id)
        if not user_statistics:
            return None, ErrorMessages.USER_NOT_FOUND
        return user_statistics, None

    def create_user_statistics(self, user_id, high_score, stage):
        existing, _ = self.get_user_statistics(user_id)
        if existing:
            return None, ErrorMessages.USER_STATISTICS_EXISTS

        try:
            new_user_statistics = self.user_statistics_repository.create_user_statistics(
                high_score, stage, user_id)
            return new_user_statistics, None
        except sqlite3.IntegrityError:
            return None, ErrorMessages.USER_NOT_FOUND

    def upsert_user_statistics(self, user_id, high_score, stage):
        user_statistics, _ = self.get_user_statistics(user_id)

        try:
            if not user_statistics:
                user_statistics = self.user_statistics_repository.create_user_statistics(
                    high_score, stage, user_id)
            elif high_score > user_statistics.high_score:
                user_statistics = self.user_statistics_repository.update_user_statistics(
                    high_score, stage, user_id)
            return user_statistics, None
        except sqlite3.IntegrityError:
            return None, ErrorMessages.USER_NOT_FOUND
