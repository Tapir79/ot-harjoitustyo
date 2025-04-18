from models.sprite_info import SpriteInfo
from models.size import Size


class BaseSpriteService:
    def __init__(self, sprite_info: SpriteInfo):
        self.sprite_info = sprite_info

    @property
    def size(self):
        return self.sprite_info.size

    def get_position(self):
        return self.sprite_info.get_position()

    def get_x(self):
        return self.sprite_info.get_x()

    def set_x(self, new_x):
        self.sprite_info.set_x(new_x)

    def get_y(self):
        return self.sprite_info.get_y()

    def set_y(self, new_y):
        self.sprite_info.set_y(new_y)

    def get_speed(self):
        return self.sprite_info.speed

    def set_speed(self, amount=1):
        self.sprite_info.set_speed(amount)

    def get_height(self):
        return self.sprite_info.get_height()

    def get_width(self):
        return self.sprite_info.get_width()

    def increase_speed(self, amount=1):
        current_speed = self.sprite_info.get_speed()
        self.sprite_info.set_speed(current_speed + amount)

    def decrease_speed(self, amount=1):
        current_speed = self.sprite_info.get_speed()
        self.sprite_info.set_speed(max(1, current_speed - amount))

    def add_hit(self):
        self.sprite_info.add_hit()
