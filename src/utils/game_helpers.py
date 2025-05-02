import os
from pathlib import Path
import random

from app_enums import GameAttributes, LevelAttributes
from config import BRONZE, GOLD, PROJECT_ROOT, SILVER
from entities.general_statistics import GeneralStatistics
from entities.user_statistics import UserStatistics
from models.hit import Hit
from models.point import Point
from models.size import Size
from models.sprite_info import SpriteInfo
from services.enemy_service import EnemyService
from services.player_service import PlayerService


def create_enemy_service(point: Point,
                         size: Size,
                         speed,
                         enemy_max_hits,
                         enemy_cooldown):
    """
    Creates EnemyService object.

    Args:
        - point: (x,y)
        - size: (width, height)
        - speed: how fast enemy moves as integer
        - enemy_max_hits: how many hits the enemy can take
        - enemy_cooldown: how long the enemy waits 
                        before a new shooting attempt

    Returns:
        EnemyService object
    """
    return EnemyService(
        SpriteInfo(
            point,
            size,
            speed,
            Hit(0, enemy_max_hits)),
        cooldown=enemy_cooldown)


def init_start_level_attributes():
    """
    Returns:
        Starting level game attributes
    """
    return {
        GameAttributes.LEVEL: 1,
        GameAttributes.LEVEL_STARTED: False,
        GameAttributes.TRANSITION_TIMER: 0,
        GameAttributes.TICKS_REMAINING: 180,
        GameAttributes.LEVEL_COUNTDOWN: 3
    }


def set_new_level_attributes(current_level):
    """

    Args:
        current_level: game current level

    Returns:
        level attributes: enemy attributes of the current level
    """
    cooldown = current_level[LevelAttributes.ENEMY_COOLDOWN]
    enemy_shooting_probability = current_level[LevelAttributes.ENEMY_SHOOT_PROB]
    enemy_count_cols = current_level[LevelAttributes.ENEMY_COLS]
    enemy_rows = current_level[LevelAttributes.ENEMY_ROWS]
    enemy_speed = current_level[LevelAttributes.ENEMY_SPEED]
    enemy_bullet_speed = current_level[LevelAttributes.ENEMY_BULLET_SPEED]
    enemy_max_hits = current_level[LevelAttributes.ENEMY_MAX_HITS]
    enemy_image = current_level[LevelAttributes.ENEMY_IMAGE]
    return {GameAttributes.COOLDOWN: cooldown,
            GameAttributes.SHOOT_PROB: enemy_shooting_probability,
            GameAttributes.COLS: enemy_count_cols,
            GameAttributes.ROWS: enemy_rows,
            GameAttributes.SPEED: enemy_speed,
            GameAttributes.BULLET_SPEED: enemy_bullet_speed,
            GameAttributes.MAX_HITS: enemy_max_hits,
            GameAttributes.IMAGE: enemy_image
            }


def init_high_score(general_statistics_service):
    """

    Args:
        general_statistics_service: GeneralStatisticsService object


    Returns:
        high_score: game all time high score
    """
    return general_statistics_service.get_top_scores()[
        0].high_score


def get_game_over_initialization_data():
    """
    Return a dictionary of the game's gameover constants.
    """
    running = True
    gameover = False
    gameover_text = ""
    return {GameAttributes.RUNNING: running,
            GameAttributes.GAMEOVER: gameover,
            GameAttributes.GAMEOVER_TEXT: gameover_text}


def check_database_exists(database):
    """
    Health check before starting the game. If the database does not exist 
    print instructions for the user and exit gracefully.
    """
    schema_path = Path(PROJECT_ROOT) / "data" / database
    if not os.path.isfile(schema_path):
        print(f"Database file “{schema_path}” not found.")
        print("Please initialize your database first:")
        print("    poetry run invoke build")
        return False
    return True


def update_single_field(text: str, backspace: bool = False, char: str = None) -> str:
    """
    Purely compute the next value of a single text field.

    Args:
      text: current contents of the field
      backspace: whether to delete the last character
      char: a new character to append

    Returns:
      new text
    """
    if backspace:
        return text[:-1]
    if char:
        return text + char
    return text


def format_high_scores(rank_index, statistics: GeneralStatistics):
    """
    Format high score rows that they are aligned. 

    Args:
      rank_index: the rank is 1st, 2nd, 3rd. Index is 0,1,2.
      statistics: General game statistics. 

    Returns:
      rank: 1., 2. or 3.
      high_score: High score filled with zeros. 8 -> 00000008 
      username: Username or -- 
    """
    username = statistics.username if statistics else "---"
    high_score = statistics.high_score if statistics else 0
    rank = str(rank_index + 1) + " " * 7
    high_score = str(high_score).zfill(8) + " "

    return rank, high_score, username


