from repositories.user_repository import UserRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.general_statistics_service import GeneralStatisticsService
from services.session_service import SessionService
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService


class SessionManager:
    """Handles session-related services and user initialization."""

    def __init__(self, db=None):
        """
        Initializes service instances with the given database.

        Args:
            db: A database connection.
        """
        self.user_service = UserService(UserRepository(db))
        self.user_statistics_service = UserStatisticsService(
            UserStatisticsRepository(db))
        self.session_service = SessionService()
        self.general_statistics_service = GeneralStatisticsService()

    def current_user(self, user):
        """
        Initializes and returns the current user and user's statistics.

        Args:
            user: The user object.

        Returns:
            tuple: (user, user_statistics)
        """
        self.user, self.user_statistics = self.session_service.init_user(user)
        return self.user, self.user_statistics

    def top_scores(self):
        """
        Retrieves the top 3 high scores.

        Returns:
            list: A list of 3 top scores.
        """
        return self.general_statistics_service.get_top_scores()
