import os
import pygame
from services.player_service import PlayerService
from config import ASSETS_DIR


class PlayerSprite(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Handles movement and rendering of the player sprite. The player can move left and right
    using the 'a' and 'd' keys. The class also manages the player's position, speed,
    dimensions, and the boundaries within which the player is allowed to move.
    """

    def __init__(self, player_service: PlayerService):
        super().__init__()
        self.player = player_service
        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "player.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.player.width, self.player.height))

        self.rect = self.image.get_rect()

    def handle_input(self):
        """
        Handles keyboard input for the player.

        Moves the player left if 'a' is pressed, and right if 'd' is pressed.
        Movement is bounded by left and right limits of the screen.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move('a')
        if keys[pygame.K_d]:
            self.player.move('d')

    def update(self):
        x, y = self.player.get_position()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        self.update()
        screen.blit(self.image, self.rect)
