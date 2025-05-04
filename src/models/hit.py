class Hit:
    """
    Stores the health information of the sprite. 
    Hitcount tells how many hits the sprite has taken so far. 0 = full health.
    Max hits tells how many hits the sprite can take. 
    """

    def __init__(self, hitcount: int, max_hits: int):
        """
        Initialize the Hit object.

        Args:
            hitcount: The current number of hits the sprite has taken.
            max_hits: The maximum number of hits the sprite can take.
        """
        self._hitcount = hitcount
        self._max_hits = max_hits

    @property
    def hitcount(self):
        """
        Returns:
            hitcount: The current number of hits the sprite has taken.
        """
        return self._hitcount

    @hitcount.setter
    def hitcount(self, value):
        """
        Set the current number of hits.

        Args:
            value: The new hit count.
        """
        self._hitcount = value

    @property
    def max_hits(self):
        """
        Returns:
            int: The maximum number of hits the sprite can take.
        """
        return self._max_hits
