from services.shooting_sprite_service import ShootingSpriteService
from models.sprite_info import SpriteInfo
from config import PLAYER_COOLDOWN


class PlayerService():
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
            points (int, optional): The initial points of the player. Defaults to 0.
        """
        self._shooter = ShootingSpriteService(sprite_info, cooldown=cooldown)
        self.points = points

    def __getattr__(self, name):
        return getattr(self._shooter, name)

    def __setattr__(self, name, value):
        if name in {"_shooter", "points"}:
            super().__setattr__(name, value)
        else:
            setattr(self._shooter, name, value)

    def can_shoot(self):
        return self._shooter.can_shoot()

    def move(self, key: int):
        """
        Move the player left or right within the screen boundaries.

        Args:
            key: Key pressed by the user (pygame key code).

        Returns:
            int: The updated x-coordinate after movement.
        """
        local_x = self._shooter.x
        width = self.width

        if key == "a":
            new_x = max(self._shooter.left_boundary,
                        local_x - self._shooter.speed)
        elif key == "d":
            new_x = min(self._shooter.right_boundary -
                        width, local_x + self._shooter.speed)
        else:
            new_x = local_x

        self._shooter.x = new_x
        return new_x


    def add_points(self, value: int):
        """
        Increase total points by the value.

        Args:
            value: Points to add to the current score.
        """
        self.points = self.points + value
