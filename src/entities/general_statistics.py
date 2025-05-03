from dataclasses import dataclass


@dataclass
class GeneralStatistics:
    """
    Entity that represents a user's game statistics.

    Attributes:
        username: The user's username
        high_score: The user's highest score achieved in the game.
        level: The highest level the user has reached.
    """
    username: str
    high_score: int
    level: int
