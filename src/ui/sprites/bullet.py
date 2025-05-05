import pygame
import os
from config import ASSETS_DIR
from services.bullet_service import BulletService

dirname = os.path.dirname(__file__)


class BulletSprite (pygame.sprite.Sprite):
    """
    User Interface pygame bullet sprite in the game.

    This class uses the logic from a BulletService and then
    updates the sprite image and location on the screen.
    """

    def __init__(self, bullet_service: BulletService):
        """
        Initialize the bullet sprite, load its image based on direction,
        and set its size and starting position.

        Args:
            bullet_service: The logic class controlling bullet behavior.
        """
        super().__init__()
        self.bullet = bullet_service

        width = self.bullet.width
        height = self.bullet.height

        if self.bullet.direction == "up":
            image_name = "player_bullet.png"
        else:
            image_name = "enemy_bullet.png"

        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, image_name)
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, (width, height))

        self.rect = self.image.get_rect()

    def update(self):
        """
        Updates the bullet's position and checks if it should be removed from the screen.
        """
        self.bullet.update()
        x, y = self.bullet.position
        self.rect.x = x
        self.rect.y = y

        if self.bullet.is_moving() == False:
            self.kill()
