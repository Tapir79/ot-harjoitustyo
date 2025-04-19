from models.point import Point
from models.size import Size
from models.hit import Hit


class SpriteInfo:
    def __init__(self, position: Point, size: Size, speed: int, hit: Hit):
        self._position = position
        self._size = size
        self._speed = speed
        self._hit = hit

    @property
    def size(self):
        return self._size

    @property
    def x(self):
        return self._position.x

    @x.setter
    def x(self, value):
        self._position.x = value

    @property
    def y(self):
        return self._position.y

    @y.setter
    def y(self, value):
        self._position.y = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Point):
        if not isinstance(value, Point):
            raise TypeError("position must be a Point instance")
        self._position = value

    @property
    def position_tuple(self):
        return self._position.as_tuple()

    @property
    def width(self):
        return self._size.width

    @property
    def height(self):
        return self._size.height

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def hit(self):
        return self._hit

    def add_hit(self):
        current_hits = self._hit.hitcount
        if current_hits < self._hit.max_hits:
            self._hit.hitcount = current_hits + 1
        return self._hit.hitcount

    def is_dead(self):
        return self._hit.hitcount == self._hit.max_hits
