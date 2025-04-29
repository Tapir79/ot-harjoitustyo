from db import Database
from entities.general_statistics import GeneralStatistics


class GeneralStatisticsRepository:
    def __init__(self, db=None):
        self._db = db or Database()

    def get_top_high_scores(self):
        sql = """SELECT username, high_score, level
                 FROM general_statistics"""
        rows = self._db.query(sql)
        return [GeneralStatistics(row["username"], row["high_score"], row["level"]) for row in rows]
