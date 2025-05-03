from dataclasses import dataclass
from typing import Optional


@dataclass
class UserStatistics:
    """
    Entity that represents a user's game statistics.

    Attributes:
        user_id: The ID of the user this statistic belongs to.
        high_score: The user's highest score achieved in the game.
        level: The highest level the user has reached.
        created_at: Timestamp when the statistics were created.
        updated_at: Timestamp when the statistics were last updated.
    """
    user_id: int
    high_score: int
    level: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
