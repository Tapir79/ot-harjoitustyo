import random

from config import BRONZE, GOLD, SILVER
from entities.general_statistics import GeneralStatistics
from entities.user_statistics import UserStatistics
from models.point import Point
from models.size import Size
from services.player_service import PlayerService


def format_high_scores(rank_index, statistics: GeneralStatistics):
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
        user (User): The logged-in user (or None).
        player_service (PlayerService): The player's service instance.
        user_service (UserService): The service to fetch user info.
        user_statistics_service (UserStatisticsService): The service to fetch user statistics.
        position (Point): Starting screen position to display the scores.

    Returns:
        List of dicts, each dict containing:
            - 'text': Text to display
            - 'position': Point object where text should be displayed
    """

    ending_points_data = []
    y_spacing = 25  # Space between lines

    current_points_text = f"Points: {current_points}"
    ending_points_data.append({
        "text": current_points_text,
        "color": BRONZE,
        "position": Point(position.x, position.y)
    })

    if user_statistics:
        high_score = user_statistics.high_score if user_statistics else 0

        if current_points > high_score and current_points > all_time_high_score:
            high_score_text = f"NEW HIGH SCORE: {current_points}"
            color = GOLD
        elif high_score < current_points <= all_time_high_score:
            high_score_text = f"NEW RECORD: {current_points}"
            color = SILVER
        else:
            high_score_text = f"Your record: {high_score}"
            color = BRONZE

        ending_points_data.append({
            "text": high_score_text,
            "color": color,
            "position": Point(position.x, position.y + y_spacing)
        })

    return ending_points_data


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
