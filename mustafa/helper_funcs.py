"""Helper functions for the main-supermarket-program"""
import random
import numpy as np


AISLE_POSITIONS = {'checkout1': (2, 3, 8, 9),
                   'checkout2': (6, 7, 8, 9),
                   'checkout3': (10, 11, 8, 9),
                   'drinks': (2, 3, 2, 6),
                   'spices': (6, 7, 2, 6),
                   'dairy': (10, 11, 2, 6),
                   'fruit': (14, 15, 2, 6)}


def get_target_coordinates(target):
    """returns the tile-location of the target-aisle."""
    if target == 'checkout':
        target = random.choices(['checkout1', 'checkout2', 'checkout3'])[0]
    t_loc = AISLE_POSITIONS[target]
    locx = np.random.randint(low=t_loc[0], high=t_loc[1]+1)
    locy = np.random.randint(low=t_loc[2], high=t_loc[3]+1)
    return locx, locy

def move_step(x, y, xt, yt, current, target):
    """Returns new location of the customer in the direction of the target."""
    if current == 'entrance' and y not in [1, 7]:
        y -= 1
    elif target == 'exit':
        if y == 10 and x != 14:
            x += 1
        else:
            y += 1
    elif y not in [1, 7] and x != xt: # move up/down, depending on which is quicker
        if y > yt:
            y += 1
        else:
            y -= 1
    elif y in [1, 7] and x != xt: # move on x- axis
        if x > xt:
            x -= 1
        else:
            x += 1
    else:  # move up or down
        if y > yt:
            y -= 1
        else:
            y += 1
    return x, y

def get_time(minutes):
    """Returns current time in format HH:MM from given minute-counter"""
    current_hour = 7 + minutes // 60
    current_mins = minutes % 60
    current_time = f'{current_hour:02}:{current_mins:02}'
    return current_time
