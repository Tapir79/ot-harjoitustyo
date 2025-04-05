from services.base_sprite_service import BaseSpriteService
from models.sprite_info import SpriteInfo
from config import UPPER_BOUNDARY, LOWER_BOUNDARY

class BulletService(BaseSpriteService):
    def __init__(self,
                 sprite_info: SpriteInfo,
                 speed=5,
                 direction="up"):
        super().__init__(sprite_info, speed)
        self.lower_boundary = LOWER_BOUNDARY + self.sprite_info.size.height
        self.upper_boundary = UPPER_BOUNDARY - self.sprite_info.size.height
        self.direction = direction

    def move(self):
        height = self.sprite_info.size.height
        y = self.sprite_info.get_y()

        if self.direction == 'up':
            new_y = max(self.upper_boundary, y - self.speed)
        elif self.direction == 'down':
            new_y = min(self.lower_boundary, y + self.speed)
        else:
            new_y = y  # do nothing

        self.sprite_info.set_y(new_y)
        return new_y

    def update(self):
        self.move()
        return self.get_position()
