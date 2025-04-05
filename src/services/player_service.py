from models.sprite_info import SpriteInfo
from services.base_sprite_service import BaseSpriteService


class PlayerService(BaseSpriteService):
    def __init__(self, sprite_info: SpriteInfo, speed=5, left_boundary=0, right_boundary=800):
        super().__init__(sprite_info, speed)
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary

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
        x = self.sprite_info.get_x()
        width = self.sprite_info.get_width()

        if key == 'a':
            new_x = max(self.left_boundary, x - self.speed)
        elif key == 'd':
            new_x = min(self.right_boundary - width, x + self.speed)
        else:
            new_x = x

        self.sprite_info.set_x(new_x)
        return new_x

