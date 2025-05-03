from models.hit import Hit
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from services.base_sprite_service import BaseSpriteService
from services.shooting_service import ShootingService
from config import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY
)
from level_config import (
    ENEMY_COOLDOWN
)


class EnemyService():
    """
    Controls enemy behavior such as movement, direction changes, and shooting.

    Gets basic sprite behavior from ShootingSpriteService and adds logic
    specific to enemy movement patterns and boundary handling.
    """

    def __init__(self, sprite_info, cooldown=ENEMY_COOLDOWN):
        """
        Initialize the enemy with its sprite info and shooting cooldown.

        Args:
            sprite_info: The enemy's position, size, speed, and hit data.
            cooldown: Time in seconds between allowed shots.
        """
        self._sprite = BaseSpriteService(sprite_info)
        self._shooter = ShootingService(cooldown=cooldown)
        self.direction = "right"

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
    def position(self):
        return self._sprite.position

    @property
    def is_dead(self):
        return self._sprite.is_dead()

    @staticmethod
    def create(
            point: Point,
            size: Size,
            speed,
            enemy_max_hits,
            enemy_cooldown):
        """
        Creates EnemyService object. Simplifies the creation
        compared to the constructor.

        Args:
            - point: (x,y)
            - size: (width, height)
            - speed: how fast enemy moves as integer
            - enemy_max_hits: how many hits the enemy can take
            - enemy_cooldown: how long the enemy waits 
                            before a new shooting attempt

        Returns:
            EnemyService object
        """
        return EnemyService(
            SpriteInfo(
                point,
                size,
                speed,
                Hit(0, enemy_max_hits)),
            cooldown=enemy_cooldown)

    def add_hit(self):
        self._sprite.add_hit()

    def try_shoot(self):
        return self._shooter.try_shoot(self._sprite.position, self._sprite.size, direction="down")

    def can_shoot(self):
        return self._shooter.can_shoot()

    def move(self):
        """
        Handles enemy movement, including boundary checks and direction changes.

        Returns:
            tuple: The new (x, y) position of the enemy.
        """
        if self._has_hit_bottom():
            return self._stop_at_bottom()

        if self._hit_left_wall():
            return self._drop_and_turn_right()

        if self._hit_right_wall():
            return self._drop_and_turn_left()

        self._move_in_current_direction()
        return self._sprite.x, self._sprite.y

    def _has_hit_bottom(self):
        """
        Check if the enemy has reached the bottom boundary.

        Returns:
            bool: True if the enemy is at or below the bottom boundary.
        """
        return self._sprite.y + self._sprite.height >= LOWER_BOUNDARY

    def _stop_at_bottom(self):
        """
        Stop the enemy at the lower boundary.

        Returns:
            tuple: The adjusted (x, y) position at the bottom.
        """
        self._sprite.y = LOWER_BOUNDARY - self._sprite.height
        return self._sprite.x, self._sprite.y

    def _hit_left_wall(self):
        """
        Check if the enemy has reached the left edge of the screen.

        Returns:
            bool: True if at the left boundary and moving left.
        """
        return self._sprite.x <= LEFT_BOUNDARY and self.direction == "left"

    def _drop_and_turn_right(self):
        """
        Move the enemy down one row and change direction to right.

        Returns:
            tuple: The new (x, y) position after moving and turning.
        """
        self._sprite.y += self._sprite.height
        self._sprite.x = LEFT_BOUNDARY
        self.direction = "right"
        self._sprite.increase_speed()
        return self._sprite.x, self._sprite.y

    def _hit_right_wall(self):
        """
        Check if the enemy has reached the right edge of the screen.

        Returns:
            bool: True if at the right boundary and moving right.
        """
        enemy_x = self._sprite.x + self._sprite.width

        return enemy_x >= RIGHT_BOUNDARY and self.direction == "right"

    def _drop_and_turn_left(self):
        """
        Move the enemy down one row and change direction to left.

        Returns:
            tuple: The new (x, y) position after moving and turning.
        """
        self._sprite.x = RIGHT_BOUNDARY - self._sprite.width
        self._sprite.y += self._sprite.height
        self.direction = "left"
        self._sprite.increase_speed()
        return self._sprite.x, self._sprite.y

    def _move_in_current_direction(self):
        """
        Move the enemy one step in its current direction.
        """
        if self.direction == "left":
            self._sprite.x -= self._sprite.speed
        else:
            self._sprite.x += self._sprite.speed
