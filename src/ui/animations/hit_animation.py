import os
from config import ASSETS_DIR
from models.size import Size
from ui.animations.animation import AnimationSprite


class HitAnimation(AnimationSprite):
    """
    A AnimationSprite that plays a sequence of hit images as an animation. 
    The images must be named hit1.png, hit2.png, ... , hit5.png.
    """

    def __init__(self, position, size: Size):
        self.image_paths = [os.path.join(
            ASSETS_DIR, f"hit{i}.png") for i in range(1, 5)]

        super().__init__(position, size, self.image_paths, duration=200)
