class Hit:
    def __init__(self, hitcount: int, max_hits: int):
        self.hitcount = hitcount
        self.max_hits = max_hits

    def get_hitcount(self):
        return self.hitcount

    def set_hit_count(self, hitcount):
        self.hitcount = hitcount

    def get_max_hits(self):
        return self.max_hits
