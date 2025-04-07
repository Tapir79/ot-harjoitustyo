import time
from services.base_sprite_service import BaseSpriteService
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from config import LEFT_BOUNDARY, RIGHT_BOUNDARY


class ShootingSpriteService(BaseSpriteService):
    def __init__(self, sprite_info: SpriteInfo, cooldown=0.3,
                 left_boundary=LEFT_BOUNDARY, right_boundary=RIGHT_BOUNDARY):
        super().__init__(sprite_info)
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.cooldown = cooldown
        self.last_shot = 0

    def can_shoot(self):
        current_time = time.time()
        if current_time - self.last_shot >= self.cooldown:
            self.last_shot = current_time
            return True

        return False

    def try_shoot(self):
        if self.can_shoot():
            return self.shoot()
        return None

    def shoot(self, direction="up", bullet_width=5, bullet_height=10):
        """
        Create a new bullet.
        """
        sprite_x, sprite_y = self.get_position()

        bullet_x = sprite_x + self.sprite_info.size.width // 2 - bullet_width // 2
        bullet_y = self.get_bullet_y(direction, sprite_y, bullet_height)

        bullet_position = Point(bullet_x, bullet_y)
        bullet_size = Size(bullet_width, bullet_height)
        bullet_sprite_info = SpriteInfo(bullet_position, bullet_size, 5)

        return BulletService(sprite_info=bullet_sprite_info, direction=direction)

    def get_bullet_y(self, direction, sprite_y, bullet_height):
        if direction == "down":
            return sprite_y + self.sprite_info.size.height + bullet_height
        return sprite_y - bullet_height
