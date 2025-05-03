class Size:
    """
    Represents the size (width and height) of a sprite or game object.
    """

    def __init__(self, width, height):
        """
        Initialize the Size with a given width and height.

        Args:
            width: The width of the object.
            height: The height of the object.
        """
        self._width = width
        self._height = height

    @property
    def width(self):
        """
        Returns:
            width: The width of the object.
        """
        return self._width

    @property
    def height(self):
        """
        Returns:
            height: The height of the object.
        """
        return self._height
