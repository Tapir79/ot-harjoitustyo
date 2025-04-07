import pygame
import os
from config import ASSETS_DIR

from services.bullet_service import BulletService

dirname = os.path.dirname(__file__)


class BulletSprite (pygame.sprite.Sprite):
    def __init__(self, bullet_service: BulletService):
        super().__init__()
        self.bullet = bullet_service

        width = self.bullet.sprite_info.size.get_width()
        height = self.bullet.sprite_info.size.get_height()

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
        self.bullet.update()
        x, y = self.bullet.get_position()
        self.rect.x = x
        self.rect.y = y

        if self.bullet.is_moving() == False:
            self.kill()

    def draw(self, screen):
        self.update()
        screen.blit(self.image, (self.x, self.y))
