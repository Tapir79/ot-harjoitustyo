import os
import random
import pygame
from config import ASSETS_DIR
from level_config import ENEMY_SHOOTING_PROBABILITY
from ui.sprites.bullet import BulletSprite
from services.enemy_service import EnemyService


class EnemySprite(pygame.sprite.Sprite):
    """
    Represents the enemy sprite in the game.
    Updates movement, shooting and rendering of the enemy sprite. 
    The class uses the logic from a EnemyService 
    """

    def __init__(self, enemy_service: EnemyService,
                 bullet_group: pygame.sprite.Group,
                 shooting_probability: int,
                 image_path: str = "enemy.png"):
        """
        Initialize the enemy sprite, load its image,
        and set its size and starting position.

        Args:
            enemy_service: The EnemyService object controlling enemy logic.
            bullet_group: The group where bullets are added.
            image_path: Path to the enemy image file.
        """
        super().__init__()
        self.enemy_service = enemy_service
        self.bullet_group = bullet_group
        self.shooting_probability = shooting_probability
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
        bullet_service = self.enemy_service.try_shoot()

        if bullet_service:
            bullet_sprite = BulletSprite(bullet_service)
            self.bullet_group.add(bullet_sprite)

    def update(self):
        """
        Updates the emey's position. Randomly shoots a new bullet. 
        """
        self.enemy_service.move()
        shooting_probability = self.shooting_probability if self.shooting_probability else ENEMY_SHOOTING_PROBABILITY
        if random.random() < shooting_probability:
            self.shoot()
        x, y = self.enemy_service.position
        self.rect.x = x
        self.rect.y = y

    def is_dead(self):
        """
        Returns:
            bool: Whether the enemy has surpassed the maximum hitcount.
        """
        return self.enemy_service.is_dead
