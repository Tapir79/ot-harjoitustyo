from services.base_sprite_service import BaseSpriteService
from models.sprite_info import SpriteInfo
from config import UPPER_BOUNDARY, LOWER_BOUNDARY


class BulletService(BaseSpriteService):
    """
    Controls the movement and state of a bullet in the game.

    Inherits basic sprite properties from BaseSpriteService and adds 
    behavior for bullet movement and boundary checks.
    """

    def __init__(self, sprite_info: SpriteInfo, direction="up"):
        """
        Initialize the bullet with its sprite info and movement direction.

        Args:
            sprite_info (SpriteInfo): The bullet's position, size, speed, and hit data.
            direction (str): The direction the bullet moves ("up" or "down").
        """
        super().__init__(sprite_info)
        self._lower_boundary = LOWER_BOUNDARY + self.height
        self._upper_boundary = UPPER_BOUNDARY - self.height
        self._direction = direction

    @property
    def direction(self):
        """
        str: The direction the bullet is moving ("up" or "down").
        """
        return self._direction

    def move(self):
        """
        Move the bullet in its direction, limited by screen boundaries.

        int: The updated y-position after moving.
        """
        if self.direction == "up":
            self.y = max(self._upper_boundary, self.y - self.speed)
        elif self.direction == "down":
            self.y = min(self._lower_boundary, self.y + self.speed)
        # else do nothing
        return self.y

    def update(self):
        """
        Update the bullet's position every frame.

        tuple: The new (x, y) position after moving.
        """
        self.move()
        return self.position

    def is_moving(self):
        """
        Check if the bullet is still moving. Bullet needs to be in the allowed move area 
        (inside boundaries).

        bool: If the bullet has reached its end boundary -> False, otherwise -> True.
        """
        if self.direction == "down" and self.y > LOWER_BOUNDARY:
            return False
        if self.direction == "up" and self.y < UPPER_BOUNDARY:
            return False
        return True
