from app_enums import LevelAttributes
from level_config import (ENEMY_COOLDOWN, ENEMY_SHOOTING_PROBABILITY,
                          ENEMY_COLS, ENEMY_ROWS, ENEMY_SPEED, FINAL_LEVEL,
                          ENEMY_BULLET_SPEED, ENEMY_MAX_HITS, ENEMY_IMAGE,
                          ENEMY_BULLET_SPEED_2, ENEMY_MAX_HITS_2, ENEMY_IMAGE_2,
                          ENEMY_BULLET_SPEED_3, ENEMY_MAX_HITS_3, ENEMY_IMAGE_3)


class LevelService():
    """
    Handles the configuration and data for different game levels.

    This service builds a dictionary of levels based on configuration constants.
    This makes scaling and adjusting level difficulty easier.
    """

    def __init__(self):
        """
        Initialize levels.
        """
        self.levels = {}
        self.final_level = FINAL_LEVEL
        self.initialize_levels()

    def get_level(self, level):
        """
        Get the configuration for a specific level.

        Args:
            level: The level number.

        Returns:
            dict: The configuration dictionary for the requested level.
        """
        return self.levels[level]

    def get_final_level(self):
        """
        Get the final level number.
        Example: levels are 1-15. This will return number 15.

        Returns:
            int: The number of the final level.
        """
        return self.final_level

    def initialize_levels(self):
        """
        Build a dictionary levels. Each level will be
        a new dictionary. 
        Example: levels[1] = {"enemy_cooldown":3, "enemy_cols":4 ...}
        """
        for level in range(1, FINAL_LEVEL + 1):
            self.levels[level] = {}
            self.create_common_level_attributes(level)
            self.create_specific_level_attributes(level)
            if not self.is_starting_level(level):
                self.scale_from_previous_level(level)

    def create_common_level_attributes(self, level):
        """
        Add shared common attributes to the given level.

        Args:
            level: The level number.
        """
        self.levels[level][LevelAttributes.ENEMY_COOLDOWN] = ENEMY_COOLDOWN
        self.levels[level][LevelAttributes.ENEMY_SHOOT_PROB] = ENEMY_SHOOTING_PROBABILITY
        self.levels[level][LevelAttributes.ENEMY_COLS] = ENEMY_COLS
        self.levels[level][LevelAttributes.ENEMY_ROWS] = ENEMY_ROWS
        self.levels[level][LevelAttributes.ENEMY_SPEED] = ENEMY_SPEED

    def create_specific_level_attributes(self, level):
        """
        Add level-specific attributes like enemy bullet speed and image.

        Args:
            level: The level number.
        """
        level_attributes = self.get_level_specific_attributes(level)
        bullet_speed, enemy_max_hits, enemy_image = level_attributes
        self.levels[level][LevelAttributes.ENEMY_BULLET_SPEED] = bullet_speed
        self.levels[level][LevelAttributes.ENEMY_MAX_HITS] = enemy_max_hits
        self.levels[level][LevelAttributes.ENEMY_IMAGE] = enemy_image

    def scale_from_previous_level(self, level):
        """
        Slightly increase difficulty compared to the previous level.

        Args:
            level: The current level number.
        """
        prev = level - 1
        shoot_prob = LevelAttributes.ENEMY_SHOOT_PROB
        enemy_cols = LevelAttributes.ENEMY_COLS
        enemy_rows = LevelAttributes.ENEMY_ROWS
        self.levels[level][shoot_prob] = self.levels[prev][shoot_prob] + 0.0001
        self.levels[level][enemy_cols] = self.levels[prev][enemy_cols] + 1
        self.levels[level][enemy_rows] = min(
            4, self.levels[prev][enemy_rows] + 1)

    def get_level_specific_attributes(self, level):
        """
        Return bullet speed, max hits, and image based on level range.

        Args:
            level: The level number.

        Returns:
            tuple: (bullet_speed, enemy_max_hits, enemy_image) for the level.
        """
        if level <= 5:
            return (ENEMY_BULLET_SPEED, ENEMY_MAX_HITS, ENEMY_IMAGE)
        if 6 <= level <= 10:
            return (ENEMY_BULLET_SPEED_2, ENEMY_MAX_HITS_2, ENEMY_IMAGE_2)

        return (ENEMY_BULLET_SPEED_3, ENEMY_MAX_HITS_3, ENEMY_IMAGE_3)

    def is_starting_level(self, level):
        """
        Check if the level is a starting point for a new level set.

        Args:
            level: The level number.

        Returns:
            bool: 
                - True: If a starting level of level group.
                - False: Not a starting level.
        """
        return level in (1, 6, 11)
