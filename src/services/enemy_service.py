from services.shooting_sprite_service import ShootingSpriteService
from config import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY,
    BULLET_WIDTH, BULLET_HEIGHT
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
        self._shooter = ShootingSpriteService(sprite_info, cooldown=cooldown)
        self.direction = "right"

    def __getattr__(self, name):
        return getattr(self._shooter, name)

    def __setattr__(self, name, value):
        if name in {"_shooter", "direction"}:
            super().__setattr__(name, value)
        else:
            setattr(self._shooter, name, value)

    def shoot(self, direction="down", bullet_width=BULLET_WIDTH, bullet_height=BULLET_HEIGHT):
        """
        Shoot a bullet in the given direction.

        Args:
            dir: Direction to shoot ("up" or "down").
            bullet_width: Width of the bullet.
            bullet_height: Height of the bullet.

        Returns:
            BulletService: The bullet that was created.
        """
        return self._shooter.shoot(direction, bullet_width, bullet_height)

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
        return self._shooter.x, self._shooter.y

    def _has_hit_bottom(self):
        """
        Check if the enemy has reached the bottom boundary.

        Returns:
            bool: True if the enemy is at or below the bottom boundary.
        """
        return self._shooter.y + self._shooter.height >= LOWER_BOUNDARY

    def _stop_at_bottom(self):
        """
        Stop the enemy at the lower boundary.

        Returns:
            tuple: The adjusted (x, y) position at the bottom.
        """
        self._shooter.y = LOWER_BOUNDARY - self._shooter.height
        return self._shooter.x, self._shooter.y

    def _hit_left_wall(self):
        """
        Check if the enemy has reached the left edge of the screen.

        Returns:
            bool: True if at the left boundary and moving left.
        """
        return self._shooter.x <= LEFT_BOUNDARY and self.direction == "left"

    def _drop_and_turn_right(self):
        """
        Move the enemy down one row and change direction to right.

        Returns:
            tuple: The new (x, y) position after moving and turning.
        """
        self._shooter.y += self._shooter.height
        self._shooter.x = LEFT_BOUNDARY
        self.direction = "right"
        self._shooter.increase_speed()
        return self._shooter.x, self._shooter.y

    def _hit_right_wall(self):
        """
        Check if the enemy has reached the right edge of the screen.

        Returns:
            bool: True if at the right boundary and moving right.
        """
        enemy_x = self._shooter.x + self._shooter.width

        return enemy_x >= RIGHT_BOUNDARY and self.direction == "right"

    def _drop_and_turn_left(self):
        """
        Move the enemy down one row and change direction to left.

        Returns:
            tuple: The new (x, y) position after moving and turning.
        """
        self._shooter.x = RIGHT_BOUNDARY - self._shooter.width
        self._shooter.y += self._shooter.height
        self.direction = "left"
        self._shooter.increase_speed()
        return self._shooter.x, self._shooter.y

    def _move_in_current_direction(self):
        """
        Move the enemy one step in its current direction.
        """
        if self.direction == "left":
            self._shooter.x -= self._shooter.speed
        else:
            self._shooter.x += self._shooter.speed
