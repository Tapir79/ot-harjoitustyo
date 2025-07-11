import pygame
from app_enums import AppState, GameAttributes
from config import (BULLET_POINTS_COEFFICIENT,
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
from services.enemy_service import EnemyService
from services.general_statistics_service import GeneralStatisticsService
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService
from services.level_service import LevelService
from ui.game_views.game.draw import GameDrawer
from ui.game_views.game.init import (create_player,
                                     init_display,
                                     init_game_groups,
                                     init_game_info,
                                     init_ui_images)
from utils.ui_helpers import (get_buffered_size,
                              get_game_over_initialization_data,
                              init_high_score,
                              init_start_level_attributes,
                              set_new_level_attributes)
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

    def run(self):
        """
        Runs the main game loop.
        Continuously handles events, updates the game state, 
        and renders the screen until the game is quit.
        """
        while self.gameover_data[GameAttributes.RUNNING]:
            self.handle_events()

            if self.is_game_over() and not self.gameover_data[GameAttributes.GAMEOVER]:
                self.lose_game()
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

    def update(self):
        """
        Update the game state. 
        This happens on every game loop.
        """
        self.player.handle_input()
        self.game_groups[GameAttributes.PLAYER_BULLETS].update()
        self.game_groups[GameAttributes.ENEMY_BULLETS].update()
        self.game_groups[GameAttributes.ENEMIES].update()
        self.game_groups[GameAttributes.HITS].update()

    def draw(self):
        """
        Draw game background, player, enemies, bullets and animations on screen. 
        This happens on every game loop.
        All drawing is handled in a separate GameDrawer class. 
        """
        self.drawer.draw()

    ################## INIT ######################

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

        return EnemyService.create(Point(x, y),
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

    ########################### UPDATE ###########################

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
            explosion = self.drawer.get_hit_animation(position, size)
            self.game_groups[GameAttributes.HITS].add(explosion)

            if self.player.is_dead():
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
            explosion = self.drawer.get_hit_animation(position, size)
            self.game_groups[GameAttributes.HITS].add(explosion)

            if self.player.is_dead():
                self.player.kill()

    def check_enemy_and_player_bullet_collisions(self):
        """
        Handle enemy collisions with player bullets. 
        First get all player bullets. 
        Then check collisions with each enemy.
        Using pygame group collisions. 
        Remove enemy.
        Remove bullet.
        """
        collisions = pygame.sprite.groupcollide(
            self.game_groups[GameAttributes.ENEMIES],
            self.game_groups[GameAttributes.PLAYER_BULLETS],
            False,
            True
        )

        if collisions:
            for enemy, bullets in collisions.items():
                for _ in bullets:
                    self.try_kill_enemy(enemy)

                position = enemy.rect.center
                size = enemy.enemy_service.size
                explosion = self.drawer.get_hit_animation(position, size)
                self.game_groups[GameAttributes.HITS].add(explosion)

    def try_kill_enemy(self, enemy):
        """
        Add a hit to an enemy. 
        Check if enemy is dead. If yes, remove enemy from
        the class enemy group. Also, increase player points.
        """
        enemy.enemy_service.add_hit()
        if enemy.is_dead():
            self.increase_player_points()
            enemy.remove(self.game_groups[GameAttributes.ENEMIES])

    def increase_player_points(self, coefficient=1):
        """
        Add points to player multiplied by the coefficient.

        Args: 
            coefficient: points are multiplied by the coefficient.
        """
        level_enemy = self.enemy_attributes[GameAttributes.IMAGE]
        points_char = ''.join([char for char in level_enemy if char in "123"])
        points = int(points_char)
        self.player.player_service.add_points(
            points * coefficient)

    def check_enemy_bullet_and_player_bullet_collisions(self):
        """
        Handle enemy bullet collisions with player bullets.
        Remove enemy bullet.
        Remove player bullet.
        """
        collisions = pygame.sprite.groupcollide(
            self.game_groups[GameAttributes.ENEMY_BULLETS],
            self.game_groups[GameAttributes.PLAYER_BULLETS],
            True,
            True
        )

        if collisions:
            for enemy_bullet, player_bullet in collisions.items():
                position = enemy_bullet.rect.center
                buffered_size = get_buffered_size(enemy_bullet.bullet.size,
                                                  10)
                explosion = self.drawer.get_hit_animation(
                    position, buffered_size)
                self.increase_player_points(BULLET_POINTS_COEFFICIENT)
                self.game_groups[GameAttributes.HITS].add(explosion)

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
            if self.start_level_data[GameAttributes.LEVEL] > self.levels.get_final_level():
                self.win_game()
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
        """
        Player wins. An animation plays and gameover data is set.
        """
        self.drawer.fly_player_over_bounds_animation()
        self.gameover_data[GameAttributes.GAMEOVER_TEXT] = "YOU WIN!"
        self.gameover_data[GameAttributes.GAMEOVER] = True

    def lose_game(self):
        """
        Player loses. An animation plays and gameover data is set.
        """
        self.drawer.destroy_player_animation()
        self.gameover_data[GameAttributes.GAMEOVER_TEXT] = "GAME OVER"
        self.gameover_data[GameAttributes.GAMEOVER] = True

    def game_over(self):
        """
        Game is over. Draw gameover text (win or lose). 
        Draw player received points. 
        Update display.
        """
        self.screen.fill(BLACK)
        self.drawer.draw_game_over_text()
        points_position = Point(self.display_width//2,
                                self.display_height//2 + 40)
        self.drawer.draw_player_points(position=points_position, center=True)
        pygame.display.update()

    def is_game_over(self):
        """
        Check if player sprite is dead.

        Returns:
            is_dead: True if player is dead
        """
        if self.player.is_dead():
            return True
        return False
