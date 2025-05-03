import time
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.hit import Hit
from models.sprite_info import SpriteInfo
from config import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, BULLET_WIDTH,
    BULLET_HEIGHT, PLAYER_BULLET_SPEED, PLAYER_COOLDOWN
)
from level_config import (
    ENEMY_BULLET_SPEED
)


class ShootingService():
    """
    Base class for any sprite that can shoot bullets.
    """

    def __init__(self, cooldown=PLAYER_COOLDOWN,
                 left_boundary=LEFT_BOUNDARY, right_boundary=RIGHT_BOUNDARY):
        """
        Initialize the shooting sprite with sprite info and shooting behavior.

        Args:
            sprite_info (SpriteInfo): The sprite's position, size, speed, and hit state.
            cooldown (float): Time in seconds between shots.
            left_boundary (int): Minimum x-coordinate allowed.
            right_boundary (int): Maximum x-coordinate allowed.
        """
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.cooldown = cooldown
        self.last_shot = 0

    def can_shoot(self):
        """
        Check if the sprite is in cooldown.
        If not, then the sprite can shoot.
        Otherwise not.

        Returns:
            bool: True if the sprite can shoot, False otherwise.
        """
        current_time = time.time()
        if current_time - self.last_shot >= self.cooldown:
            self.last_shot = current_time
            return True
        return False

    def try_shoot(self, sprite_position, sprite_size, direction="up"):
        """
        Attempt to shoot a bullet if cooldown is over.

        Args:
            direction: The shooting direction ("up" or "down"). Defaults to "up".

        Returns:
            BulletService or None: The created bullet if shooting was possible, otherwise None.
        """
        if self.can_shoot():
            return self.shoot(sprite_position, sprite_size, direction)
        return None

    def shoot(self,
              sprite_position,
              sprite_size,
              direction="up",
              bullet_size=Size(BULLET_WIDTH, BULLET_HEIGHT)
              ):
        """
        Create a new bullet.

        Args:
            direction: The shooting direction ("up" or "down"). Defaults to "up".
            bullet_width: Width of the bullet. Defaults to BULLET_WIDTH.
            bullet_height: Height of the bullet. Defaults to BULLET_HEIGHT.

        Returns:
            BulletService: The created bullet object.
        """
        sprite_x, sprite_y = sprite_position
        sprite_width = sprite_size.width
        sprite_height = sprite_size.height

        bullet_x = sprite_x + sprite_width // 2 - bullet_size.width // 2
        bullet_y = self._get_bullet_y(
            direction, sprite_y, sprite_height, bullet_size.height)

        bullet_position = Point(bullet_x, bullet_y)
        bullet_size = Size(bullet_size.width, bullet_size.height)
        bullet_speed = PLAYER_BULLET_SPEED if direction == "up" else ENEMY_BULLET_SPEED
        bullet_sprite_info = SpriteInfo(
            bullet_position, bullet_size, bullet_speed, Hit(0, 1)
        )

        return BulletService(sprite_info=bullet_sprite_info, direction=direction)

    def _get_bullet_y(self, direction, sprite_y, sprite_height, bullet_height):
        """
        Calculate the vertical position for a new bullet.

        Args:
            direction: The direction the bullet is moving.
            sprite_y: The y-coordinate of the sprite.
            bullet_height: The height of the bullet.

        Returns:
            int: The calculated y-coordinate for the bullet.
        """
        if direction == "down":
            return sprite_y + sprite_height + bullet_height
        return sprite_y - bullet_height
