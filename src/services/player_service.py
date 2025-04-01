class PlayerService:
    def __init__(self, x, y, width=20, height=20, speed=5, left_boundary=0, right_boundary=800):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary

    def move(self, key):
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
            self.x = max(self.left_boundary, self.x - self.speed)
        if key == 'd':
            self.x = min(self.right_boundary - self.width, self.x + self.speed)
        return self.x
    
    def get_position(self):
        """Get player position"""
        return self.x, self.y
    
    def set_speed(self, amount=1):
        """Set player speed to some amount"""
        self.speed = amount
    
    def increase_speed(self, amount=1):
        """Increase player speed by the given amount"""
        self.speed += amount

    def decrease_speed(self, amount=1):
        """Decrease player speed by the given amount. Min=1"""
        self.speed = max(1, self.speed - amount)