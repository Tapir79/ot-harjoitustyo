from services.shooting_sprite_service import ShootingSpriteService
from config import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY,
    BULLET_WIDTH, BULLET_HEIGHT
)
from level_config import (
    ENEMY_COOLDOWN
)


class EnemyService(ShootingSpriteService):
    """
    Controls enemy behavior such as movement, direction changes, and shooting.

    Inherits basic sprite behavior from ShootingSpriteService and adds logic
    specific to enemy movement patterns and boundary handling.
    """

    def __init__(self, sprite_info, cooldown=ENEMY_COOLDOWN):
        """
        Initialize the enemy with its sprite info and shooting cooldown.

        Args:
            sprite_info: The enemy's position, size, speed, and hit data.
            cooldown: Time in seconds between allowed shots.
        """
        super().__init__(sprite_info, cooldown=cooldown)
        self._direction = "right"

    @property
    def direction(self):
        """
        Returns:
            str: The current direction the enemy is moving ("left" or "right").
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        """
        Set the enemy's movement direction.

        Args:
            value: "left" or "right".
        """
        self._direction = value

    def shoot(self, direction="down", bullet_width=BULLET_WIDTH, bullet_height=BULLET_HEIGHT):
        """
        Shoot a bullet in the given direction.

        Args:
            direction: Direction to shoot ("up" or "down").
            bullet_width: Width of the bullet.
            bullet_height: Height of the bullet.

        Returns:
            BulletService: The bullet that was created.
        """
        return super().shoot(direction, bullet_width, bullet_height)

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
        return self.x, self.y

    def _has_hit_bottom(self):
        """
        Check if the enemy has reached the bottom boundary.

        Returns:
            bool: True if the enemy is at or below the bottom boundary.
        """
        return self.y + self.height >= LOWER_BOUNDARY

    def _stop_at_bottom(self):
        """
        Stop the enemy at the lower boundary.

        Returns:
            tuple: The adjusted (x, y) position at the bottom.
        """
        self.y = LOWER_BOUNDARY - self.height
        return self.x, self.y

    def _hit_left_wall(self):
        """
        Check if the enemy has reached the left edge of the screen.

        Returns:
            bool: True if at the left boundary and moving left.
        """
        return self.x <= LEFT_BOUNDARY and self.direction == "left"

    def _drop_and_turn_right(self):
        """
        Move the enemy down one row and change direction to right.

        Returns:
            tuple: The new (x, y) position after moving and turning.
        """
        self.y += self.height
        self.x = LEFT_BOUNDARY
        self.direction = "right"
        self.increase_speed()
        return self.x, self.y

    def _hit_right_wall(self):
        """
        Check if the enemy has reached the right edge of the screen.

        Returns:
            bool: True if at the right boundary and moving right.
        """
        return self.x + self.width >= RIGHT_BOUNDARY and self.direction == "right"

    def _drop_and_turn_left(self):
        """
        Move the enemy down one row and change direction to left.

        Returns:
            tuple: The new (x, y) position after moving and turning.
        """
        self.x = RIGHT_BOUNDARY - self.width
        self.y += self.height
        self.direction = "left"
        self.increase_speed()
        return self.x, self.y

    def _move_in_current_direction(self):
        """
        Move the enemy one step in its current direction.
        """
        if self.direction == "left":
            self.x -= self.speed
        else:
            self.x += self.speed
