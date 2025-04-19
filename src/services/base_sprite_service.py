from models.sprite_info import SpriteInfo


class BaseSpriteService:
    def __init__(self, sprite_info: SpriteInfo):
        self._sprite_info = sprite_info

    def get_size(self):
        return self._sprite_info.size

    def get_buffered_size(self, buffer):
        return self._sprite_info.size.get_buffered_size(buffer)

    def get_position(self):
        return self._sprite_info.position_tuple

    def get_x(self):
        return self._sprite_info.x

    def set_x(self, new_x):
        self._sprite_info.x = new_x

    def get_y(self):
        return self._sprite_info.y

    def set_y(self, new_y):
        self._sprite_info.y = new_y

    def get_speed(self):
        return self._sprite_info.speed

    def set_speed(self, amount=1):
        self._sprite_info.speed = amount

    def get_height(self):
        return self._sprite_info.height

    def get_width(self):
        return self._sprite_info.width

    def increase_speed(self, amount=1):
        current_speed = self._sprite_info.speed
        self._sprite_info.speed = current_speed + amount

    def decrease_speed(self, amount=1):
        current_speed = self._sprite_info.speed
        self._sprite_info.speed = max(1, current_speed - amount)

    def get_hitcount(self):
        return self._sprite_info.hit.hitcount

    def get_max_hits(self):
        return self._sprite_info.hit.max_hits

    def add_hit(self):
        return self._sprite_info.add_hit()

    def is_dead(self):
        return self._sprite_info.is_dead()
