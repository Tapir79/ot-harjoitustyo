import pygame
import os
from config import ASSETS_DIR
from pygame.sprite import Group
from app_enums import AppState
from utils.game_helpers import get_player_lives, get_random_positions_around_center_point
from ui.animations.player_hit_animation import PlayerHitAnimation
from ui.animations.hit_animation import HitAnimation
from ui.sprites.enemy import EnemySprite
from ui.sprites.player import PlayerSprite
from services.player_service import PlayerService
from services.enemy_service import EnemyService
from services.level_service import LevelService
from models.hit import Hit
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from config import (UPPER_BOUNDARY,
                    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED,
                    ENEMY_WIDTH, ENEMY_HEIGHT, PLAYER_MAX_HITS, BLACK, WHITE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Game:
    """
    The Game class represents the main game logic for a simple Space Invaders-style game.

    It handles initialization, the main game loop, event handling, updating game state,
    and rendering the screen including the player and on-screen instructions.
    """

    def __init__(self, screen, user=None):
        """
        Initializes the game, including the display, player, clock, and font.
        Sets up the game window and player object.
        """

        self.reset_game(screen)
        self.user = self.set_user(user)

    def set_user(self, user):
        self.user = user if user else ""

    def reset_game(self, screen):
        self.screen = screen
        self.display_height = screen.get_height()
        self.display_width = screen.get_width()
        # game info
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 30)
        self.gameover = False
        self.gameover_text = ""

        self.init_ui_images()
        self.init_levels()
        self.init_bullets()
        self.player = self.create_player()

    def init_ui_images(self):
        self.heart_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "heart.png")).convert_alpha()
        self.broken_heart_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "broken_heart.png")).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (25, 25))
        self.broken_heart_image = pygame.transform.scale(
            self.broken_heart_image, (25, 25))

    def init_levels(self):
        self.level = 1
        self.level_started = False
        self.level_transition_timer = 0
        self.level_ticks_remaining = 180
        self.level_countdown = 3
        self.levels = LevelService()
        self.set_new_level_attributes()

    def init_bullets(self):
        self.player_bullet_group = Group()
        self.enemy_bullet_group = Group()
        self.enemy_group = Group()
        self.hit_group = pygame.sprite.Group()

    def create_player(self):
        player_position = Point(self.display_width // 2,
                                self.display_height - 50)
        player_size = Size(PLAYER_WIDTH, PLAYER_HEIGHT)
        hit = Hit(0, PLAYER_MAX_HITS)
        player_info = SpriteInfo(
            player_position, player_size, PLAYER_SPEED, hit)

        player_service = PlayerService(
            sprite_info=player_info
        )

        return PlayerSprite(player_service, self.player_bullet_group)

    def create_enemies(self, spacing=60):
        """
        Create enemies on screen. 
        """
        enemy_width = ENEMY_WIDTH
        enemy_height = ENEMY_HEIGHT
        rows = self.enemy_rows
        cols = self.enemy_count_cols
        speed = self.enemy_speed
        enemy_max_hits = self.enemy_max_hits
        enemy_image = self.enemy_image
        margin_x = 50
        margin_y = 50

        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing
                y = margin_y + row * spacing

                enemy_info = SpriteInfo(
                    Point(x, y), Size(enemy_width, enemy_height), speed, Hit(0, enemy_max_hits))
                enemy_service = EnemyService(
                    enemy_info)
                enemy_sprite = EnemySprite(
                    enemy_service, self.enemy_bullet_group, enemy_image)
                self.enemy_group.add(enemy_sprite)

    def set_new_level_attributes(self):
        current_level = self.levels.get_level(self.level)
        self.cooldown = current_level["enemy_cooldown"]
        self.enemy_shooting_probability = current_level["enemy_shoot_prob"]
        self.enemy_count_cols = current_level["enemy_cols"]
        self.enemy_rows = current_level["enemy_rows"]
        self.enemy_speed = current_level["enemy_speed"]
        self.enemy_bullet_speed = current_level["enemy_bullet_speed"]
        self.enemy_max_hits = current_level["enemy_max_hits"]
        self.enemy_image = current_level["enemy_image"]

    def new_level_reset(self):
        self.player_bullet_group.empty()
        self.enemy_bullet_group.empty()
        self.enemy_group.empty()
        self.hit_group.empty()
        self.level_transition_timer = 0
        self.level_countdown = 3
        self.level_ticks_remaining = 180
        self.set_new_level_attributes()

    def handle_events(self):
        """
        Handles user input events such as closing the game window.
        If the user clicks the close button, the game loop will stop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def check_sprite_collisions(self):
        self.check_enemy_and_player_bullet_collisions()
        self.check_enemy_bullet_and_player_bullet_collisions()
        self.check_player_and_enemy_bullet_collisions()
        self.check_player_and_enemies_collisions()

    def check_player_and_enemies_collisions(self):
        hits = pygame.sprite.spritecollide(
            self.player, self.enemy_group, dokill=True)

        if hits:
            self.player.player_service.add_hit()

            position = self.player.rect.center
            size = self.player.player_service.size
            explosion = HitAnimation(position, size)
            self.hit_group.add(explosion)

            if self.player.player_service.is_dead:
                self.player.kill()

    def check_player_and_enemy_bullet_collisions(self):
        """
        Handle player collisions with enemy bullets.
        """
        collisions = pygame.sprite.spritecollide(
            self.player, self.enemy_bullet_group, dokill=True)

        if collisions:
            self.player.player_service.add_hit()

            position = self.player.rect.center
            size = self.player.player_service.size
            explosion = HitAnimation(position, size)
            self.hit_group.add(explosion)

            if self.player.player_service.is_dead:
                self.player.kill()

    def check_enemy_and_player_bullet_collisions(self):
        """
        Handle enemy collisions with player bullets. 
        First get all player bullets. 
        Then check collisions with each enemy.
        Using pygame group collisions. 
        """
        collisions = pygame.sprite.groupcollide(
            self.enemy_group,
            self.player_bullet_group,
            False,  # remove enemy
            True   # remove bullet
        )

        if collisions:
            for enemy, bullets in collisions.items():
                for _ in bullets:
                    enemy.enemy_service.add_hit()
                    if enemy.enemy_service.is_dead:
                        self.increase_player_points()
                        enemy.remove(self.enemy_group)

                position = enemy.rect.center
                size = enemy.enemy_service.size
                explosion = HitAnimation(position, size)
                self.hit_group.add(explosion)

    def increase_player_points(self):
        """
        Add points to player per shot enemy.
        The player gets more points per enemy from higher levels. 
        """
        self.player.player_service.add_points(self.level)

    def check_enemy_bullet_and_player_bullet_collisions(self):
        """
        Handle enemy bullet collisions with player bullets.
        """
        collisions = pygame.sprite.groupcollide(
            self.enemy_bullet_group,
            self.player_bullet_group,
            True,  # remove enemy bullet
            True   # remove player bullet
        )

        if collisions:
            for enemy_bullet, player_bullet in collisions.items():
                position = enemy_bullet.rect.center
                buffered_size = enemy_bullet.bullet.get_buffered_size(
                    10)
                explosion = HitAnimation(position, buffered_size)
                self.hit_group.add(explosion)

    def update(self):
        """
        Updates the game state. 
        """
        self.player.handle_input()
        self.player_bullet_group.update()
        self.enemy_bullet_group.update()
        self.enemy_group.update()
        self.hit_group.update()

    def draw(self):
        """
        Renders the game screen.
        Clears the screen.
        Draws the player, enemies, bullets, hit animations and instruction text
        Updates the display.
        """
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        self.player_bullet_group.draw(self.screen)
        self.enemy_bullet_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.draw_player_points()
        self.draw_level_title()
        self.draw_player_hearts()
        self.hit_group.draw(self.screen)
        pygame.display.update()

    def draw_text(self, text, position, center=False):
        """
        General method for drawing text on the screen.
        """
        text_surface = self.font.render(text, True, WHITE)
        rect = text_surface.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(text_surface, rect)

    def draw_level_title(self):
        """
        Draw current level on screen
        """
        text = f"Level {self.level}"
        position = ((self.display_width // 2 - len(text) // 2), 20)
        self.draw_text(text, position)

    def draw_instructions_text(self):
        """
        Instructions for the player.
        """
        text = "Move the player with 'a' and 'd', Shoot with SPACE"
        y_offset = 40
        position = (self.display_width // 2,
                    self.display_height // 2 + y_offset)
        self.draw_text(text, position, center=True)

    def draw_game_over_text(self):
        text = self.gameover_text
        position = (self.display_width // 2, self.display_height // 2)
        self.draw_text(text, position, center=True)

    def draw_player_points(self, position=(20, 20), center=False):
        """
        Draw current player points on screen.
        """
        points = self.player.player_service.points
        text = f"{self.user} points: {points}"
        position = position
        self.draw_text(text, position, center)

    def draw_player_hearts(self):
        """
        Draw current player hearts and broken hearts on screen.
        """
        hearts, broken_hearts = get_player_lives(self.player.player_service)
        x_offset = self.display_width - 30
        y_position = 20

        total_hearts = []
        for h in range(0, hearts):
            total_hearts.append(1)

        for h in range(0, broken_hearts):
            total_hearts.append(0)

        for i, h in enumerate(total_hearts):
            if h == 1:
                self.screen.blit(self.heart_image,
                                 (x_offset - i * 30, y_position))
            else:
                self.screen.blit(self.broken_heart_image,
                                 (x_offset - i * 30, y_position))

    def run(self):
        """
        Runs the main game loop.
        Continuously handles events, updates the game state, 
        and renders the screen until the game is quit.
        """
        while self.running:
            self.handle_events()

            if self.is_game_over() and not self.gameover:
                self.end_game()
            elif self.gameover:
                self.game_over()
                self.reset_game(self.screen)
                pygame.time.wait(2000)
                return AppState.START_SCREEN
            elif not self.level_started:
                self.start_new_level()
            else:
                self.update()
                self.check_sprite_collisions()
                self.move_to_next_level()
                self.draw()
                self.clock.tick(60)

        return AppState.QUIT

    def move_to_next_level(self):
        """
        Check if all enemies in the level are dead. 
        If the level was the last, player won the game.
        Else move to the next level.
        """
        if not self.enemy_group:
            self.level += 1
            # passed final level
            if self.level > self.levels.get_final_level():
                self.win_game()
            # load next level
            else:
                self.new_level_reset()
                self.level_started = False

    def start_new_level(self):
        """
        When level changes, this is drawn before the new level starts.
        It resets level timer, clears the screen and shows the next level.
        """

        if self.level_transition_timer == 0:
            self.level_transition_timer = 1
            self.level_ticks_remaining = 60  # show for 1 second at 60 FPS

        self.screen.fill(BLACK)

        if self.level_ticks_remaining > 0:
            self.draw_next_level_title()
            self.draw_instructions_text()
            pygame.display.update()

            self.level_ticks_remaining -= 1
            self.clock.tick(60)
        else:
            self.level_started = True
            self.level_transition_timer = 0
            self.create_enemies()

    def draw_next_level_title(self):
        text = self.font.render(
            f"Level {self.level}", True, WHITE)
        self.screen.blit(
            text, text.get_rect(center=(self.display_width // 2, self.display_height // 2)))

    def win_game(self):
        self.fly_player_over_bounds_animation()
        self.gameover_text = "YOU WIN!"
        self.gameover = True

    def end_game(self):
        self.destroy_player_animation()
        self.gameover_text = "GAME OVER"
        self.gameover = True

    def wait(self, n):
        for i in range(0, n):
            self.clock.tick(60)

    def play_animation_once(self, animation_sprite):
        """
        Plays a given animation sprite for a fixed duration (default 1000ms = 1 second).
        """
        clock = pygame.time.Clock()
        group = pygame.sprite.Group(animation_sprite)

        images = animation_sprite.image_paths

        for image in images:
            self.handle_events()  # So the window doesn't freeze
            group.update()
            self.screen.fill(BLACK)
            group.draw(self.screen)
            pygame.display.update()
            clock.tick(60)

    def destroy_player_animation(self):
        position = self.player.rect.center
        center_x, center_y = position
        positions = get_random_positions_around_center_point(
            Point(center_x, center_y), Size(self.display_width, self.display_height))
        size = self.player.player_service.size
        player_size = self.player.player_service.get_buffered_size(20)
        explosion = PlayerHitAnimation(position, player_size)
        self.play_animation_once(explosion)

        for pos in positions:
            explosion = HitAnimation(pos, size)
            self.play_animation_once(explosion)
            self.wait(5)

    def fly_player_over_bounds_animation(self):
        clock = pygame.time.Clock()
        current_y = self.player.player_service.y

        while current_y > UPPER_BOUNDARY:
            self.handle_events()
            current_y = self.player.player_service.y
            self.player.player_service.y = current_y - PLAYER_SPEED

            self.screen.fill(BLACK)
            self.player.update()
            self.player.draw(self.screen)
            pygame.display.update()
            clock.tick(60)

    def game_over(self):
        self.screen.fill(BLACK)
        self.draw_game_over_text()

        points_position = self.display_width//2, self.display_height//2 + 40
        self.draw_player_points(position=points_position, center=True)
        pygame.display.update()

    def is_game_over(self):
        if self.player.is_dead():
            return True
        return False
