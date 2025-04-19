from services.base_sprite_service import BaseSpriteService
from models.sprite_info import SpriteInfo
from config import UPPER_BOUNDARY, LOWER_BOUNDARY


class BulletService(BaseSpriteService):
    def __init__(self, sprite_info: SpriteInfo, direction="up"):
        super().__init__(sprite_info)
        self._lower_boundary = LOWER_BOUNDARY + self.height
        self._upper_boundary = UPPER_BOUNDARY - self.height
        self._direction = direction

    @property
    def direction(self):
        return self._direction

    def move(self):
        if self.direction == "up":
            self.y = max(self._upper_boundary, self.y - self.speed)
        elif self.direction == "down":
            self.y = min(self._lower_boundary, self.y + self.speed)
        # else do nothing
        return self.y

    def update(self):
        self.move()
        return self.position

    def is_moving(self):
        if self.direction == "down" and self.y > LOWER_BOUNDARY:
            return False
        if self.direction == "up" and self.y < UPPER_BOUNDARY:
            return False
        return True
