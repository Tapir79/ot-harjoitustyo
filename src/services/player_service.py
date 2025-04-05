from models.sprite_info import SpriteInfo
from services.base_sprite_service import BaseSpriteService
from config import LEFT_BOUNDARY, RIGHT_BOUNDARY
from models.point import Point
from models.size import Size
from services.bullet_service import BulletService


class PlayerService(BaseSpriteService):
    def __init__(self, sprite_info: SpriteInfo, speed=5, left_boundary=LEFT_BOUNDARY, right_boundary=RIGHT_BOUNDARY):
        super().__init__(sprite_info, speed)
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.shooting = False

    def shoot(self, bullet_width=5, bullet_height=10):
        """
        Create a new bullet.
        """
        player_x, player_y = self.get_position()

        bullet_x = player_x + self.sprite_info.size.width // 2 - bullet_width // 2
        bullet_y = player_y - bullet_height

        bullet_position = Point(bullet_x, bullet_y)
        bullet_size = Size(bullet_width, bullet_height)
        bullet_sprite_info = SpriteInfo(bullet_position, bullet_size)

        return BulletService(sprite_info=bullet_sprite_info, direction="up")

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

        if key == "a":
            new_x = max(self.left_boundary, x - self.speed)
        elif key == "d":
            new_x = min(self.right_boundary - width, x + self.speed)
        else:
            new_x = x

        self.sprite_info.set_x(new_x)
        return new_x
