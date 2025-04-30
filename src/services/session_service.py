from db import Database
from repositories.user_repository import UserRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService


class SessionService:

    def __init__(self, user_service=None, user_statistics_service=None):
        self.user_service = user_service if user_service else UserService(
            UserRepository(Database()))
        self.user_statistics_service = (user_statistics_service
                                        if user_statistics_service
                                        else UserStatisticsService(
                                            UserStatisticsRepository(
                                                Database()
                                            )))

    def init_user(self, user):
        """
        Fetch default user if user is None
        Fetch user statistics
        """
        if user is None:
            user, _ = self.user_service.get_user(1)
        user_statistics, _ = self.user_statistics_service.get_user_statistics(
            user.user_id)

        return user, user_statistics