def get_ending_points(current_points: int,
                      user_statistics: UserStatistics,
                      position: Point,
                      all_time_high_score: int = 0):
    """
    Collects the ending points information including:
    - Player's current session points
    - Player's personal high score (if logged in)
    - All-time high score (global)

    Args:
        current_points: User's current score
        user_statistics (UserStatistics): user statistics object.
        position (Point): Starting screen position to display the scores.
        all_time_high_score: The highest score ever reached in the game (all users).

    Returns:
        List of dicts, each dict containing:
            - 'text': Text to display
            - 'color': Text color
            - 'position': Point object where text should be displayed
    """

    ending_points_data = None
    y_spacing = 25

    if user_statistics:
        ending_points_data = get_logged_in_high_score_data(
            current_points, user_statistics, position, all_time_high_score, y_spacing)
    else:
        current_points_text = f"Points: {current_points}"

        ending_points_data = {
            "text": current_points_text,
            "color": BRONZE,
            "position": Point(position.x, position.y + y_spacing)
        }

    return ending_points_data


def get_logged_in_high_score_data(
        current_points,
        user_statistics,
        position,
        all_time_high_score,
        y_spacing):
    """
    Collects the ending points information for logged in user

    Args:
        current_points: User's current score
        user_statistics (UserStatistics): user statistics object.
        position (Point): Starting screen position to display the scores.
        all_time_high_score: The highest score ever reached in the game (all users).
        y_spacing: gap to previous text

    Returns:
        List of dicts, each dict containing:
            - 'text': Text to display
            - 'color': Text color
            - 'position': Point object where text should be displayed
    """
    high_score = user_statistics.high_score

    if current_points > high_score and current_points > all_time_high_score:
        return {
            "text": f"NEW HIGH SCORE: {current_points}",
            "color": GOLD,
            "position": Point(position.x, position.y + y_spacing)
        }
    if high_score < current_points <= all_time_high_score:
        return {
            "text": f"NEW RECORD: {current_points}",
            "color": SILVER,
            "position": Point(position.x, position.y + y_spacing)
        }

    if current_points >= all_time_high_score:
        text = f"NEW HIGH SCORE: {current_points}"
    elif current_points == high_score:
        text = f"NEW RECORD: {current_points}"
    else:
        text = f"Points / Record: {current_points}  /  {high_score}"

    return {
        "text": text,
        "color": BRONZE,
        "position": Point(position.x, position.y + y_spacing)
    }


def get_player_lives(player: PlayerService):
    """
    The function counts how many hearts player has left.
    It also counts how many hearts are broken.
    The counts are used to draw the hearts on the game screen.
    """

    current_hits = player.hitcount
    max_hits = player.max_hits

    hearts = 0
    broken_hearts = 0

    for i in range(max_hits):
        if i < max_hits - current_hits:
            hearts += 1
        else:
            broken_hearts += 1

    return hearts, broken_hearts


def get_random_positions_around_center_point(center: Point,
                                             screen_size: Size,
                                             offset: Size = Size(100, 150),
                                             count=5
                                             ):
    """
    Returns a list of random positions above a given point within screen bounds.

    Args:
        center: the (x, y) center point (for example, player position)
        screen_width: width of the screen, used to constrain horizontal bounds
        count: how many positions to generate
        offset: max vertical spread from the center, max horizontal spread from center 
    """

    screen_width = screen_size.width
    screen_height = screen_size.height
    x_offset = offset.width
    y_offset = offset.height
    positions = []

    for _ in range(count):
        rand_x = get_random_x(center.x, x_offset, screen_width)
        rand_y = get_random_y(center.y, y_offset, screen_height)
        positions.append((rand_x, rand_y))

    return positions


def get_random_x(center_x, x_offset, screen_width):
    """
    Return x between left_x and right_x
    If the offset goes over bounds get left / right wall coordinate
                                                  screen_width
    <--|-----------|-----------|-----------|-----------|-->
       0          200         300         400         500

                               ^             player at center_x = 300
                    [                      ] horizontal spread = +-100
                min_x=200               max_x=400
        [       left_min       ][       right_max      ]  cannot go over bounds
    """

    left_min = center_x - x_offset
    right_max = center_x + x_offset
    left_x = max(0, left_min)
    right_x = min(screen_width, right_max)

    return random.randint(left_x, right_x)


def get_random_y(center_y, y_offset, screen_height):
    """
    Like get_random_x but vertically

    Y Axis 
    |
    |    y=300 ─── start of range (up)
    |        ⋮
    |    y=400 ─── center
    |        ⋮
    |    y=500 ─── end of range (down)

        Randomly chooses y within this band.

    """
    up_min = center_y - y_offset
    down_max = center_y + y_offset
    up_y = max(0, up_min)
    down_y = min(screen_height, down_max)

    return random.randint(up_y, down_y)
