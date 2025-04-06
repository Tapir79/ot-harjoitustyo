import os
import pygame
from config import ASSETS_DIR
from ui.bullet import BulletSprite  # import the sprite class
from services.bullet_service import BulletService
from services.enemy_service import EnemyService
from services.player_service import PlayerService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo


class EnemySprite(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Handles movement and rendering of the player sprite. The player can move left and right
    using the 'a' and 'd' keys. The class also manages the player's position, speed,
    dimensions, and the boundaries within which the player is allowed to move.
    """

    def __init__(self, enemy_service: EnemyService, bullet_group: pygame.sprite.Group):
        super().__init__()
        self.enemy = enemy_service
        self.bullet_group = bullet_group

        width = self.enemy.sprite_info.size.get_width()
        height = self.enemy.sprite_info.size.get_height()

        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "enemy.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (width, height)
        )

        self.rect = self.image.get_rect()

    def shoot(self):
        bullet_service = self.enemy.shoot()
        bullet_sprite = BulletSprite(bullet_service)

        self.bullet_group.add(bullet_sprite)

    def update(self):
        self.enemy.move()
        x, y = self.enemy.get_position()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        self.update()
        screen.blit(self.image, self.rect)
