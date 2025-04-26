from entities.user_statistics import UserStatistics


class UserStatisticsRepository:
    """
    Repository class for managing user statistics data.

    Handles retrieving, creating, and updating user statistics in the database.
    """

    def __init__(self, db):
        """
        Initializes the UserStatisticsRepository.

        Args:
            db: A database connection.
        """
        self._db = db

    def get_user_statistics(self, user_id):
        """
        Retrieves user statistics by user ID.

        Args:
            user_id: The ID of the user whose statistics are retrieved.

        Returns:
            UserStatistics: A UserStatistics object if found, otherwise None.
        """
        sql = """SELECT user_id,
                        high_score,
                        level,
                        created_at,
                        updated_at
                 FROM user_statistics
                 WHERE user_id = ?"""
        result = self._db.query(sql, [user_id])
        if result:
            result = result[0]
            return UserStatistics(user_id=result["user_id"],
                                  high_score=result["high_score"],
                                  level=result["level"],
                                  created_at=result["created_at"],
                                  updated_at=result["updated_at"])
        return None

    def create_user_statistics(self, high_score, level, user_id):
        """
        Creates a new user statistics database row.

        Args:
            high_score: The initial high score for the user.
            level: The initial highest level reached by the user.
            user_id: The ID of the user the statistics belong to.

        Returns:
            int: The user ID associated with the newly created statistics.
        """
        sql = """INSERT INTO user_statistics (high_score, level, user_id)
                 VALUES (?, ?, ?)"""
        self._db.execute(sql, [high_score, level, user_id])
        return user_id

    def update_user_statistics(self, high_score, level, user_id):
        """
        Updates an existing user's statistics.

        Args:
            high_score: The new high score to update.
            level: The new highest level reached to update.
            user_id: The ID of the user whose statistics are updated.

        Returns:
            int: The user ID associated with the updated statistics.
        """
        sql = """UPDATE user_statistics
                 SET high_score = ?, 
                 level = ?, 
                 updated_at =  DATETIME('now')
                 WHERE user_id = ?"""
        self._db.execute(sql, [high_score, level, user_id])
        return user_id
