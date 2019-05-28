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
tiny_world_type_assignment_tree[0:140+1] = ["Tiny (Ice)", "Tiny (Sulfur)"]
tiny_world_type_assignment_tree[141:1000+1] = ["Tiny (Rock)"]

small_world_type_assignment_tree = IntervalTree()
small_world_type_assignment_tree[0:80+1] = ["Small (Hadean)"]
small_world_type_assignment_tree[81:140+1] = ["Small (Ice)"]
small_world_type_assignment_tree[141:1000+1] = ["Small (Rock)"]

standard_world_type_assignment_tree = IntervalTree()
standard_world_type_assignment_tree[0:80+1] = ["Standard (Hadean)"]
standard_world_type_assignment_tree[81:150+1] = ["Standard (Ice)"]
standard_world_type_assignment_tree[151:230+1] = ["Standard (Ice)", "Standard (Ammonia)"]
standard_world_type_assignment_tree[231:240+1] = ["Standard (Ice)"]
standard_world_type_assignment_tree[241:320+1] = ["Standard (Ocean)", "Standard (Garden)"]
standard_world_type_assignment_tree[321:500+1] = ["Standard (Greenhouse)"]
standard_world_type_assignment_tree[501:1000+1] = ["Standard (Chthonian)"]

large_world_type_assignment_tree = IntervalTree()
large_world_type_assignment_tree[0:150+1] = ["Large (Ice)"]
large_world_type_assignment_tree[151:230+1] = ["Large (Ice)", "Large (Ammonia)"]
large_world_type_assignment_tree[231:240+1] = ["Large (Ice)"]
large_world_type_assignment_tree[241:320+1] = ["Large (Ocean)", "Large (Garden)"]
large_world_type_assignment_tree[321:500+1] = ["Large (Greenhouse)"]
large_world_type_assignment_tree[501:1000+1] = ["Large (Chthonian)"]

# Atmosphere
# import basictrees as bt
# bt.atmospheric_pressure_categories_tree
# bt.marginal_atmospheres_trees

# Hydrographics

# Climate
# 