from services.shooting_sprite_service import ShootingSpriteService
from models.sprite_info import SpriteInfo
from config import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY,
    ENEMY_COOLDOWN, BULLET_WIDTH, BULLET_HEIGHT
)


class EnemyService(ShootingSpriteService):
    def __init__(self, sprite_info: SpriteInfo, cooldown=ENEMY_COOLDOWN):
        super().__init__(sprite_info, cooldown=cooldown)
        self._direction = "right"

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    def shoot(self, direction="down", bullet_width=BULLET_WIDTH, bullet_height=BULLET_HEIGHT):
        return super().shoot(direction, bullet_width, bullet_height)

    def move(self):
        """
        Handles enemy movement, including boundary checks and direction changes.
        """
        if self._has_hit_bottom():
            return self._limit_to_bottom()

        if self._hit_left_wall():
            return self._drop_and_turn_right()

        if self._hit_right_wall():
            return self._drop_and_turn_left()

        self._move_in_current_direction()
        return self.x, self.y

    def _has_hit_bottom(self):
        return self.y + self.height >= LOWER_BOUNDARY

    def _limit_to_bottom(self):
        self.y = LOWER_BOUNDARY - self.height
        return self.x, self.y

    def _hit_left_wall(self):
        return self.x <= LEFT_BOUNDARY and self.direction == "left"

    def _drop_and_turn_right(self):
        self.y += self.height
        self.x = LEFT_BOUNDARY
        self.direction = "right"
        self.increase_speed()
        return self.x, self.y

    def _hit_right_wall(self):
        return self.x + self.width >= RIGHT_BOUNDARY and self.direction == "right"

    def _drop_and_turn_left(self):
        self.x = RIGHT_BOUNDARY - self.width
        self.y += self.height
        self.direction = "left"
        self.increase_speed()
        return self.x, self.y

    def _move_in_current_direction(self):
        if self.direction == "left":
            self.x -= self.speed
        else:
            self.x += self.speed
