class Hit:
    """
    Stores health-related information for a sprite.

    This class tracks how many times a sprite has been hit and the maximum number 
    of hits it can take before being considered 'dead'. It provides read/write 
    access to the current hit count, and read-only access to the maximum allowed hits.
    """

    def __init__(self, hitcount: int, max_hits: int):
        """
        Initialize the Hit object.

        Args:
            hitcount (int): The current number of hits the sprite has taken.
            max_hits (int): The maximum number of hits the sprite can take.
        """
        self._hitcount = hitcount
        self._max_hits = max_hits

    @property
    def hitcount(self):
        """
        int: The current number of hits.
        """
        return self._hitcount

    @hitcount.setter
    def hitcount(self, value):
        """
        Set the current number of hits.

        Args:
            value (int): The new hit count.
        """
        self._hitcount = value

    @property
    def max_hits(self):
        """
        int: The maximum number of hits allowed.
        """
        return self._max_hits
