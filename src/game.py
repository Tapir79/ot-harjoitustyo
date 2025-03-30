import pygame

from player import Player

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
        self.display_height = 600
        self.display_width = 800
        self.screen = pygame.display.set_mode(
            (self.display_width, self.display_height))
        self.player = Player(self.display_width // 2,
                             self.display_height - 50,
                             40, 40, 5, 0,
                             self.display_width)

        pygame.display.set_caption("Space Invaders")

        self.clock = pygame.time.Clock()
        self.running = True

        # TODO: Add enemies and bullets
        self.font = pygame.font.Font(None, 30)

    def handle_events(self):
        """
        Handles user input events such as closing the game window.
        If the user clicks the close button, the game loop will stop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """
        Updates the game state. Currently only handles player input.
        """
        self.player.handle_input()

    def draw(self):
        """
        Renders the game screen.
        Clears the screen, draws the player and instruction text, and updates the display.
        """
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        instruction_text = self.font.render(
            "Move the player with 'a' and 'd'", True, WHITE)
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
            self.draw()
            self.clock.tick(60)
