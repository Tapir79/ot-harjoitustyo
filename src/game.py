import pygame
import sys

from player import Player



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        self.display_height = 600
        self.display_width = 800
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.player = Player(self.display_width // 2, self.display_height // 2, 20, 20, 5, 0, self.display_width)
        pygame.display.set_caption("Space Invaders")

        self.clock = pygame.time.Clock()
        self.running = True
    
        # TODO enemies, bullets
    

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # update logic
    def update(self):
        self.player.handle_input()

    # draw player, enemies and bullets
    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
