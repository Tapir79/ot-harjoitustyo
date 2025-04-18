class Size:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get_buffered_size(self, buffer):
        """
        If 
        buffer is 1

        width = 3, 
        height = 2
        [o,o,o]
        [o,o,o]

        Area increases by 1 to all directions (buffer marked by x)
        new_width = 5 
        new_height = 4
        [x,x,x,x,x]
        [x,o,o,o,x]
        [x,o,o,o,x]
        [x,x,x,x,x]
        """
        return Size(self._width + buffer * 2, self._height + buffer * 2)
