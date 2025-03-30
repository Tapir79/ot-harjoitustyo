import pygame
import os

dirname = os.path.dirname(__file__)

WHITE = (255, 255, 255)

def move_player(x, key, speed=5, left_boundary=0, right_boundary=800, player_width=20):
    """
    Move the player left or right.
    
    :param x: Current x position of the player
    :param key: Key pressed ('a' = left, 'd' = right)
    :param speed: steps per key pressed (default: 5)
    :return: New x position
    """
    if key == 'a':  # Move left
        return max(left_boundary, x - speed)
    elif key == 'd':  # Move right
        return min(right_boundary - player_width, x + speed)
    return x  

class Player (pygame.sprite.Sprite):
    def __init__(self, x, y, width=20, height=20, speed=5, left_boundary=0, right_boundary = 800):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.right_boundary = right_boundary
        self.left_boundary = left_boundary
        self.image = pygame.image.load(
            os.path.join(dirname, "assets", "player.png")
        ).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  
            self.x = move_player(self.x, 'a', self.speed, self.left_boundary, self.right_boundary, self.width)
        if keys[pygame.K_d]:  
            self.x = move_player(self.x, 'd', self.speed, self.left_boundary, self.right_boundary, self.width)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))