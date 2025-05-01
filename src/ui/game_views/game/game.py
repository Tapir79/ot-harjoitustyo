import pygame
import os
from config import ASSETS_DIR, ENEMY_START_X_OFFSET, SILVER
from pygame.sprite import Group
from app_enums import AppState, GameAttributes, LevelAttributes
from db import Database
from entities.user import User
from repositories.general_statistics_repository import GeneralStatisticsRepository
from repositories.user_repository import UserRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.general_statistics_service import GeneralStatisticsService
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService
from services.player_service import PlayerService
from services.enemy_service import EnemyService
from services.level_service import LevelService
from ui.game_views.game.init import init_display, init_game_info, init_ui_images
from utils.game_helpers import get_ending_points, get_game_over_initialization_data, get_player_lives, get_random_positions_around_center_point, init_high_score, init_start_level_attributes, init_start_level_time, set_new_level_attributes
from ui.animations.player_hit_animation import PlayerHitAnimation
from ui.animations.hit_animation import HitAnimation
from ui.sprites.enemy import EnemySprite
from ui.sprites.player import PlayerSprite
from models.hit import Hit
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from config import (UPPER_BOUNDARY,
                    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED,
                    PLAYER_START_Y_OFFSET, ENEMY_WIDTH, ENEMY_HEIGHT,
                    ENEMY_START_Y_OFFSET, PLAYER_MAX_HITS, BLACK, WHITE)


