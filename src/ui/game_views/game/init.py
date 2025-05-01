import pygame
import os
from app_enums import GameAttributes
from config import ASSETS_DIR


def init_display(screen):
    height = screen.get_height()
    width = screen.get_width()
    return height, width


def init_game_info():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    return clock, font


def init_ui_images():
    """
    Load and scale the heart and broken-heart images.
    Returns a tuple (heart_image, broken_heart_image).
    """
    heart = pygame.image.load(
        os.path.join(ASSETS_DIR, "heart.png")
    ).convert_alpha()
    broken = pygame.image.load(
        os.path.join(ASSETS_DIR, "broken_heart.png")
    ).convert_alpha()

    heart = pygame.transform.scale(heart, (25, 25))
    broken = pygame.transform.scale(broken, (25, 25))

    return {GameAttributes.HEARTS: heart, GameAttributes.BROKEN: broken}
