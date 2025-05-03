from services.base_sprite_service import BaseSpriteService
from services.shooting_service import ShootingService
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
        self._sprite = BaseSpriteService(sprite_info)
        self._shooter = ShootingService(cooldown=cooldown)
        self.points = points

    @property
    def width(self):
        return self._sprite.width

    @property
    def height(self):
        return self._sprite.height
    
    @property
    def size(self):
        return self._sprite.size

    @property
    def is_dead(self):
        return self._sprite.is_dead

    @property
    def position(self):
        return self._sprite.position

    @property
    def hitcount(self):
        return self._sprite.hitcount

    @property
    def max_hits(self):
        return self._sprite.max_hits

    def add_hit(self):
        self._sprite.add_hit()

    def try_shoot(self):
        return self._shooter.try_shoot(self._sprite.position, self._sprite.size, direction="up")

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
        local_x = self._sprite.x
        width = self._sprite.width

        if key == "a":
            new_x = max(self._shooter.left_boundary,
                        local_x - self._sprite.speed)
        elif key == "d":
            new_x = min(self._shooter.right_boundary -
                        width, local_x + self._sprite.speed)
        else:
            return self._sprite.x

        self._sprite.x = new_x
        return new_x

    def add_points(self, value: int):
        """
        Increase total points by the value.

        Args:
            value: Points to add to the current score.
        """
        self.points = self.points + value
