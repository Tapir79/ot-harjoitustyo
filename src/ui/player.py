import os
import pygame
from services.player_service import PlayerService
from config import ASSETS_DIR

from ui.bullet import BulletSprite  # import the sprite class
from services.bullet_service import BulletService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo


class PlayerSprite(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Handles movement and rendering of the player sprite. The player can move left and right
    using the 'a' and 'd' keys. The class also manages the player's position, speed,
    dimensions, and the boundaries within which the player is allowed to move.
    """

    def __init__(self, player_service: PlayerService, bullet_group: pygame.sprite.Group):
        super().__init__()
        self.player_service = player_service
        self.bullet_group = bullet_group

        width = self.player_service.get_width()
        height = self.player_service.get_height()

        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "player.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (width, height)
        )

        self.rect = self.image.get_rect()

    def handle_input(self):
        """
        Handles keyboard input for the player.

        Moves the player left if 'a' is pressed, and right if 'd' is pressed.
        Movement is bounded by left and right limits of the screen.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_service.move('a')
        if keys[pygame.K_d]:
            self.player_service.move('d')
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        bullet_service = self.player_service.try_shoot()
        if bullet_service:
            bullet_sprite = BulletSprite(bullet_service)
            self.bullet_group.add(bullet_sprite)

    def update(self):
        x, y = self.player_service.get_position()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        self.update()
        screen.blit(self.image, self.rect)

    def is_dead(self):
        return self.player_service.is_dead()
