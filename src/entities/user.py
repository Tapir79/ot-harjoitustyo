from dataclasses import dataclass


@dataclass
class User:
    """
    Entity that represents the user or player in the game.

    Attributes:
        user_id: Unique identifier for the user.
        username: The user's username.
    """
    user_id: int
    username: str
