"""
Configuration constants for enemy attributes across different game levels.

Defines shooting cooldowns, enemy movement speeds, bullet speeds, enemy images,
and level difficulty scaling.
"""

# Common level starting attributes
ENEMY_COOLDOWN = 30
ENEMY_SHOOTING_PROBABILITY = 0.0006
ENEMY_COLS = 4
ENEMY_ROWS = 2
ENEMY_SPEED = 1

# Level 1 -5
ENEMY_BULLET_SPEED = 3
ENEMY_MAX_HITS = 1
ENEMY_IMAGE = "enemy1.png"

# Level 6-10
ENEMY_BULLET_SPEED_2 = 4
ENEMY_MAX_HITS_2 = 2
ENEMY_IMAGE_2 = "enemy2.png"

# Level 11-15
ENEMY_BULLET_SPEED_3 = 5
ENEMY_MAX_HITS_3 = 3
ENEMY_IMAGE_3 = "enemy3.png"

FINAL_LEVEL = 15
