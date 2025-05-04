

from models.hit import Hit
from models.sprite_info import SpriteInfo


def create_sprite_info(point, size, speed, max_hits):
    """
    Create SpriteInfo with 0 hitcount.

    Args:
        point: (x,y)
        size: (width, height)
        speed: sprite speed
        max_hits: maximum amount of hits the sprite can take.

    Returns:
        SpriteInfo object with full health.
    """
    return SpriteInfo(point, size, speed, Hit(0, max_hits))
