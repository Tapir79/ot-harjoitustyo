import pygame

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

class Player:
    def __init__(self, x, y, width=20, height=20, speed=5, left_boundary=0, right_boundary = 800):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.right_boundary = right_boundary
        self.left_boundary = left_boundary


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  
            self.x = move_player(self.x, 'a', self.speed, self.left_boundary, self.right_boundary, self.width)
        if keys[pygame.K_d]:  
            self.x = move_player(self.x, 'd', self.speed, self.left_boundary, self.right_boundary, self.width)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))