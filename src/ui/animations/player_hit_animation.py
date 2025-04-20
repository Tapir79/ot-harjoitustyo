import os
from config import ASSETS_DIR
from models.size import Size
from ui.animations.animation import AnimationSprite


class PlayerHitAnimation(AnimationSprite):
    """
    An AnimationSprite that plays a sequence of player hit images as an animation.
    The animation is played when the player is destroyed. 
    The images must be named player_hit1.png, player_hit2.png, ... , player_hit9.png.
    """

    def __init__(self, position, size: Size):
        self.image_paths = [os.path.join(
            ASSETS_DIR, f"player_hit{i}.png") for i in range(1, 9)]

        super().__init__(position, size, self.image_paths, duration=300)
