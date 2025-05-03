

from models.hit import Hit
from models.sprite_info import SpriteInfo


def create_sprite_info(point, size, speed, max_hits):
    return SpriteInfo(point, size, speed, Hit(0, max_hits))
