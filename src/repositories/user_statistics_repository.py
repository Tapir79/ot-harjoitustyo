from entities.user_statistics import UserStatistics


class UserStatisticsRepository:
    def __init__(self, db):
        self._db = db

    def get_user_statistics(self, user_id):
        sql = """SELECT user_id, high_score, level
                 FROM user_statistics
                 WHERE user_id = ?"""
        result = self._db.query(sql, [user_id])
        if result:
            result = result[0]
            return UserStatistics(result["user_id"],
                                  result["high_score"],
                                  result["level"])
        return None

    def create_user_statistics(self, high_score, level, user_id):
        sql = """INSERT INTO user_statistics (high_score, level, user_id)
                 VALUES (?, ?, ?)"""
        self._db.execute(sql, [high_score, level, user_id])
        return UserStatistics(user_id, high_score, level)

    def update_user_statistics(self, high_score, level, user_id):
        sql = """UPDATE user_statistics
                 SET high_score = ?, level = ?
                 WHERE user_id = ?"""
        self._db.execute(sql, [high_score, level, user_id])
        return UserStatistics(user_id, high_score, level)
