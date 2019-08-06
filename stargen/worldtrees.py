"""
GURPS Space 4th Edition Advanced Worldbuilding - Generating World Detials

This module contains all the applicable data from the Generating World Details
section of the Advanced Worldbuilding system. To easily account for a range
of inputs the IntervalTree data structure is used. Due to the interval 
inclusivity of Python clashing with the interval exclusivity of the tables,
most ranges are notated as [start:end+1]. Due to this and to fit the data
structure better, tables have been modified and in some cases omitted.

"""

from intervaltree import Interval, IntervalTree
import random

from typing import Any, Union, Optional, List

# This is a duplicate I need to remove once I square away the import
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


# World Types
tiny_world_type_assignment_tree = IntervalTree()
tiny_world_type_assignment_tree[0 : 140 + 1] = ["Tiny (Ice)", "Tiny (Sulfur)"]
tiny_world_type_assignment_tree[141 : 13145.8 + 1] = "Tiny (Rock)"

small_world_type_assignment_tree = IntervalTree()
small_world_type_assignment_tree[0 : 80 + 1] = "Small (Hadean)"
small_world_type_assignment_tree[81 : 140 + 1] = "Small (Ice)"
small_world_type_assignment_tree[141 : 13145.8 + 1] = "Small (Rock)"

standard_world_type_assignment_tree = IntervalTree()
standard_world_type_assignment_tree[0 : 80 + 1] = "Standard (Hadean)"
standard_world_type_assignment_tree[81 : 150 + 1] = "Standard (Ice)"
standard_world_type_assignment_tree[151 : 230 + 1] = [
    "Standard (Ice)",
    "Standard (Ammonia)",
]
standard_world_type_assignment_tree[231 : 240 + 1] = "Standard (Ice)"
standard_world_type_assignment_tree[241 : 320 + 1] = [
    "Standard (Ocean)",
    "Standard (Garden)",
]
standard_world_type_assignment_tree[321 : 500 + 1] = "Standard (Greenhouse)"
standard_world_type_assignment_tree[501 : 13145.8 + 1] = "Standard (Chthonian)"

large_world_type_assignment_tree = IntervalTree()
large_world_type_assignment_tree[0 : 150 + 1] = "Large (Ice)"
large_world_type_assignment_tree[151 : 230 + 1] = ["Large (Ice)", "Large (Ammonia)"]
large_world_type_assignment_tree[231 : 240 + 1] = "Large (Ice)"
large_world_type_assignment_tree[241 : 320 + 1] = ["Large (Ocean)", "Large (Garden)"]
large_world_type_assignment_tree[321 : 500 + 1] = "Large (Greenhouse)"
large_world_type_assignment_tree[501 : 13145.8 + 1] = "Large (Chthonian)"

# Atmosphere
no_atmosphere_world_types = [
    "Asteroid Belt",
    "Tiny (Ice)",
    "Tiny (Rock)",
    "Tiny (Sulfur)",
    "Small (Hadean)",
    "Small (Rock)",
    "Standard (Hadean)",
    "Standard (Chthonian)",
    "Large (Chthonian)",
]

# World Size
icy_core_world_types = [
    "Tiny (Ice)",
    "Tiny (Sulfur)",
    "Small (Hadean)",
    "Small (Ice)",
    "Standard (Hadean)",
    "Standard (Ammonia)",
    "Large (Ammonia)",
]
small_iron_core_world_types = ["Tiny (Rock)", "Small (Rock)"]

gas_giant_size_tree = IntervalTree()
gas_giant_size_tree[3 : 8 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[9 : 10 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[11 : 11 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[12 : 12 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[13 : 13 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[14 : 14 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[15 : 15 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[16 : 16 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]
gas_giant_size_tree[17 : 18 + 1] = [[10, 0.42], [100, 0.18], [600, 0.31]]

# Dynamic Parameters
planetary_orbital_eccentricity_tree = IntervalTree()
planetary_orbital_eccentricity_tree[-100 : 3 + 1] = 0.0
planetary_orbital_eccentricity_tree[4 : 6 + 1] = 0.05
planetary_orbital_eccentricity_tree[7 : 9 + 1] = 0.1
planetary_orbital_eccentricity_tree[10 : 11 + 1] = 0.15
planetary_orbital_eccentricity_tree[12 : 12 + 1] = 0.2
planetary_orbital_eccentricity_tree[13 : 13 + 1] = 0.3
planetary_orbital_eccentricity_tree[14 : 14 + 1] = 0.4
planetary_orbital_eccentricity_tree[15 : 15 + 1] = 0.5
planetary_orbital_eccentricity_tree[16 : 16 + 1] = 0.6
planetary_orbital_eccentricity_tree[17 : 17 + 1] = 0.7
planetary_orbital_eccentricity_tree[18 : 100 + 1] = 0.8

# Special Rotation
special_rotation_tree = IntervalTree()
special_rotation_tree[0 : 6 + 1] = 0
special_rotation_tree[7 : 7 + 1] = roll_dice(1) * 2 * 24
special_rotation_tree[8 : 8 + 1] = roll_dice(1) * 5 * 24
special_rotation_tree[9 : 9 + 1] = roll_dice(1) * 10 * 24
special_rotation_tree[10 : 10 + 1] = roll_dice(1) * 20 * 24
special_rotation_tree[11 : 11 + 1] = roll_dice(1) * 50 * 24
special_rotation_tree[12 : 12 + 1] = roll_dice(1) * 100 * 24

# Axial Tilt
axial_tilt_extended_tree = IntervalTree()
axial_tilt_extended_tree[1 : 2 + 1] = 50 + roll_dice(2, -2)
axial_tilt_extended_tree[3 : 4 + 1] = 60 + roll_dice(2, -2)
axial_tilt_extended_tree[5 : 5 + 1] = 70 + roll_dice(2, -2)
axial_tilt_extended_tree[6 : 6 + 1] = 80 + roll_dice(2, -2)

axial_tilt_tree = IntervalTree()
axial_tilt_tree[3 : 6 + 1] = 0 + roll_dice(2, -2)
axial_tilt_tree[7 : 9 + 1] = 10 + roll_dice(2, -2)
axial_tilt_tree[10 : 12 + 1] = 20 + roll_dice(2, -2)
axial_tilt_tree[13 : 14 + 1] = 30 + roll_dice(2, -2)
axial_tilt_tree[15 : 16 + 1] = 40 + roll_dice(2, -2)
axial_tilt_tree[17 : 18 + 1] = look_up(axial_tilt_extended_tree, roll_dice(1))

# Volcanic Activity
volcanic_activity_tree = IntervalTree()
volcanic_activity_tree[0 : 16 + 1] = "None"
volcanic_activity_tree[17 : 20 + 1] = "Light"
volcanic_activity_tree[21 : 26 + 1] = "Moderate"
volcanic_activity_tree[27 : 70 + 1] = "Heavy"
volcanic_activity_tree[71 : 16000 + 1] = "Extreme"

# Tectonic Activity
tectonic_activity_tree = IntervalTree()
tectonic_activity_tree[-6000 : 6 + 1] = "None"
tectonic_activity_tree[7 : 10 + 1] = "Light"
tectonic_activity_tree[11 : 14 + 1] = "Moderate"
tectonic_activity_tree[15 : 18 + 1] = "Heavy"
tectonic_activity_tree[19 : 6000 + 1] = "Extreme"
