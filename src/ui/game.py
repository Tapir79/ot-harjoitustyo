import pygame
import random
from pygame.sprite import Group
from ui.animations.player_hit_animation import PlayerHitAnimation
from ui.animations.hit_animation import HitAnimation
from ui.enemy import EnemySprite
from ui.player import PlayerSprite
from services.player_service import PlayerService
from services.enemy_service import EnemyService
from models.hit import Hit
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from config import LOWER_BOUNDARY, RIGHT_BOUNDARY, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, ENEMY_SPEED, PLAYER_MAX_HITS, ENEMY_MAX_HITS, ENEMY_COUNT_COLS, ENEMY_ROWS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Game:
    """
    The Game class represents the main game logic for a simple Space Invaders-style game.

    It handles initialization, the main game loop, event handling, updating game state,
    and rendering the screen including the player and on-screen instructions.
    """

    def __init__(self):
        """
        Initializes the game, including the display, player, clock, and font.
        Sets up the game window and player object.
        """
        pygame.init()
        self.display_height = LOWER_BOUNDARY
        self.display_width = RIGHT_BOUNDARY
        self.screen = pygame.display.set_mode(
            (self.display_width, self.display_height))
        pygame.display.set_caption("Alien Attack")

        # bullets
        self.player_bullet_group = Group()
        self.enemy_bullet_group = Group()
        self.enemy_group = Group()
        self.hit_group = pygame.sprite.Group()

        # player
        self.player = self.create_player()

        # enemies
        self.create_enemies()

        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 30)
        self.gameover = False

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
            self.player.player.sprite_info.add_hit()

            position = self.player.rect.center
            size = self.player.player.sprite_info.size
            explosion = HitAnimation(position, size)
            self.hit_group.add(explosion)

            print("player is dead:", self.player.is_dead())
            if self.player.is_dead():
                self.player.kill()

    def check_player_and_enemy_bullet_collisions(self):
        """
        Handle player collisions with enemy bullets.
        """
        hits = pygame.sprite.spritecollide(
            self.player, self.enemy_bullet_group, dokill=True)

        if hits:
            self.player.player.sprite_info.add_hit()

            position = self.player.rect.center
            size = self.player.player.sprite_info.size
            explosion = HitAnimation(position, size)
            self.hit_group.add(explosion)

            print("player is dead:", self.player.is_dead())
            if self.player.is_dead():
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
            True,  # remove enemy
            True   # remove bullet
        )

        if collisions:
            for enemy, bullets in collisions.items():
                position = enemy.rect.center
                size = enemy.enemy.sprite_info.size
                explosion = HitAnimation(position, size)
                self.hit_group.add(explosion)

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
                buffered_size = enemy_bullet.bullet.sprite_info.size.get_buffered_size(
                    10)
                explosion = HitAnimation(position, buffered_size)
                self.hit_group.add(explosion)

    def update(self):
        """
        Updates the game state. Currently only handles player input.
        """
        self.player.handle_input()
        self.player_bullet_group.update()
        self.enemy_bullet_group.update()
        self.enemy_group.update()
        self.hit_group.update()

    def draw(self):
        """
        Renders the game screen.
        Clears the screen, draws the player and instruction text, and updates the display.
        """
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        self.player_bullet_group.draw(self.screen)
        self.enemy_bullet_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.hit_group.draw(self.screen)
        instruction_text = self.font.render(
            "Move the player with 'a' and 'd', Shoot with SPACE", True, WHITE)
        self.screen.blit(instruction_text, (20, 20))
        pygame.display.update()

    def run(self):
        """
        Runs the main game loop.
        Continuously handles events, updates the game state, 
        and renders the screen until the game is quit.
        """
        while self.running:
            self.handle_events()
            if self.is_game_over() and self.gameover == False:
                position = self.player.rect.center
                positions = self.get_random_positions_above_player(position)
                size = self.player.player.sprite_info.size
                player_size = size.get_buffered_size(20)
                explosion = PlayerHitAnimation(position, player_size)
                self.play_animation_once(explosion)

                for pos in positions:
                    explosion = HitAnimation(pos, size)
                    self.play_animation_once(explosion)
                    self.wait(5)

                self.gameover = True
            elif self.gameover == True:
                self.game_over()
            else:
                self.update()
                self.check_sprite_collisions()
                self.draw()
                self.clock.tick(60)

    def wait(self, n):
        for i in range(0, n):
            self.clock.tick(60)

    def get_random_positions_above_player(self, center, count=5, y_offset=100, max_spread=150):
        """
        Returns a list of random positions above the player within screen bounds.

        - center: the (x, y) center of the player
        - count: how many positions to generate
        - y_offset: how high above the player the effects appear
        - max_spread: max horizontal spread from center
        """
        cx, cy = center
        positions = []

        for _ in range(count):
            rand_x = random.randint(
                max(0, cx - max_spread),
                min(self.screen.get_width(), cx + max_spread)
            )
            rand_y = max(0, cy - y_offset - random.randint(0, 40))
            positions.append((rand_x, rand_y))

        return positions

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

    def game_over(self):
        self.screen.fill(BLACK)
        instruction_text = self.font.render(
            "GAME OVER", True, WHITE)
        text_rect = instruction_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(instruction_text, text_rect)

        pygame.display.update()

    def is_game_over(self):
        if self.player.is_dead():
            return True
        return False

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

    def create_enemies(self, rows=ENEMY_ROWS, cols=ENEMY_COUNT_COLS, spacing=60):
        """
        Create enemies on screen. 
        """
        enemy_width = 40
        enemy_height = 40
        margin_x = 50
        margin_y = 50

        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing
                y = margin_y + row * spacing

                enemy_info = SpriteInfo(
                    Point(x, y), Size(enemy_width, enemy_height), ENEMY_SPEED, Hit(0, ENEMY_MAX_HITS))
                enemy_service = EnemyService(
                    enemy_info)
                enemy_sprite = EnemySprite(
                    enemy_service, self.enemy_bullet_group)
                self.enemy_group.add(enemy_sprite)
