from models.point import Point
from models.size import Size
from models.hit import Hit


class SpriteInfo:
    def __init__(self, position: Point, size: Size, speed: int, hit: Hit):
        self.position = position
        self._size = size
        self.speed = speed
        self.hit = hit

    @property
    def size(self):
        return self._size

    def get_x(self):
        return self.position.x

    def get_y(self):
        return self.position.y

    def set_x(self, x):
        self.position.x = x

    def set_y(self, y):
        self.position.y = y

    def get_position(self):
        return self.position.as_tuple()

    def get_width(self):
        return self.size.width

    def get_height(self):
        return self.size.height

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def add_hit(self):
        current_hits = self.hit.hitcount
        if current_hits < self.hit.max_hits:
            self.hit.hitcount = current_hits + 1
        return self.hit.hitcount

    def is_dead(self):
        return self.hit.hitcount == self.hit.max_hits
