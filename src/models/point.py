class Point:
    """
    Represents a position point in 2D space with x and y coordinates.
    """

    def __init__(self, x, y):
        """
        Initializes a Point object.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        Returns:
            x: The current x-coordinate of the point.
        """
        return self._x

    @x.setter
    def x(self, value):
        """
        Set a new x-coordinate.

        Args:
            value: The new x value.
        """
        self._x = value

    @property
    def y(self):
        """
        Returns:
            y: The current y-coordinate of the point.
        """
        return self._y

    @y.setter
    def y(self, value):
        """
        Set a new y-coordinate.

        Args:
            value: The new y value.
        """
        self._y = value

    def as_tuple(self):
        """
        Returns:
            tuple: A tuple (x, y) representing the point's coordinates.
        """
        return (self._x, self._y)
