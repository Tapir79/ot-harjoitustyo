from services.base_sprite_service import BaseSpriteService
from models.sprite_info import SpriteInfo
from config import UPPER_BOUNDARY, LOWER_BOUNDARY


class BulletService(BaseSpriteService):
    def __init__(self,
                 sprite_info: SpriteInfo,
                 direction="up"):
        super().__init__(sprite_info)
        self.lower_boundary = LOWER_BOUNDARY + self.get_height()
        self.upper_boundary = UPPER_BOUNDARY - self.get_height()
        self.direction = direction

    def move(self):
        y = self.get_y()

        if self.direction == "up":
            new_y = max(self.upper_boundary, y - self.get_speed())
        elif self.direction == "down":
            new_y = min(self.lower_boundary, y + self.get_speed())
        else:
            new_y = y  # do nothing

        self.set_y(new_y)
        return new_y

    def update(self):
        self.move()
        return self.get_position()

    def is_moving(self):
        y = self.get_y()
        if y > LOWER_BOUNDARY and self.direction == "down":
            return False
        if y < UPPER_BOUNDARY and self.direction == "up":
            return False
        return True
