import pygame
from pygame.sprite import Group
import os
from app_enums import GameAttributes
from config import (ASSETS_DIR,
                    PLAYER_HEIGHT,
                    PLAYER_START_Y_OFFSET,
                    PLAYER_WIDTH)
from models.hit import Hit
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from services.player_service import PlayerService
from ui.sprites.player import PlayerSprite


def init_display(screen):
    """
    Initialize game screen or display.
    """
    height = screen.get_height()
    width = screen.get_width()
    return height, width


def init_game_info():
    """
    Initialize pygame information
    """
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


def init_game_groups():
    """
    Initialize all pygame groups. 
    """
    return {
        GameAttributes.PLAYER_BULLETS: Group(),
        GameAttributes.ENEMY_BULLETS: Group(),
        GameAttributes.ENEMIES: Group(),
        GameAttributes.HITS: Group()
    }


def create_player(display_width, display_height, game_groups):
    """
    Create new player with constant values.
    """
    player_position = Point(display_width // 2,
                            display_height - PLAYER_START_Y_OFFSET)
    player_size = Size(PLAYER_WIDTH, PLAYER_HEIGHT)
    player_service = PlayerService.create(player_position,
                                          player_size)

    return PlayerSprite(player_service, game_groups[GameAttributes.PLAYER_BULLETS])
