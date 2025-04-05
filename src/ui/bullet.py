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

        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "player_bullet.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, (width, height))
        
        self.rect = self.image.get_rect()

    def update(self):
        x, y = self.bullet.get_position()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        self.update()
        screen.blit(self.image, (self.x, self.y))
