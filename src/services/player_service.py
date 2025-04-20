from services.shooting_sprite_service import ShootingSpriteService
from models.sprite_info import SpriteInfo
from config import PLAYER_COOLDOWN


class PlayerService(ShootingSpriteService):
    """
    Manages the player's movement and shooting logic.

    Inherits ShootingSpriteService.
    """

    def __init__(self, sprite_info: SpriteInfo,
                 cooldown=PLAYER_COOLDOWN,
                 points: int = 0):
        """
        Initialize the player with sprite information and shooting cooldown.

        Args:
            sprite_info (SpriteInfo): The player's position, size, speed, and health.
            cooldown (float): The cooldown time between player shots.
        """
        super().__init__(sprite_info, cooldown=cooldown)
        self._points = points

    def move(self, key: int) -> int:
        """
        Move the player left or right within the screen boundaries.

        Args:
            x (int): Current x-coordinate of the player.
            key (str): Key pressed by the user ('a' for left, 'd' for right).
            speed (int, optional): Movement speed in pixels. Defaults to 5.
            left_boundary (int, optional): Minimum x-coordinate the player can reach. 
            Defaults to 0.
            right_boundary (int, optional): Maximum x-coordinate the player can reach. 
            Defaults to 800.
            player_width (int, optional): Width of the player sprite. 
            Used to prevent moving out of bounds.

        Returns:
            int: The updated x-coordinate after movement.
        """
        x = self.x
        width = self.width

        if key == "a":
            new_x = max(self.left_boundary, x - self.speed)
        elif key == "d":
            new_x = min(self.right_boundary - width, x + self.speed)
        else:
            new_x = x

        self.x = new_x
        return new_x

    @property
    def points(self):
        """
        int: The current amount of points
        """
        return self._points

    @points.setter
    def points(self, value: int):
        """
        Set the value of points 

        Args:
            points (int): The new value of points
        """
        self._points = value

    def add_points(self, value: int):
        """
        Increase total points by the value
        """
        self.points = self.points + value
