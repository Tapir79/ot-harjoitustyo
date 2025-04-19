import time
from services.base_sprite_service import BaseSpriteService
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.hit import Hit
from models.sprite_info import SpriteInfo
from config import (
    LEFT_BOUNDARY, RIGHT_BOUNDARY, BULLET_WIDTH, BULLET_HEIGHT,
    PLAYER_BULLET_SPEED, ENEMY_BULLET_SPEED, PLAYER_COOLDOWN
)


class ShootingSpriteService(BaseSpriteService):
    def __init__(self, sprite_info: SpriteInfo, cooldown=PLAYER_COOLDOWN,
                 left_boundary=LEFT_BOUNDARY, right_boundary=RIGHT_BOUNDARY):
        super().__init__(sprite_info)
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.cooldown = cooldown
        self._last_shot = 0

    @property
    def last_shot(self):
        return self._last_shot

    @last_shot.setter
    def last_shot(self, value):
        self._last_shot = value

    def can_shoot(self):
        current_time = time.time()
        if current_time - self._last_shot >= self.cooldown:
            self._last_shot = current_time
            return True
        return False

    def try_shoot(self, direction="up"):
        if self.can_shoot():
            return self.shoot(direction)
        return None

    def shoot(self, direction="up", bullet_width=BULLET_WIDTH, bullet_height=BULLET_HEIGHT):
        """
        Create a new bullet.
        """
        sprite_x, sprite_y = self.position

        bullet_x = sprite_x + self.width // 2 - bullet_width // 2
        bullet_y = self._get_bullet_y(direction, sprite_y, bullet_height)

        bullet_position = Point(bullet_x, bullet_y)
        bullet_size = Size(bullet_width, bullet_height)
        bullet_speed = PLAYER_BULLET_SPEED if direction == "up" else ENEMY_BULLET_SPEED
        bullet_sprite_info = SpriteInfo(
            bullet_position, bullet_size, bullet_speed, Hit(0, 1)
        )

        return BulletService(sprite_info=bullet_sprite_info, direction=direction)

    def _get_bullet_y(self, direction, sprite_y, bullet_height):
        if direction == "down":
            return sprite_y + self.height + bullet_height
        return sprite_y - bullet_height
