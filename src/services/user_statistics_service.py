import sqlite3
from repositories.user_statistics_repository import UserStatisticsRepository
from app_enums import ErrorMessages


class UserStatisticsService:
    """
    Service class that handles user statistics operations such as fetching, creating,
    and updating user statistics.
    """

    def __init__(self, user_statistic_repository: UserStatisticsRepository):
        """
        Initializes the UserStatisticsService with a user statistics repository.

        Args:
            user_statistic_repository: Repository for user statistics data operations.
        """
        self.user_statistics_repository = user_statistic_repository

    def get_user_statistics(self, user_id):
        """
        Retrieves user statistics for a given user.

        Args:
            user_id: The ID of the user.

        Returns:
            tuple: (UserStatistics or None, str or None)
            - Found:     (UserStatistics, None)
            - Not found: (None, error message)
        """
        user_statistics = self.user_statistics_repository.get_user_statistics(
            user_id)
        if not user_statistics:
            return None, ErrorMessages.USER_NOT_FOUND
        return user_statistics, None

    def create_user_statistics(self, user_id, high_score, stage):
        """
        Creates new user statistics if no existing statistics are found for the user.

        Args:
            user_id: The ID of the user.
            high_score: The high score to initialize.
            stage: The current level or stage to initialize.

        Returns:
            tuple: (UserStatistics or None, str or None)
            - Success: (UserStatistics, None)
            - Already exists: (None, error message)
            - Failure: (None, error message)
        """
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
        """
        Updates user statistics if existing and new high score is higher.
        Creates new statistics if none exist.

        Args:
            user_id: The ID of the user.
            high_score: The new high score to update.
            stage: The current level or stage to update.

        Returns:
            tuple: (UserStatistics or None, str or None)
            - Success: (UserStatistics, None)
            - Failure: (None, error message)
        """
        user_statistics, _ = self.get_user_statistics(user_id)

        try:
            if not user_statistics:
                self.user_statistics_repository.create_user_statistics(
                    high_score, stage, user_id)
            elif high_score > user_statistics.high_score:
                self.user_statistics_repository.update_user_statistics(
                    high_score, stage, user_id)
            user_statistics = self.user_statistics_repository.get_user_statistics(
                user_id)
            return user_statistics, None
        except sqlite3.IntegrityError:
            return None, ErrorMessages.USER_NOT_FOUND
