from models.sprite_info import SpriteInfo


class BaseSpriteService:
    """
    The shared base class for all sprite game logic service classes. 
    Provides high-level access to sprite information and common game behavior 
    such as movement and health updates. 

    The class acts as a layer between game logic and raw sprite data.

    Attributes:
        _sprite_info (SpriteInfo): The underlying data object containing sprite state.
    """

    def __init__(self, sprite_info: SpriteInfo):
        """
        Initialize the service with a SpriteInfo object.
        """
        self._sprite_info = sprite_info

    @property
    def x(self):
        """
        The x-coordinate of the sprite.

        Returns:
            int: The x-coordinate of the sprite.
        """
        return self._sprite_info.x

    @x.setter
    def x(self, value):
        """
        Set the x-coordinate of the sprite.

        Args:
            value: The new x-coordinate.
        """
        self._sprite_info.x = value

    @property
    def y(self):
        """
        The y-coordinate of the sprite.

        Returns:
            int: The y-coordinate of the sprite.
        """
        return self._sprite_info.y

    @y.setter
    def y(self, value):
        """
        Set the y-coordinate of the sprite.

        Args:
            value: The new y-coordinate.
        """
        self._sprite_info.y = value

    @property
    def position(self):
        """
        Returns:
            tuple: The (x, y) position of the sprite.
        """
        return self._sprite_info.position_tuple

    @property
    def size(self):
        """
        Returns:
            Size: The full size object of the sprite.
        """
        return self._sprite_info.size

    def get_buffered_size(self, buffer):
        """
        Get the sprite's size expanded by a given buffer on all sides.

        Args:
            buffer (int): Amount of padding to add.

        Returns:
            Size: A new size with the buffer applied.
        """
        return self._sprite_info.size.get_buffered_size(buffer)

    @property
    def width(self):
        """
        Returns:
            int: The width of the sprite.
        """
        return self._sprite_info.width

    @property
    def height(self):
        """
        Returns:    
            int: The height of the sprite.
        """
        return self._sprite_info.height

    @property
    def hitcount(self):
        """
        Returns:
            int: The current number of hits the sprite has taken.
        """
        return self._sprite_info.hit.hitcount

    @property
    def max_hits(self):
        """
        Returns:
            int: The maximum number of hits the sprite can take.
        """
        return self._sprite_info.hit.max_hits

    def add_hit(self):
        """
        Increase the sprite's hit count by one, if not already at max.

        Returns:
            int: The updated hit count.
        """
        return self._sprite_info.add_hit()

    @property
    def is_dead(self):
        """
        Returns:
            bool: Whether the sprite has reached its max hits and is considered dead.
        """
        return self._sprite_info.is_dead()

    @property
    def speed(self):
        """
        Returns:
            int: The current movement speed of the sprite.
        """
        return self._sprite_info.speed

    @speed.setter
    def speed(self, value):
        """
        Set a new movement speed for the sprite.

        Args:
            value: The new speed value.
        """
        self._sprite_info.speed = value

    def increase_speed(self, amount=1):
        """
        Increase the sprite's speed by a given amount.

        This function is in the service class because the functionality is about game behavior 
        (like getting faster after a power-up). The speed value is stored in 
        SpriteInfo, but changing it is handled here.

        Args:
            value: The increment speed value.
        """
        self.speed += amount

    def decrease_speed(self, amount=1):
        """
        Like increase speed but opposite behaviour.

        Args:
            value: The decrement speed value.
        """
        self.speed = max(1, self.speed - amount)
