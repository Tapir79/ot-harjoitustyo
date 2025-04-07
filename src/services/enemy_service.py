from services.shooting_sprite_service import ShootingSpriteService
from models.sprite_info import SpriteInfo
from config import LEFT_BOUNDARY, RIGHT_BOUNDARY, LOWER_BOUNDARY


class EnemyService(ShootingSpriteService):
    def __init__(self, sprite_info: SpriteInfo,
                 cooldown=1
                 ):
        sprite_info.set_speed(1)
        super().__init__(sprite_info, cooldown=cooldown)
        self.direction = "right"

    def shoot(self, direction="down", bullet_width=5, bullet_height=10):
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

        return self.sprite_info.get_x(), self.sprite_info.get_y()

    def _has_hit_bottom(self):
        y = self.sprite_info.get_y()
        height = self.sprite_info.get_height()
        return y + height >= LOWER_BOUNDARY

    def _limit_to_bottom(self):
        height = self.sprite_info.get_height()
        self.sprite_info.set_y(LOWER_BOUNDARY - height)
        return self.sprite_info.get_x(), self.sprite_info.get_y()

    def _hit_left_wall(self):
        return self.sprite_info.get_x() <= LEFT_BOUNDARY and self.direction == "left"

    def _drop_and_turn_right(self):
        y = self.sprite_info.get_y()
        height = self.sprite_info.get_height()
        self.sprite_info.set_y(y + height)
        self.sprite_info.set_x(LEFT_BOUNDARY)
        self.set_direction("right")
        self.increase_speed()
        return self.sprite_info.get_x(), self.sprite_info.get_y()

    def _hit_right_wall(self):
        x = self.sprite_info.get_x()
        width = self.sprite_info.get_width()
        return x + width >= RIGHT_BOUNDARY and self.direction == "right"

    def _drop_and_turn_left(self):
        y = self.sprite_info.get_y()
        height = self.sprite_info.get_height()
        width = self.sprite_info.get_width()
        self.sprite_info.set_x(RIGHT_BOUNDARY - width)
        self.sprite_info.set_y(y + height)
        self.set_direction("left")
        self.increase_speed()
        return self.sprite_info.get_x(), self.sprite_info.get_y()

    def _move_in_current_direction(self):
        x = self.sprite_info.get_x()
        if self.direction == "left":
            self.sprite_info.set_x(x - self.sprite_info.speed)
        if self.direction == "right":
            self.sprite_info.set_x(x + self.sprite_info.speed)

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction
