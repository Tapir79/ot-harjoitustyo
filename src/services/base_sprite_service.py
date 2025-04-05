from models.sprite_info import SpriteInfo


class BaseSpriteService:
    def __init__(self, sprite_info: SpriteInfo, speed=5):
        self.sprite_info = sprite_info
        self.speed = speed

    def get_position(self):
        return self.sprite_info.position.as_tuple()

    def set_speed(self, amount=1):
        self.speed = amount

    def increase_speed(self, amount=1):
        self.speed += amount

    def decrease_speed(self, amount=1):
        self.speed = max(1, self.speed - amount)
