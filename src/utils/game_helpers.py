import random

from models.point import Point
from models.size import Size
from services.player_service import PlayerService


def get_player_lives(player: PlayerService):

    current_hits = player.get_hitcount()
    max_hits = player.get_max_hits()

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

    - center: the (x, y) center point (for example, player position)
    - screen_width: width of the screen, used to constrain horizontal bounds
    - count: how many positions to generate
    - y_offset: max vertical spread from the center
    - x_offset: max horizontal spread from center
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
                    [                      ] horizontal spread = ±100
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

    Y Axis ↓

        y=300 ─── start of range (up)
            ⋮
        y=400 ─── center
            ⋮
        y=500 ─── end of range (down)

        Randomly chooses y within this band.

    """
    up_min = center_y - y_offset
    down_max = center_y + y_offset
    up_y = max(0, up_min)
    down_y = min(screen_height, down_max)

    return random.randint(up_y, down_y)
