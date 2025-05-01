import pygame
from app_enums import AppState, GameAttributes
from config import (BULLET_POINTS_COEFFICIENT, UPPER_BOUNDARY, PLAYER_SPEED,
                    ENEMY_WIDTH, ENEMY_HEIGHT,
                    ENEMY_START_Y_OFFSET, BLACK,
                    ENEMY_START_X_OFFSET)
from db import Database
from entities.user import User
from models.point import Point
from models.size import Size
from repositories.general_statistics_repository import GeneralStatisticsRepository
from repositories.user_repository import UserRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.general_statistics_service import GeneralStatisticsService
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService
from services.level_service import LevelService
from ui.game_views.draw import GameDrawer
from ui.game_views.game.init import (create_player,
                                     init_display,
                                     init_game_groups,
                                     init_game_info,
                                     init_ui_images)
from utils.game_helpers import (create_enemy_service,
                                get_game_over_initialization_data,
                                get_random_positions_around_center_point,
                                init_high_score,
                                init_start_level_attributes,
                                set_new_level_attributes)
from ui.animations.player_hit_animation import PlayerHitAnimation
from ui.animations.hit_animation import HitAnimation
from ui.sprites.enemy import EnemySprite


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
        self.user = self.set_user(user)
        self.reset_game(screen)
        self.drawer = GameDrawer(self)

    def set_user(self, user):
        """
        Set game user to be logged in user or guest.
        """
        self.user = user if user else User(1, "guest")

    def reset_game(self, screen):
        """
        Reset game attributes when it starts over.
        """
        self.screen = screen
        self.display_height, self.display_width = init_display(screen)
        self.clock, self.font = init_game_info()
        self.gameover_data = get_game_over_initialization_data()
        self.all_time_high_score = init_high_score(
            self.general_statistics_service)

        self.heart_data = init_ui_images()
        self.init_levels()
        self.game_groups = init_game_groups()
        self.player = create_player(self.display_width,
                                    self.display_height,
                                    self.game_groups)

    def init_levels(self):
        """
        Initialize game levels
        """
        self.start_level_data = init_start_level_attributes()
        self.levels = LevelService()
        self.set_level_attributes()

    def set_level_attributes(self):
        """
        Set attributes for current level. Gets level information from
        level service.
        """
        level = self.start_level_data[GameAttributes.LEVEL]
        current_level = self.levels.get_level(level)
        self.enemy_attributes = set_new_level_attributes(current_level)

    def create_enemies(self, spacing=60):
        """
        Create enemies on screen. 

        Args: 
            spacing: spacing between each enemy
        """
        rows = self.enemy_attributes[GameAttributes.ROWS]
        cols = self.enemy_attributes[GameAttributes.COLS]
        enemy_shooting_probability = self.enemy_attributes[GameAttributes.SHOOT_PROB]
        enemy_image = self.enemy_attributes[GameAttributes.IMAGE]
        margin_x = ENEMY_START_X_OFFSET
        margin_y = ENEMY_START_Y_OFFSET

        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing
                y = margin_y + row * spacing

                enemy_sprite = EnemySprite(
                    self.get_enemy_service(x, y),
                    self.game_groups[GameAttributes.ENEMY_BULLETS],
                    enemy_shooting_probability, enemy_image)
                self.game_groups[GameAttributes.ENEMIES].add(enemy_sprite)

    def get_enemy_service(self, x, y):
        """
        Create a new enemy service for each enemy.

        Args: 
            x: enemy x coordinate
            y: enemy y coordinate

        Returns:
            enemy_service
        """
        enemy_width = ENEMY_WIDTH
        enemy_height = ENEMY_HEIGHT
        speed = self.enemy_attributes[GameAttributes.SPEED]
        enemy_max_hits = self.enemy_attributes[GameAttributes.MAX_HITS]
        enemy_cooldown = self.enemy_attributes[GameAttributes.COOLDOWN]

        return create_enemy_service(Point(x, y),
                                    Size(enemy_width,
                                    enemy_height),
                                    speed,
                                    enemy_max_hits,
                                    enemy_cooldown)

    def new_level_reset(self):
        """
        Reset level attributes before it begins.
        """
        self.game_groups[GameAttributes.PLAYER_BULLETS].empty()
        self.game_groups[GameAttributes.ENEMY_BULLETS].empty()
        self.game_groups[GameAttributes.ENEMIES].empty()
        self.game_groups[GameAttributes.HITS].empty()
        self.start_level_data[GameAttributes.TRANSITION_TIMER] = 0
        self.start_level_data[GameAttributes.LEVEL_COUNTDOWN] = 3
        self.start_level_data[GameAttributes.TICKS_REMAINING] = 180
        self.set_level_attributes()

    def handle_events(self):
        """
        Handles user input events such as closing the game window.
        If the user clicks the close button, the game loop will stop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameover_data[GameAttributes.RUNNING] = False

    def check_sprite_collisions(self):
        """
        Check all collisions per game loop.
        """
        self.check_enemy_and_player_bullet_collisions()
        self.check_enemy_bullet_and_player_bullet_collisions()
        self.check_player_and_enemy_bullet_collisions()
        self.check_player_and_enemies_collisions()

    def check_player_and_enemies_collisions(self):
        hits = pygame.sprite.spritecollide(
            self.player, self.game_groups[GameAttributes.ENEMIES], dokill=True)

        if hits:
            self.player.player_service.add_hit()

            position = self.player.rect.center
            size = self.player.player_service.size
            explosion = HitAnimation(position, size)
            self.game_groups[GameAttributes.HITS].add(explosion)

            if self.player.player_service.is_dead:
                self.player.kill()

    def check_player_and_enemy_bullet_collisions(self):
        """
        Handle player collisions with enemy bullets.
        """
        collisions = pygame.sprite.spritecollide(
            self.player, self.game_groups[GameAttributes.ENEMY_BULLETS], dokill=True)

        if collisions:
            self.player.player_service.add_hit()

            position = self.player.rect.center
            size = self.player.player_service.size
            explosion = HitAnimation(position, size)
            self.game_groups[GameAttributes.HITS].add(explosion)

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
            self.game_groups[GameAttributes.ENEMIES],
            self.game_groups[GameAttributes.PLAYER_BULLETS],
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
                self.game_groups[GameAttributes.HITS].add(explosion)

    def try_kill_enemy(self, enemy):
        """
        Add a hit to an enemy. 
        Check if enemy is dead. If yes, remove enemy from
        the class enemy group. Also, increase player points.
        """
        enemy.enemy_service.add_hit()
        if enemy.enemy_service.is_dead:
            self.increase_player_points()
            enemy.remove(self.game_groups[GameAttributes.ENEMIES])

    def increase_player_points(self, coefficient=1):
        """
        Add points to player multiplied by the coefficient.

        Args: 
            coefficient: points are multiplied by the coefficient.
        """
        self.player.player_service.add_points(
            self.start_level_data[GameAttributes.LEVEL] * coefficient)

    def check_enemy_bullet_and_player_bullet_collisions(self):
        """
        Handle enemy bullet collisions with player bullets.
        """
        collisions = pygame.sprite.groupcollide(
            self.game_groups[GameAttributes.ENEMY_BULLETS],
            self.game_groups[GameAttributes.PLAYER_BULLETS],
            True,  # remove enemy bullet
            True   # remove player bullet
        )

        if collisions:
            for enemy_bullet, player_bullet in collisions.items():
                position = enemy_bullet.rect.center
                buffered_size = enemy_bullet.bullet.get_buffered_size(
                    10)
                explosion = HitAnimation(position, buffered_size)
                self.increase_player_points(BULLET_POINTS_COEFFICIENT)
                self.game_groups[GameAttributes.HITS].add(explosion)

    def update(self):
        """
        Updates the game state. 
        """
        self.player.handle_input()
        self.game_groups[GameAttributes.PLAYER_BULLETS].update()
        self.game_groups[GameAttributes.ENEMY_BULLETS].update()
        self.game_groups[GameAttributes.ENEMIES].update()
        self.game_groups[GameAttributes.HITS].update()

    def draw(self):
        self.drawer.draw()

    def run(self):
        """
        Runs the main game loop.
        Continuously handles events, updates the game state, 
        and renders the screen until the game is quit.
        """
        while self.gameover_data[GameAttributes.RUNNING]:
            self.handle_events()

            if self.is_game_over() and not self.gameover_data[GameAttributes.GAMEOVER]:
                self.end_game()
            elif self.gameover_data[GameAttributes.GAMEOVER]:
                self.save_user_statistics()
                self.game_over()
                self.reset_game(self.screen)
                pygame.time.wait(2000)
                return AppState.START_SCREEN
            elif not self.start_level_data[GameAttributes.LEVEL_STARTED]:
                self.start_new_level()
            else:
                self.update()
                self.check_sprite_collisions()
                self.move_to_next_level()
                self.draw()
                self.clock.tick(60)

        return AppState.QUIT

    def save_user_statistics(self):
        """
        Saves the player's score and level to the database if they are better than previous.
        """
        if not self.user_statistics_service:
            return

        user_id = self.user.user_id if self.user and self.user.user_id != 0 else 1
        points = self.player.player_service.points
        level = self.start_level_data[GameAttributes.LEVEL]

        self.user_statistics_service.upsert_user_statistics(
            user_id, points, level)

    def move_to_next_level(self):
        """
        Check if all enemies in the level are dead. 
        If the level was the last, player won the game.
        Else move to the next level.
        """
        if not self.game_groups[GameAttributes.ENEMIES]:
            self.start_level_data[GameAttributes.LEVEL] += 1
            # passed final levelga
            if self.start_level_data[GameAttributes.LEVEL] > self.levels.get_final_level():
                self.win_game()
            # load next level
            else:
                self.new_level_reset()
                self.start_level_data[GameAttributes.LEVEL_STARTED] = False

    def start_new_level(self):
        """
        When level changes, this is drawn before the new level starts.
        It resets level timer, clears the screen and shows the next level.
        """

        if self.start_level_data[GameAttributes.TRANSITION_TIMER] == 0:
            self.start_level_data[GameAttributes.TRANSITION_TIMER] = 1
            # show for 1 second at 60 FPS
            self.start_level_data[GameAttributes.TICKS_REMAINING] = 60

        self.screen.fill(BLACK)

        if self.start_level_data[GameAttributes.TICKS_REMAINING] > 0:
            self.drawer.draw_next_level_title()
            pygame.display.update()

            self.start_level_data[GameAttributes.TICKS_REMAINING] -= 1
            self.clock.tick(60)
        else:
            self.start_level_data[GameAttributes.LEVEL_STARTED] = True
            self.start_level_data[GameAttributes.TRANSITION_TIMER] = 0
            self.create_enemies()

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
        self.drawer.draw_game_over_text()
        points_position = Point(self.display_width//2,
                                self.display_height//2 + 40)
        self.drawer.draw_player_points(position=points_position, center=True)
        pygame.display.update()

    def is_game_over(self):
        if self.player.is_dead():
            return True
        return False
