from services.shooting_sprite_service import ShootingSpriteService
from models.sprite_info import SpriteInfo
from config import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY,
    ENEMY_COOLDOWN, BULLET_WIDTH, BULLET_HEIGHT
)


class EnemyService(ShootingSpriteService):
    def __init__(self, sprite_info: SpriteInfo,
                 cooldown=ENEMY_COOLDOWN  # 1
                 ):
        super().__init__(sprite_info, cooldown=cooldown)
        self._direction = "right"

    def shoot(self, direction="down", bullet_width=BULLET_WIDTH, bullet_height=BULLET_HEIGHT):
        return super().shoot(direction)

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

        return self.get_x(), self.get_y()

    def _has_hit_bottom(self):
        y = self.get_y()
        height = self.get_height()
        return y + height >= LOWER_BOUNDARY

    def _limit_to_bottom(self):
        height = self.get_height()
        self.set_y(LOWER_BOUNDARY - height)
        return self.get_x(), self.get_y()

    def _hit_left_wall(self):
        return self.get_x() <= LEFT_BOUNDARY and self._direction == "left"

    def _drop_and_turn_right(self):
        y = self.get_y()
        height = self.get_height()
        self.set_y(y + height)
        self.set_x(LEFT_BOUNDARY)
        self.set_direction("right")
        self.increase_speed()
        return self.get_x(), self.get_y()

    def _hit_right_wall(self):
        x = self.get_x()
        width = self.get_width()
        return x + width >= RIGHT_BOUNDARY and self._direction == "right"

    def _drop_and_turn_left(self):
        y = self.get_y()
        height = self.get_height()
        width = self.get_width()
        self.set_x(RIGHT_BOUNDARY - width)
        self.set_y(y + height)
        self.set_direction("left")
        self.increase_speed()
        return self.get_x(), self.get_y()

    def _move_in_current_direction(self):
        x = self.get_x()
        if self._direction == "left":
            self.set_x(x - self.get_speed())
        if self._direction == "right":
            self.set_x(x + self.get_speed())

    def set_direction(self, direction):
        self._direction = direction

    def get_direction(self):
        return self._direction
