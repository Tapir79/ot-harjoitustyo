from db import Database
from repositories.user_repository import UserRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.general_statistics_service import GeneralStatisticsService
from services.session_service import SessionService
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService


class SessionManager:
    def __init__(self, db=None):
        self.user_service = UserService(UserRepository(db))
        self.user_statistics_service = UserStatisticsService(
            UserStatisticsRepository(db))
        self.session_service = SessionService()
        self.general_statisstics_service = GeneralStatisticsService()

    def current_user(self, user):
        self.user, self.user_statistics = self.session_service.init_user(user)
        return self.user, self.user_statistics

    def top_scores(self):
        return self.general_statistics_service.get_top_scores()
