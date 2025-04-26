"""
General game constants. 

Defines general game constants like src-folder path, project path,
colours used in the game, boundaries, player attributes and other
sprite dimensions. 
"""
import os

SRC_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = SRC_ROOT[:-4]
DATABASE_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "database.db")
ASSETS_DIR = os.path.join(SRC_ROOT, "assets")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# global boundaries
UPPER_BOUNDARY = 0
LOWER_BOUNDARY = 600
LEFT_BOUNDARY = 0
RIGHT_BOUNDARY = 800

# Player starting attributes
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SPEED = 5
PLAYER_BULLET_SPEED = 5
PLAYER_MAX_HITS = 3
PLAYER_COOLDOWN = 0.3

# Bullet starting attributes
BULLET_WIDTH = 10
BULLET_HEIGHT = 20

# Enemy starting attributes
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
