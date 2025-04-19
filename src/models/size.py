class Size:
    """
    Represents the size (width and height) of a sprite or game object.
    """

    def __init__(self, width, height):
        """
        Initialize the Size with a given width and height.

        Args:
            width (int): The width of the object.
            height (int): The height of the object.
        """
        self._width = width
        self._height = height

    @property
    def width(self):
        """
        int: The width of the object.
        """
        return self._width

    @property
    def height(self):
        """
        int: The height of the object.
        """
        return self._height

    def get_buffered_size(self, buffer):
        """
        Returns a new Size with a buffer added to all sides.

        If buffer is 1:

        width = 3,
        height = 2
        [o,o,o]
        [o,o,o]

        Area increases by 1 in all directions (buffer marked by x)
        new_width = 5 
        new_height = 4
        [x,x,x,x,x]
        [x,o,o,o,x]
        [x,o,o,o,x]
        [x,x,x,x,x]

        Args:
            buffer (int): The number of units to add to all sides.

        Returns:
            Size: A new Size object with increased width and height.
        """
        return Size(self._width + buffer * 2, self._height + buffer * 2)
