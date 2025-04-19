class Hit:
    def __init__(self, hitcount: int, max_hits: int):
        self._hitcount = hitcount
        self._max_hits = max_hits

    @property
    def hitcount(self):
        return self._hitcount

    @hitcount.setter
    def hitcount(self, value):
        self._hitcount = value

    @property
    def max_hits(self):
        return self._max_hits
