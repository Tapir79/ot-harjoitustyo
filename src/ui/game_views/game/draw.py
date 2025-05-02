import os
import pygame
from app_enums import GameAttributes
from config import ASSETS_DIR, BLACK, PLAYER_SPEED, UPPER_BOUNDARY, WHITE, SILVER
from models.point import Point
from models.size import Size
from ui.animations.animation import AnimationSprite
from utils.game_helpers import (get_ending_points,
                                get_player_lives,
                                get_random_positions_around_center_point)


class GameDrawer():
    """
    A separate class for drawing the game objects. 
    """

    def __init__(self, game):
        """
        Args:
            game: Game instance, which must have at least:
                  - screen, font, heart_data, game_groups, player, user
        """
        self.game = game
        self.screen = game.screen
        self.display_width = game.screen.get_width()
        self.display_height = game.screen.get_height()
        self.font = game.font

    def draw(self):
        """
        Renders the game screen.
        Clears the screen.
        Draws the player, enemies, bullets, hit animations and instruction text
        Updates the display.
        """
        self.screen.fill(BLACK)
        self.game.player.draw(self.screen)
        self.game.game_groups[GameAttributes.PLAYER_BULLETS].draw(self.screen)
        self.game.game_groups[GameAttributes.ENEMY_BULLETS].draw(self.screen)
        self.game.game_groups[GameAttributes.ENEMIES].draw(self.screen)
        self.draw_player_name()
        self.draw_player_points()
        self.draw_level_title()
        self.draw_player_hearts()
        self.game.game_groups[GameAttributes.HITS].draw(self.screen)
        self.draw_instructions_text()
        pygame.display.update()

    def draw_player_name(self):
        """
        Draw current player name on screen
        """
        text = f"Player: {self.game.user.username}"
        self.draw_text(text, Point(20, 20), center=False)

    def draw_level_title(self):
        """
        Draw current level on screen
        """

        self.game.all_time_high_score
        text = f"Level {self.game.start_level_data[GameAttributes.LEVEL]} | High score {self.game.all_time_high_score}"
        position = Point((self.display_width // 2 - (len(text) // 2)), 20)
        self.draw_text(text, position, center=True, color=SILVER)

    def draw_instructions_text(self):
        """
        Instructions for the player.
        """
        text = "Move the player with 'a' and 'd', Shoot with SPACE"
        y_offset = 40
        position = Point(self.display_width // 2,
                         self.display_height - y_offset)
        self.draw_text(text, position, center=True)

    def draw_player_hearts(self):
        """
        Draw current player hearts and broken hearts on screen.
        """
        hearts, broken_hearts = get_player_lives(
            self.game.player.player_service)
        x_offset = self.display_width - 30
        y_position = 20

        total_hearts = []
        for h in range(0, hearts):
            total_hearts.append(1)

        for h in range(0, broken_hearts):
            total_hearts.append(0)

        for i, h in enumerate(total_hearts):
            if h == 1:
                self.screen.blit(self.game.heart_data[GameAttributes.HEARTS],
                                 (x_offset - i * 30, y_position))
            else:
                self.screen.blit(self.game.heart_data[GameAttributes.BROKEN],
                                 (x_offset - i * 30, y_position))

    def draw_game_over_text(self):
        """
        Draw text: GAME OVER.
        """
        text = self.game.gameover_data[GameAttributes.GAMEOVER_TEXT]
        position = Point(self.display_width // 2, self.display_height // 2)
        self.draw_text(text, position, center=True)

    def draw_player_points(self, position=Point(20, 20), center=False):
        """
        Draw current player points on screen.
        Draw player high score on screen.
        """
        player_current_points = self.game.player.player_service.points
        user_statistics = None
        if self.game.user:
            user_statistics, _ = self.game.user_statistics_service.get_user_statistics(
                self.game.user.user_id)

        data = get_ending_points(player_current_points,
                                 user_statistics,
                                 position,
                                 all_time_high_score=self.game.all_time_high_score)

        self.draw_text(data["text"], data["position"],
                       center, color=data["color"])

    def draw_next_level_title(self):
        """
        Draws "Level <level_number>".
        """
        text = self.font.render(
            f"Level {self.game.start_level_data[GameAttributes.LEVEL]}", True, WHITE)
        self.screen.blit(
            text, text.get_rect(center=(self.display_width // 2, self.display_height // 2)))

    def play_animation_once(self, animation_sprite):
        """
        Plays a given animation sprite for a fixed duration (default 1000ms = 1 second).
        """
        clock = pygame.time.Clock()
        group = pygame.sprite.Group(animation_sprite)

        images = animation_sprite.image_count

        for _ in range(0, images):
            self.game.handle_events()  # So the window doesn't freeze
            group.update()
            self.screen.fill(BLACK)
            group.draw(self.screen)
            pygame.display.update()
            clock.tick(60)

    def destroy_player_animation(self):
        """
        Draws an animation sprite of the player destruction.
        """
        position = self.game.player.rect.center
        center_x, center_y = position
        positions = get_random_positions_around_center_point(
            Point(center_x, center_y), Size(self.display_width, self.display_height))
        size = self.game.player.player_service.size
        player_size = self.game.player.player_service.get_buffered_size(20)
        explosion = self.get_player_hit_animation(position, player_size)
        self.play_animation_once(explosion)

        for pos in positions:
            explosion = self.get_hit_animation(pos, size)
            self.play_animation_once(explosion)
            self.wait(5)

    def get_player_hit_animation(self, position, player_size):
        self.image_paths = [os.path.join(
            ASSETS_DIR, f"player_hit{i}.png") for i in range(1, 9)]
        return AnimationSprite(position, player_size, self.image_paths, duration=300)

    def get_hit_animation(self, position, size):
        self.image_paths = [os.path.join(
            ASSETS_DIR, f"hit{i}.png") for i in range(1, 5)]
        return AnimationSprite(position, size, self.image_paths, duration=200)

    def wait(self, n):
        """
        Pause the game for n * 60 seconds.
        """
        for i in range(0, n):
            self.game.clock.tick(60)

    def fly_player_over_bounds_animation(self):
        """
        Plays an animation of the player winning. 
        """
        clock = pygame.time.Clock()
        current_y = self.game.player.player_service.y

        while current_y > UPPER_BOUNDARY:
            self.game.handle_events()
            current_y = self.game.player.player_service.y
            self.game.player.player_service.y = current_y - PLAYER_SPEED

            self.screen.fill(BLACK)
            self.game.player.update()
            self.game.player.draw(self.screen)
            pygame.display.update()
            clock.tick(60)

    def draw_text(self, text, position: Point, center=False, color=WHITE):
        """
        General method for drawing text on the screen.
        """
        text_surface = self.font.render(text, True, color)
        rect = text_surface.get_rect()
        if center:
            rect.center = position.x, position.y
        else:
            rect.topleft = position.x, position.y
        self.screen.blit(text_surface, rect)
