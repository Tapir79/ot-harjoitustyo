
from models.point import Point
from models.size import Size


class SpriteInfo:
    def __init__(self, position: Point, size: Size):
        self.position = position
        self.size = size

    def get_x(self):
        return self.position.x

    def get_y(self):
        return self.position.y

    def set_x(self, x):
        self.position.x = x

    def set_y(self, y):
        self.position.y = y

    def get_width(self):
        return self.size.width

    def get_height(self):
        return self.size.height
