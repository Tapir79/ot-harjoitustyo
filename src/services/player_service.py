from services.shooting_sprite_service import ShootingSpriteService
from models.sprite_info import SpriteInfo
from config import PLAYER_COOLDOWN


class PlayerService(ShootingSpriteService):
    def __init__(self, sprite_info: SpriteInfo,
                 cooldown=PLAYER_COOLDOWN):
        super().__init__(sprite_info, cooldown=cooldown)

    def move(self, key):
        """
        Move the player left or right within the screen boundaries.

        Args:
            x (int): Current x-coordinate of the player.
            key (str): Key pressed by the user ('a' for left, 'd' for right).
            speed (int, optional): Movement speed in pixels. Defaults to 5.
            left_boundary (int, optional): Minimum x-coordinate the player can reach. 
            Defaults to 0.
            right_boundary (int, optional): Maximum x-coordinate the player can reach. 
            Defaults to 800.
            player_width (int, optional): Width of the player sprite. 
            Used to prevent moving out of bounds.

        Returns:
            int: The updated x-coordinate after movement.
        """
        x = self.get_x()
        width = self.get_width()

        if key == "a":
            new_x = max(self.left_boundary, x - self.get_speed())
        elif key == "d":
            new_x = min(self.right_boundary - width,
                        x + self.get_speed())
        else:
            new_x = x

        self.set_x(new_x)
        return new_x
