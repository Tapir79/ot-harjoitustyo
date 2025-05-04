from services.base_sprite_service import BaseSpriteService
from models.sprite_info import SpriteInfo
from config import UPPER_BOUNDARY, LOWER_BOUNDARY


class BulletService():
    """
    Controls the movement and state of a bullet in the game.

    Injected basic sprite properties from BaseSpriteService and adds 
    behavior for bullet movement and boundary checks.

    Attributes:
        _lower_boundary (int): The lower boundary for bullet movement.
        _upper_boundary (int): The upper boundary for bullet movement.
        _direction (str): The movement direction ("up" or "down").
    """

    def __init__(self, sprite_info: SpriteInfo, direction="up"):
        """
        Initialize the bullet with its sprite info and movement direction.

        Args:
            sprite_info: The bullet's position, size, speed, and hit data.
            direction: The direction the bullet moves ("up" or "down").
        """
        self._sprite = BaseSpriteService(sprite_info)
        self._lower_boundary = LOWER_BOUNDARY + self._sprite.height
        self._upper_boundary = UPPER_BOUNDARY - self._sprite.height
        self._direction = direction

    # def __getattr__(self, name):
    #     """
    #     Delegate attribute access to the internal BaseSpriteService.

    #     This allows the sprite service to expose the same interface as BaseSpriteService
    #     without inheriting from it. Any attribute not found on the service class itself
    #     is automatically looked up in the composed BaseSpriteService instance.

    #     Args:
    #         name (str): The name of the attribute being accessed.

    #     Returns:
    #         Any: The value of the attribute from BaseSpriteService.

    #     Raises:
    #         AttributeError: If the attribute does not exist on BaseSpriteService.
    #     """
    #     return getattr(self._sprite, name)

    # def __setattr__(self, name, value):
    #     """
    #     Delegate setting attributes to the internal BaseSpriteService.
    #     Always set BulletService's own attributes directly.

    #     Args:
    #         name: name of the attribute
    #         value: value to set for the attribute
    #     """

    #     if name in {"_sprite", "_direction", "_lower_boundary", "_upper_boundary"}:
    #         super().__setattr__(name, value)
    #     else:
    #         setattr(self._sprite, name, value)

    @property
    def direction(self):
        """
        Returns:
            str: The direction the bullet is moving ("up" or "down").
        """
        return self._direction

    def move(self):
        """
        Move the bullet in its direction, limited by screen boundaries.

        Returns:
            int: The updated y-position after moving.
        """
        if self.direction == "up":
            self._sprite.y = max(self._upper_boundary,
                                 self._sprite.y - self._sprite.speed)
        elif self.direction == "down":
            self._sprite.y = min(self._lower_boundary,
                                 self._sprite.y + self._sprite.speed)
        # else do nothing
        return self._sprite.y

    def update(self):
        """
        Update the bullet's position every frame.

        Returns:
            tuple: The new (x, y) position after moving.
        """
        self.move()
        return self._sprite.position

    def is_moving(self):
        """
        Check if the bullet is still moving. Bullet needs to be in the allowed move area 
        (inside boundaries).

        Returns:
            bool: If the bullet has reached its end boundary -> False, otherwise -> True.
        """
        if self.direction == "down" and self._sprite.y > LOWER_BOUNDARY:
            return False
        if self.direction == "up" and self._sprite.y < UPPER_BOUNDARY:
            return False
        return True
