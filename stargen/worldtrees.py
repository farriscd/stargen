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

# World Types
tiny_world_type_assignment_tree = IntervalTree()
tiny_world_type_assignment_tree

small_world_type_assignment_tree = IntervalTree()
small_world_type_assignment_tree

standard_world_type_assignment_tree = IntervalTree()
standard_world_type_assignment_tree

large_world_type_assignment_tree = IntervalTree()
large_world_type_assignment_tree