class Game:
    """
    The Game class represents the main game logic for a simple Space Invaders-style game.

    It handles initialization, the main game loop, event handling, updating game state,
    and rendering the screen including the player and on-screen instructions.
    """

    def __init__(self, screen, user=None, user_service=None, user_statistics_service=None):
        """
        Initializes the game, including the display, player, clock, and font.
        Sets up the game window and player object.
        """

        self.user_service = user_service if user_service else UserService(
            UserRepository(Database()))
        self.user_statistics_service = user_statistics_service if user_statistics_service else UserStatisticsService(
            UserStatisticsRepository(Database()))
        self.general_statistics_service = GeneralStatisticsService(
            GeneralStatisticsRepository(Database()))
        self.reset_game(screen)
        self.user = self.set_user(user)

    def save_user_statistics(self):
        """
        Saves the player's score and level to the database if they are better than previous.
        """
        if not self.user_statistics_service:
            return

        user_id = self.user.user_id if self.user and self.user.user_id != 0 else 1
        points = self.player.player_service.points
        level = self.level

        self.user_statistics_service.upsert_user_statistics(
            user_id, points, level)

    def set_user(self, user):
        self.user = user if user else User(1, "guest")

    def reset_game(self, screen):
        self.screen = screen
        self.display_height, self.display_width = init_display(screen)
        # game info
        self.clock, self.font = init_game_info()
        self.gameover_data = get_game_over_initialization_data()
        self.all_time_high_score = init_high_score(
            self.general_statistics_service)

        self.heart_data = init_ui_images()
        self.init_levels()
        self.init_bullets()
        self.player = self.create_player()

    def init_levels(self):
        self.level, self.level_started = init_start_level_attributes()
        self.level_transition_timer, self.level_ticks_remaining, self.level_countdown = init_start_level_time()
        self.levels = LevelService()
        self.set_new_level_attributes()

    def set_new_level_attributes(self):
        current_level = self.levels.get_level(self.level)
        self.enemy_attributes = set_new_level_attributes(current_level)

    def create_enemies(self, spacing=60):
        """
        Create enemies on screen. 
        """
        enemy_width = ENEMY_WIDTH
        enemy_height = ENEMY_HEIGHT
        enemy_cooldown = self.enemy_attributes[GameAttributes.COOLDOWN]
        rows = self.enemy_attributes[GameAttributes.ROWS]
        cols = self.enemy_attributes[GameAttributes.COLS]
        speed = self.enemy_attributes[GameAttributes.SPEED]
        enemy_max_hits = self.enemy_attributes[GameAttributes.MAX_HITS]
        enemy_shooting_probability = self.enemy_attributes[GameAttributes.SHOOT_PROB]
        enemy_image = self.enemy_attributes[GameAttributes.IMAGE]
        margin_x = ENEMY_START_X_OFFSET
        margin_y = ENEMY_START_Y_OFFSET

        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing
                y = margin_y + row * spacing

                enemy_info = SpriteInfo(
                    Point(x, y), Size(enemy_width, enemy_height), speed, Hit(0, enemy_max_hits))
                enemy_service = EnemyService(
                    enemy_info, cooldown=enemy_cooldown)
                enemy_sprite = EnemySprite(
                    enemy_service, self.enemy_bullet_group, enemy_shooting_probability, enemy_image)
                self.enemy_group.add(enemy_sprite)

    def init_bullets(self):
        self.player_bullet_group = Group()
        self.enemy_bullet_group = Group()
        self.enemy_group = Group()
        self.hit_group = pygame.sprite.Group()

    def create_player(self):
        player_position = Point(self.display_width // 2,
                                self.display_height - PLAYER_START_Y_OFFSET)
        player_size = Size(PLAYER_WIDTH, PLAYER_HEIGHT)
        hit = Hit(0, PLAYER_MAX_HITS)
        player_info = SpriteInfo(
            player_position, player_size, PLAYER_SPEED, hit)

        player_service = PlayerService(
            sprite_info=player_info
        )

        return PlayerSprite(player_service, self.player_bullet_group)

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
                self.gameover_data[GameAttributes.RUNNING] = False

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
                    self.try_kill_enemy(enemy)

                position = enemy.rect.center
                size = enemy.enemy_service.size
                explosion = HitAnimation(position, size)
                self.hit_group.add(explosion)

    def try_kill_enemy(self, enemy):
        """
        Add a hit to an enemy. 
        Check if enemy is dead. If yes, remove enemy from
        the class enemy group. Also, increase player points.
        """
        enemy.enemy_service.add_hit()
        if enemy.enemy_service.is_dead:
            self.increase_player_points_enemy()
            enemy.remove(self.enemy_group)

    def increase_player_points_enemy(self):
        """
        Add points to player per shot enemy.
        The player gets more points per enemy from higher levels. 
        """
        self.player.player_service.add_points(self.level)

    def increase_player_points_bullet(self):
        """
        Add points to player per shot bullet.
        The player gets more points per bullet from higher levels.
        """
        self.player.player_service.add_points(self.level * 1.5)

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
                self.increase_player_points_bullet()
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
        self.draw_player_name()
        self.draw_player_points()
        self.draw_level_title()
        self.draw_player_hearts()
        self.hit_group.draw(self.screen)
        self.draw_instructions_text()
        pygame.display.update()

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

    def draw_player_name(self):
        """
        Draw current player name on screen
        """

        text = f"Player: {self.user.username}"
        position = Point(20, 20)
        self.draw_text(text, position, center=False)

    def draw_level_title(self):
        """
        Draw current level on screen
        """

        self.all_time_high_score
        text = f"Level {self.level} | High score {self.all_time_high_score}"
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

    def draw_game_over_text(self):
        """
        Draw text: GAME OVER.
        """
        text = self.gameover_text
        position = Point(self.display_width // 2, self.display_height // 2)
        self.draw_text(text, position, center=True)

    def draw_player_points(self, position=Point(20, 20), center=False):
        """
        Draw current player points on screen.
        Draw player high score on screen.
        """
        player_current_points = self.player.player_service.points
        user_statistics = None
        if self.user:
            user_statistics, _ = self.user_statistics_service.get_user_statistics(
                self.user.user_id)

        data = get_ending_points(player_current_points,
                                 user_statistics,
                                 position,
                                 all_time_high_score=self.all_time_high_score)

        self.draw_text(data["text"], data["position"],
                       center, color=data["color"])

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
                self.screen.blit(self.heart_data[GameAttributes.HEARTS],
                                 (x_offset - i * 30, y_position))
            else:
                self.screen.blit(self.heart_data[GameAttributes.BROKEN],
                                 (x_offset - i * 30, y_position))

    def run(self):
        """
        Runs the main game loop.
        Continuously handles events, updates the game state, 
        and renders the screen until the game is quit.
        """
        while self.gameover_data[GameAttributes.RUNNING]:
            self.handle_events()

            if self.is_game_over() and not self.gameover:
                self.end_game()
            elif self.gameover:
                self.save_user_statistics()
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
            # passed final levelga
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
        self.gameover_data[GameAttributes.GAMEOVER_TEXT] = "YOU WIN!"
        self.gameover_data[GameAttributes.GAMEOVER] = True

    def end_game(self):
        self.destroy_player_animation()
        self.gameover_data[GameAttributes.GAMEOVER_TEXT] = "GAME OVER"
        self.gameover_data[GameAttributes.GAMEOVER] = True

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
        points_position = Point(self.display_width//2,
                                self.display_height//2 + 40)
        self.draw_player_points(position=points_position, center=True)
        pygame.display.update()

    def is_game_over(self):
        if self.player.is_dead():
            return True
        return False
