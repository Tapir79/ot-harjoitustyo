import pygame
from pygame.sprite import Group
from ui.animations.hit import HitAnimation
from ui.enemy import EnemySprite
from ui.player import PlayerSprite
from services.player_service import PlayerService
from services.enemy_service import EnemyService
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from config import LOWER_BOUNDARY, RIGHT_BOUNDARY

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

    def handle_events(self):
        """
        Handles user input events such as closing the game window.
        If the user clicks the close button, the game loop will stop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def check_sprite_collisions(self):
        self.check_enemy_collisions()

    def check_enemy_collisions(self):
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
                size = enemy.bullet.sprite_info.size if hasattr(
                    enemy, "bullet") else enemy.enemy.sprite_info.size
                explosion = HitAnimation(position, size)
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
            self.update()
            self.check_sprite_collisions()
            self.draw()
            self.clock.tick(60)

    def create_player(self):
        player_position = Point(self.display_width // 2,
                                self.display_height - 50)
        player_size = Size(40, 40)
        player_info = SpriteInfo(player_position, player_size, 5)

        player_service = PlayerService(
            sprite_info=player_info
        )

        return PlayerSprite(player_service, self.player_bullet_group)

    def create_enemies(self, rows=3, cols=6, spacing=60):
        enemy_width = 40
        enemy_height = 40
        margin_x = 50
        margin_y = 50

        for row in range(rows):
            for col in range(cols):
                x = margin_x + col * spacing
                y = margin_y + row * spacing

                enemy_info = SpriteInfo(
                    Point(x, y), Size(enemy_width, enemy_height), 1)
                enemy_service = EnemyService(
                    enemy_info)
                enemy_sprite = EnemySprite(
                    enemy_service, self.enemy_bullet_group)
                self.enemy_group.add(enemy_sprite)
