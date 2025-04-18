from models.sprite_info import SpriteInfo


class BaseSpriteService:
    def __init__(self, sprite_info: SpriteInfo):
        self.sprite_info = sprite_info

    def get_position(self):
        return self.sprite_info.get_position()

    def get_y(self):
        return self.sprite_info.get_y()

    def set_y(self, new_y):
        self.sprite_info.set_y(new_y)

    def get_speed(self):
        return self.sprite_info.speed

    def set_speed(self, amount=1):
        self.sprite_info.set_speed(amount)

    def get_height(self):
        return self.sprite_info.size.height

    def get_width(self):
        return self.sprite_info.size.width

    def increase_speed(self, amount=1):
        current_speed = self.sprite_info.get_speed()
        self.sprite_info.set_speed(current_speed + amount)

    def decrease_speed(self, amount=1):
        current_speed = self.sprite_info.get_speed()
        self.sprite_info.set_speed(max(1, current_speed - amount))
