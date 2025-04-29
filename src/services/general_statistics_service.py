from repositories.general_statistics_repository import GeneralStatisticsRepository


class GeneralStatisticsService:
    def __init__(self, repository=None):
        self.repository = repository or GeneralStatisticsRepository()

    def get_top_scores(self):
        """
        Fetches the top 3 highest scores from the general_statistics view.

        Returns:
            list of dicts: Each dict contains username, high_score, and level.
        """
        return self.repository.get_top_high_scores()
