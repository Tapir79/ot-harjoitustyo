import pygame
import sys


   
display_height = 600
display_width = 800

BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Space Invaders")

        self.clock = pygame.time.Clock()
        self.running = True
    
        # TODO player, enemies, bullets
    

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # update logic
    def update(self):
        pass

    # draw player, enemies and bullets
    def draw(self):
        self.screen.fill(BLACK)
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
