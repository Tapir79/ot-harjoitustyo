import os
import random
import pygame
from config import ASSETS_DIR, ENEMY_SHOOTING_PROBABILITY
from ui.bullet import BulletSprite  # import the sprite class
from services.enemy_service import EnemyService


class EnemySprite(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Handles movement and rendering of the player sprite. The player can move left and right
    using the 'a' and 'd' keys. The class also manages the player's position, speed,
    dimensions, and the boundaries within which the player is allowed to move.
    """

    def __init__(self, enemy_service: EnemyService,
                 bullet_group: pygame.sprite.Group,
                 image_path: str = "enemy.png"):
        super().__init__()
        self.enemy = enemy_service
        self.bullet_group = bullet_group

        width = self.enemy.get_width()
        height = self.enemy.get_height()

        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, image_path)
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (width, height)
        )

        self.rect = self.image.get_rect()

    def shoot(self):
        bullet_service = self.enemy.try_shoot("down")

        if bullet_service:
            bullet_sprite = BulletSprite(bullet_service)
            self.bullet_group.add(bullet_sprite)

    def update(self):
        self.enemy.move()
        if random.random() < ENEMY_SHOOTING_PROBABILITY:
            self.shoot()
        x, y = self.enemy.get_position()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        self.update()
        screen.blit(self.image, self.rect)
