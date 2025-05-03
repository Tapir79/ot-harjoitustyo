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
        hit (Hit): Health data that tracks how many times the sprite has been hit 
                   and the max hits allowed.
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
        Returns:
            Size: The size object representing the width and height of the sprite.
        """
        return self._size

    @property
    def x(self):
        """
        Returns:
            int: The x-coordinate of the sprite.
        """
        return self._position.x

    @x.setter
    def x(self, value):
        """
        Sets a new x-coordinate.

        Args:
            value (int): The new x-coordinate.
        """
        self._position.x = value

    @property
    def y(self):
        """
        Returns:
            int: The y-coordinate of the sprite.
        """
        return self._position.y

    @y.setter
    def y(self, value):
        """
        Sets a new y-coordinate.

        Args:
            value (int): The new y-coordinate.
        """
        self._position.y = value

    @property
    def position_tuple(self):
        """
        Returns:
            tuple: The (x, y) coordinates of the sprite as a tuple.
        """
        return self._position.as_tuple()

    @property
    def width(self):
        """
        Returns:
            int: The width of the sprite.
        """
        return self._size.width

    @property
    def height(self):
        """
        Returns:
            int: The height of the sprite.
        """
        return self._size.height

    @property
    def speed(self):
        """
        Returns:
            int: The current movement speed of the sprite.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """
        Sets a new speed value for the sprite.

        Args:
            value (int): The new speed.
        """
        self._speed = value

    @property
    def hit(self):
        """
        Returns:
            Hit: The hit/health information of the sprite.
        """
        return self._hit

    @property
    def hitcount(self):
        return self._hit.hitcount

    @hitcount.setter
    def hitcount(self, value):
        self._hit.hitcount = value
