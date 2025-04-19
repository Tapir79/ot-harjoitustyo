from models.point import Point
from models.size import Size
from models.hit import Hit


class SpriteInfo:
    """
    Holds the basic state information of a sprite, such as position, size, speed, and health.

    This class does not include any game behavior or logic. It only stores and provides access 
    to the data needed to represent a sprite on screen. Game logic, such as movement or collision 
    response, should be handled in service classes.

    Attributes:
        position (Point): The (x, y) coordinates of the sprite.
        size (Size): The width and height of the sprite.
        speed (int): The movement speed of the sprite.
        hit (Hit): Health data that tracks how many times the sprite has been hit and the max hits allowed.
    """

    def __init__(self, position: Point, size: Size, speed: int, hit: Hit):
        """
        Initialize the SpriteInfo object.

        Args:
            position (Point): The initial position of the sprite.
            size (Size): The dimensions of the sprite.
            speed (int): The movement speed of the sprite.
            hit (Hit): The hit/health information for the sprite.
        """
        self._position = position
        self._size = size
        self._speed = speed
        self._hit = hit

    @property
    def size(self):
        """
        Size: The size object representing the width and height of the sprite.
        """
        return self._size

    @property
    def x(self):
        """
        int: The x-coordinate of the sprite.
        """
        return self._position.x

    @x.setter
    def x(self, value):
        """
        Set the x-coordinate of the sprite.
        """
        self._position.x = value

    @property
    def y(self):
        """
        int: The y-coordinate of the sprite.
        """
        return self._position.y

    @y.setter
    def y(self, value):
        """
        Set the y-coordinate of the sprite.
        """
        self._position.y = value

    @property
    def position_tuple(self):
        """
        tuple: The (x, y) coordinates of the sprite as a tuple.
        """
        return self._position.as_tuple()

    @property
    def width(self):
        """
        int: The width of the sprite.
        """
        return self._size.width

    @property
    def height(self):
        """
        int: The height of the sprite.
        """
        return self._size.height

    @property
    def speed(self):
        """
        int: The current movement speed of the sprite.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """
        Set a new speed value for the sprite.
        """
        self._speed = value

    @property
    def hit(self):
        return self._hit

    def add_hit(self):
        """
        Modifies internal health state by one.
        """
        current_hits = self._hit.hitcount
        if current_hits < self._hit.max_hits:
            self._hit.hitcount = current_hits + 1
        return self._hit.hitcount

    def is_dead(self):
        """
        Queries internal health state. 
        If all health is depleted the player is dead.
        """
        return self._hit.hitcount == self._hit.max_hits
