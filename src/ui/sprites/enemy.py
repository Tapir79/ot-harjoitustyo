import os
import random
import pygame
from config import ASSETS_DIR, ENEMY_SHOOTING_PROBABILITY
from ui.sprites.bullet import BulletSprite  # import the sprite class
from services.enemy_service import EnemyService


class EnemySprite(pygame.sprite.Sprite):
    """
    Represents the enemy sprite in the game.
    Updates movement, shooting and rendering of the enemy sprite. 
    The class uses the logic from a EnemyService 
    """

    def __init__(self, enemy_service: EnemyService,
                 bullet_group: pygame.sprite.Group,
                 image_path: str = "enemy.png"):
        """
        Initialize the enemy sprite, load its image,
        and set its size and starting position.
        """
        super().__init__()
        self.enemy_service = enemy_service
        self.bullet_group = bullet_group

        width = self.enemy_service.width
        height = self.enemy_service.height

        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, image_path)
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (width, height)
        )

        self.rect = self.image.get_rect()

    def shoot(self):
        """
        Tries to shoot. If shooting is a success a new bullet is created. 
        The bullet is added to enemy bullet group.
        """
        bullet_service = self.enemy_service.try_shoot("down")

        if bullet_service:
            bullet_sprite = BulletSprite(bullet_service)
            self.bullet_group.add(bullet_sprite)

    def update(self):
        """
        Updates the emey's position. Randomly shoots a new bullet. 
        """
        self.enemy_service.move()
        if random.random() < ENEMY_SHOOTING_PROBABILITY:
            self.shoot()
        x, y = self.enemy_service.position
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        """
        Draws the enemy on the screen at its current position.

        Args:
            screen (Surface): The game screen surface to draw the enemy on.
        """
        self.update()
        screen.blit(self.image, self.rect)
