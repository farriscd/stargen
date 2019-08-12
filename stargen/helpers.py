import random
from typing import Any, Union, Optional, List
from intervaltree import Interval, IntervalTree


def roll_dice(number_of_dice: int = 1, modifier: int = 0) -> int:
    """Return the result of a simulated 6-sided die roll

    Args:
        number_of_dice: The number of die to be rolled
        modifier: A number to be added/subtracted to the sum of the die roll
    """
    sum_of_dice = 0
    for _ in range(number_of_dice):
        sum_of_dice += random.randrange(1, 6 + 1)
    return sum_of_dice + modifier


def look_up(tree: IntervalTree, point: Union[float, int]) -> Any:
    """Return data from interval tree at point

    Args:
        tree: The interval tree containing data to lookup
        point: The point within range that the data is stored
    """
    return sorted(tree[point])[0].data
