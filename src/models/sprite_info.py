from models.point import Point
from models.size import Size
from models.hit import Hit

class SpriteInfo:
    def __init__(self, position: Point, size: Size, speed: int, hit: Hit):
        self.position = position
        self.size = size
        self.speed = speed
        self.hit = hit

    def get_x(self):
        return self.position.x

    def get_y(self):
        return self.position.y

    def set_x(self, x):
        self.position.x = x

    def set_y(self, y):
        self.position.y = y

    def get_width(self):
        return self.size.get_width()

    def get_height(self):
        return self.size.get_height()

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def add_hit(self):
        current_hits = self.hit.get_hitcount()
        if current_hits < self.hit.get_max_hits():
            self.hit.set_hit_count(current_hits + 1)
        return self.hit.get_hitcount()

    def is_dead(self):
        return self.hit.get_hitcount() == self.hit.get_max_hits()
