class Point:
    """
    Represents a position point in 2D space with x and y coordinates.
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        int or float: The x-coordinate of the point.
        """
        return self._x

    @x.setter
    def x(self, value):
        """
        Set a new x-coordinate.

        Args:
            value (int or float): The new x value.
        """
        self._x = value

    @property
    def y(self):
        """
        int or float: The y-coordinate of the point.
        """
        return self._y

    @y.setter
    def y(self, value):
        """
        Set a new y-coordinate.

        Args:
            value (int or float): The new y value.
        """
        self._y = value

    def as_tuple(self):
        """
        Return the point as a tuple (x, y).
        """
        return (self._x, self._y)
