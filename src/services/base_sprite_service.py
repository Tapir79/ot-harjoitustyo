from models.sprite_info import SpriteInfo


class BaseSpriteService:
    def __init__(self, sprite_info: SpriteInfo):
        self._sprite_info = sprite_info

    @property
    def x(self):
        return self._sprite_info.x

    @x.setter
    def x(self, value):
        self._sprite_info.x = value

    @property
    def y(self):
        return self._sprite_info.y

    @y.setter
    def y(self, value):
        self._sprite_info.y = value

    @property
    def position(self):
        return self._sprite_info.position_tuple

    @property
    def size(self):
        return self._sprite_info.size

    def get_buffered_size(self, buffer):
        return self._sprite_info.size.get_buffered_size(buffer)

    @property
    def width(self):
        return self._sprite_info.width

    @property
    def height(self):
        return self._sprite_info.height

    @property
    def hitcount(self):
        return self._sprite_info.hit.hitcount

    @property
    def max_hits(self):
        return self._sprite_info.hit.max_hits

    def add_hit(self):
        return self._sprite_info.add_hit()

    @property
    def is_dead(self):
        return self._sprite_info.is_dead()

    @property
    def speed(self):
        return self._sprite_info.speed

    @speed.setter
    def speed(self, value):
        self._sprite_info.speed = value

    def increase_speed(self, amount=1):
        """
        Increase the sprite's speed by a given amount.

        This function is in the service class because it’s about game behavior 
        (like getting faster after a power-up). The speed value is stored in 
        SpriteInfo, but changing it based on how the game works is handled here.
        """
        self.speed += amount

    def decrease_speed(self, amount=1):
        """
        Like increase speed but opposite behaviour.
        """
        self.speed = max(1, self.speed - amount)
