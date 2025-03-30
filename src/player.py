import os
import pygame

dirname = os.path.dirname(__file__)

WHITE = (255, 255, 255)

def move_player(x, key, speed=5, left_boundary=0, right_boundary=800, player_width=20):
    """
    Move the player left or right within the screen boundaries.
    
     Args:
        x (int): Current x-coordinate of the player.
        key (str): Key pressed by the user ('a' for left, 'd' for right).
        speed (int, optional): Movement speed in pixels. Defaults to 5.
        left_boundary (int, optional): Minimum x-coordinate the player can reach. 
        Defaults to 0.
        right_boundary (int, optional): Maximum x-coordinate the player can reach. 
        Defaults to 800.
        player_width (int, optional): Width of the player sprite. 
        Used to prevent moving out of bounds.

    Returns:
        int: The updated x-coordinate after movement.
    """
    if key == 'a':
        return max(left_boundary, x - speed)
    if key == 'd':
        return min(right_boundary - player_width, x + speed)
    return x

class Player (pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Handles movement and rendering of the player sprite. The player can move left and right
    using the 'a' and 'd' keys. The class also manages the player's position, speed,
    dimensions, and the boundaries within which the player is allowed to move.
    """
    def __init__(self, x, y, width=20, height=20, speed=5, left_boundary=0, right_boundary = 800):
        """
        Initializes the Player object.

        Args:
            x (int): Initial x-coordinate of the player.
            y (int): Initial y-coordinate of the player.
            width (int, optional): Width of the player sprite. Defaults to 20.
            height (int, optional): Height of the player sprite. Defaults to 20.
            speed (int, optional): Movement speed of the player. Defaults to 5.
            left_boundary (int, optional): Minimum x-coordinate. Defaults to 0.
            right_boundary (int, optional): Maximum x-coordinate. Defaults to 800.
        """
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
        """
        Handles keyboard input for the player.

        Moves the player left if 'a' is pressed, and right if 'd' is pressed.
        Movement is bounded by left and right limits of the screen.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x = move_player(self.x,
                                 'a',
                                 speed = self.speed,
                                 left_boundary = self.left_boundary,
                                 right_boundary = self.right_boundary,
                                 player_width = self.width)
        if keys[pygame.K_d]:
            self.x = move_player(self.x,
                                 'd',
                                 speed = self.speed,
                                 left_boundary = self.left_boundary,
                                 right_boundary = self.right_boundary,
                                 player_width = self.width)

    def draw(self, screen):
        """
        Draws the player sprite onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the player on.
        """
        screen.blit(self.image, (self.x, self.y))
