"""
GURPS Space 4th Edition Basic Worldbuilding data

This module contains some of the applicable data from the Generating Star Systems
section of the Basic Worldbuilding system. To easily account for a range
of inputs the IntervalTree data structure is used. Due to the interval 
inclusivity of Python clashing with the interval exclusivity of the tables,
most ranges are notated as [start:end+1]. Due to this and to fit the data
structure better, tables have been modified and in some cases omitted.

Atmospheric Pressure Categories edited to allow ranges of values.

Todo:
    * Implement any of this stuff
"""

from intervaltree import Interval, IntervalTree

# World Type
overall_type_tree = IntervalTree()
overall_type_tree[3 : 7 + 1] = "Hostile"
overall_type_tree[8 : 13 + 1] = "Barren"
overall_type_tree[14 : 18 + 1] = "Garden"

world_type_tree = IntervalTree()
world_type_tree[3 : 3 + 1] = [
    "Standard (Chthonian)",
    "Small (Hadean)",
    "Standard (Garden)",
]
world_type_tree[4 : 4 + 1] = [
    "Standard (Chthonian)",
    "Small (Ice)",
    "Standard (Garden)",
]
world_type_tree[5 : 5 + 1] = [
    "Standard (Greenhouse)",
    "Small (Rock)",
    "Standard (Garden)",
]
world_type_tree[6 : 6 + 1] = [
    "Standard (Greenhouse)",
    "Small (Rock)",
    "Standard (Garden)",
]
world_type_tree[7 : 7 + 1] = ["Tiny (Sulfur)", "Tiny (Rock)", "Standard (Garden)"]
world_type_tree[8 : 8 + 1] = ["Tiny (Sulfur)", "Tiny (Rock)", "Standard (Garden)"]
world_type_tree[9 : 9 + 1] = ["Tiny (Sulfur)", "Tiny (Ice)", "Standard (Garden)"]
world_type_tree[10 : 10 + 1] = ["Standard (Ammonia)", "Tiny (Ice)", "Standard (Garden)"]
world_type_tree[11 : 11 + 1] = [
    "Standard (Ammonia)",
    "Asteroid Belt",
    "Standard (Garden)",
]
world_type_tree[12 : 12 + 1] = [
    "Standard (Ammonia)",
    "Asteroid Belt",
    "Standard (Garden)",
]
world_type_tree[13 : 13 + 1] = [
    "Large (Ammonia)",
    "Standard (Ocean)",
    "Standard (Garden)",
]
world_type_tree[14 : 14 + 1] = [
    "Large (Ammonia)",
    "Standard (Ocean)",
    "Standard (Garden)",
]
world_type_tree[15 : 15 + 1] = [
    "Large (Greenhouse)",
    "Standard (Ice)",
    "Standard (Garden)",
]
world_type_tree[16 : 16 + 1] = [
    "Large (Greenhouse)",
    "Standard (Hadean)",
    "Standard (Garden)",
]
world_type_tree[17 : 17 + 1] = ["Large (Chthonian)", "Large (Ocean)", "Large (Garden)"]
world_type_tree[18 : 18 + 1] = ["Large (Chthonian)", "Large (Ice)", "Large (Garden)"]

# Atmosphere
atmospheric_pressure_categories_tree = IntervalTree()
atmospheric_pressure_categories_tree[0:0.01] = "Trace"
atmospheric_pressure_categories_tree[0.01 : 0.50 + 0.01] = "Very Thin"
atmospheric_pressure_categories_tree[0.51 : 0.80 + 0.01] = "Thin"
atmospheric_pressure_categories_tree[0.81 : 1.20 + 0.01] = "Standard"
atmospheric_pressure_categories_tree[1.21 : 1.50 + 0.01] = "Dense"
atmospheric_pressure_categories_tree[1.51 : 10 + 0.01] = "Very Dense"
atmospheric_pressure_categories_tree[10.01:100] = "Superdense"

marginal_atmospheres_trees = IntervalTree()
marginal_atmospheres_trees[3 : 4 + 1] = "Chlorine or Flourine"
marginal_atmospheres_trees[5 : 6 + 1] = "Sulfur Compounds"
marginal_atmospheres_trees[7 : 7 + 1] = "Nitrogen Compounds"
marginal_atmospheres_trees[8 : 9 + 1] = "Organic Toxins"
marginal_atmospheres_trees[10 : 11 + 1] = "Low Oxygen"
marginal_atmospheres_trees[12 : 13 + 1] = "Pollutants"
marginal_atmospheres_trees[14 : 14 + 1] = "High Carbon Dioxide"
marginal_atmospheres_trees[15 : 16 + 1] = "High Oxygen"
marginal_atmospheres_trees[17 : 18 + 1] = "Inert Gases"

# World Size
world_density_tree = IntervalTree()
world_density_tree[3 : 6 + 1] = [0.3, 0.6, 0.8]
world_density_tree[7 : 10 + 1] = [0.4, 0.7, 0.9]
world_density_tree[11 : 14 + 1] = [0.5, 0.8, 1.0]
world_density_tree[15 : 17 + 1] = [0.6, 0.9, 1.1]
world_density_tree[18 : 18 + 1] = [0.7, 1.0, 1.2]

# Resources and Habitability
resource_value_tree_asteroid_belts = IntervalTree()
resource_value_tree_asteroid_belts[3 : 3 + 1] = ["Worthless", -5]
resource_value_tree_asteroid_belts[4 : 4 + 1] = ["Very Scant", -4]
resource_value_tree_asteroid_belts[5 : 5 + 1] = ["Scant", -3]
resource_value_tree_asteroid_belts[6 : 7 + 1] = ["Very Poor", -2]
resource_value_tree_asteroid_belts[8 : 9 + 1] = ["Poor", -1]
resource_value_tree_asteroid_belts[10 : 11 + 1] = ["Average", +0]
resource_value_tree_asteroid_belts[12 : 13 + 1] = ["Abundant", +1]
resource_value_tree_asteroid_belts[14 : 15 + 1] = ["Very Abundant", +2]
resource_value_tree_asteroid_belts[16 : 16 + 1] = ["Rich", +3]
resource_value_tree_asteroid_belts[17 : 17 + 1] = ["Very Rich", +4]
resource_value_tree_asteroid_belts[18 : 18 + 1] = ["Motherlode", +5]

resource_value_tree_other_worlds = IntervalTree()
resource_value_tree_other_worlds[0 : 2 + 1] = ["Scant", -3]
resource_value_tree_other_worlds[3 : 4 + 1] = ["Very Poor", -2]
resource_value_tree_other_worlds[5 : 7 + 1] = ["Poor", -1]
resource_value_tree_other_worlds[8 : 13 + 1] = ["Average", +0]
resource_value_tree_other_worlds[14 : 16 + 1] = ["Abundant", +1]
resource_value_tree_other_worlds[17 : 18 + 1] = ["Very Abundant", +2]
resource_value_tree_other_worlds[19 : 100 + 1] = ["Rich", +3]

# Technology Level
tech_level_tree = IntervalTree()
tech_level_tree[3 : 3 + 1] = "Primitive"
tech_level_tree[4 : 4 + 1] = "Standard-3"
tech_level_tree[5 : 5 + 1] = "Standard-2"
tech_level_tree[6 : 7 + 1] = "Standard-1"
tech_level_tree[8 : 11 + 1] = "Standard (Delayed)"
tech_level_tree[12 : 15 + 1] = "Standard"
tech_level_tree[16 : 100 + 1] = "Standard (Advanced)"

# Population
colony_population_tree = IntervalTree()
colony_population_tree[0 : 25 + 1] = 10000
colony_population_tree[26 : 26 + 1] = 13000
colony_population_tree[27 : 27 + 1] = 15000
colony_population_tree[28 : 28 + 1] = 20000
colony_population_tree[29 : 29 + 1] = 25000
colony_population_tree[30 : 30 + 1] = 30000
colony_population_tree[31 : 31 + 1] = 40000
colony_population_tree[32 : 32 + 1] = 50000
colony_population_tree[33 : 33 + 1] = 60000
colony_population_tree[34 : 34 + 1] = 80000
colony_population_tree[35 : 35 + 1] = 100000
colony_population_tree[36 : 36 + 1] = 130000
colony_population_tree[37 : 37 + 1] = 150000
colony_population_tree[38 : 38 + 1] = 200000
colony_population_tree[39 : 39 + 1] = 250000
colony_population_tree[40 : 40 + 1] = 300000
colony_population_tree[41 : 41 + 1] = 400000
colony_population_tree[42 : 42 + 1] = 500000
colony_population_tree[43 : 43 + 1] = 600000
colony_population_tree[44 : 44 + 1] = 800000

colony_population_tree[45 : 45 + 1] = 1000000
colony_population_tree[46 : 46 + 1] = 1300000
colony_population_tree[47 : 47 + 1] = 1500000
colony_population_tree[48 : 48 + 1] = 2000000
colony_population_tree[49 : 49 + 1] = 2500000
colony_population_tree[50 : 50 + 1] = 3000000
colony_population_tree[51 : 51 + 1] = 4000000
colony_population_tree[52 : 52 + 1] = 5000000
colony_population_tree[53 : 53 + 1] = 6000000
colony_population_tree[54 : 54 + 1] = 8000000
colony_population_tree[55 : 55 + 1] = 10000000
colony_population_tree[56 : 56 + 1] = 13000000
colony_population_tree[57 : 57 + 1] = 15000000
colony_population_tree[58 : 58 + 1] = 20000000
colony_population_tree[59 : 59 + 1] = 25000000
colony_population_tree[60 : 60 + 1] = 30000000
colony_population_tree[61 : 61 + 1] = 40000000
colony_population_tree[62 : 62 + 1] = 50000000
colony_population_tree[63 : 63 + 1] = 60000000
colony_population_tree[64 : 64 + 1] = 80000000

colony_population_tree[65 : 65 + 1] = 100000000
colony_population_tree[66 : 66 + 1] = 130000000
colony_population_tree[67 : 67 + 1] = 150000000
colony_population_tree[68 : 68 + 1] = 200000000
colony_population_tree[69 : 69 + 1] = 250000000
colony_population_tree[70 : 70 + 1] = 300000000
colony_population_tree[71 : 71 + 1] = 400000000
colony_population_tree[72 : 72 + 1] = 500000000
colony_population_tree[73 : 73 + 1] = 600000000
colony_population_tree[74 : 74 + 1] = 800000000
colony_population_tree[75 : 75 + 1] = 1000000000
colony_population_tree[76 : 76 + 1] = 1300000000
colony_population_tree[77 : 77 + 1] = 1500000000
colony_population_tree[78 : 78 + 1] = 2000000000
colony_population_tree[79 : 79 + 1] = 2500000000
colony_population_tree[80 : 80 + 1] = 3000000000
colony_population_tree[81 : 81 + 1] = 4000000000
colony_population_tree[82 : 82 + 1] = 5000000000
colony_population_tree[83 : 83 + 1] = 6000000000

outpost_population_tree = IntervalTree()
outpost_population_tree[3 : 3 + 1] = 100
outpost_population_tree[4 : 4 + 1] = 150
outpost_population_tree[5 : 5 + 1] = 250
outpost_population_tree[6 : 6 + 1] = 400
outpost_population_tree[7 : 7 + 1] = 600
outpost_population_tree[8 : 8 + 1] = 1000
outpost_population_tree[9 : 9 + 1] = 1500
outpost_population_tree[10 : 10 + 1] = 2500
outpost_population_tree[11 : 11 + 1] = 4000
outpost_population_tree[12 : 12 + 1] = 6000
outpost_population_tree[13 : 13 + 1] = 10000
outpost_population_tree[14 : 14 + 1] = 15000
outpost_population_tree[15 : 15 + 1] = 25000
outpost_population_tree[16 : 16 + 1] = 40000
outpost_population_tree[17 : 17 + 1] = 60000
outpost_population_tree[18 : 19 + 1] = 100000

# Society Type
world_unity_tree = IntervalTree()
world_unity_tree[0 : 5 + 1] = "Diffuse"
world_unity_tree[6 : 6 + 1] = "Factionalized"
world_unity_tree[7 : 7 + 1] = "Coalition"
world_unity_tree[8 : 8 + 1] = "World Government (Special Condition)"
world_unity_tree[9 : 100 + 1] = "World Government"

special_conditions_tree = IntervalTree()
special_conditions_tree[3 : 5 + 1] = "Subjugated"
special_conditions_tree[6 : 6 + 1] = "Sanctuary"
special_conditions_tree[7 : 8 + 1] = "Military Government"
special_conditions_tree[9 : 9 + 1] = "Socialist"
special_conditions_tree[10 : 10 + 1] = "Bureaucracy"
special_conditions_tree[11 : 12 + 1] = "Colony"
special_conditions_tree[13 : 14 + 1] = "Oligarchy"
special_conditions_tree[15 : 15 + 1] = "Meritocracy"
special_conditions_tree[16 : 16 + 1] = "Matriarchy/Patriacry"
special_conditions_tree[17 : 17 + 1] = "Utopia"
special_conditions_tree[18 : 18 + 1] = "Cybercracy"

society_types_tree = IntervalTree()
society_types_tree[3 : 6 + 1] = ["Anarchy", "Anarchy", "Anarchy", "Anarchy"]
society_types_tree[7 : 8 + 1] = [
    "Clan/Tribal",
    "Clan/Tribal",
    "Clan/Tribal",
    "Clan/Tribal",
]
society_types_tree[9 : 9 + 1] = ["Caste", "Caste", "Caste", "Caste"]
society_types_tree[10 : 10 + 1] = ["Feudal", "Feudal", "Theocracy", "Feudal"]
society_types_tree[11 : 11 + 1] = ["Feudal", "Theocracy", "Feudal", "Feudal"]
society_types_tree[12 : 12 + 1] = ["Theocracy", "Dictatorship", "Feudal", "Feudal"]
society_types_tree[13 : 13 + 1] = [
    "Dictatorship",
    "Dictatorship",
    "Dictatorship",
    "Theocracy",
]
society_types_tree[14 : 14 + 1] = [
    "Dictatorship",
    "Dictatorship",
    "Dictatorship",
    "Dictatorship",
]
society_types_tree[15 : 15 + 1] = [
    "Dictatorship",
    "Representative Democracy",
    "Dictatorship",
    "Dictatorship",
]
society_types_tree[16 : 16 + 1] = [
    "Representative Democracy",
    "Representative Democracy",
    "Representative Democracy",
    "Dictatorship",
]
society_types_tree[17 : 17 + 1] = [
    "Representative Democracy",
    "Representative Democracy",
    "Representative Democracy",
    "Dictatorship",
]
society_types_tree[18 : 18 + 1] = [
    "Representative Democracy",
    "Representative Democracy",
    "Athenian Democracy",
    "Representative Democracy",
]
society_types_tree[19 : 19 + 1] = [
    "Athenian Democracy",
    "Representative Democracy",
    "Corporate State",
    "Representative Democracy",
]
society_types_tree[20 : 20 + 1] = [
    "Athenian Democracy",
    "Athenian Democracy",
    "Corporate State",
    "Corporate State",
]
society_types_tree[21 : 21 + 1] = [
    "Corporate State",
    "Athenian Democracy",
    "Corporate State",
    "Corporate State",
]
society_types_tree[22 : 22 + 1] = [
    "Corporate State",
    "Athenian Democracy",
    "Technocracy",
    "Corporate State",
]
society_types_tree[23 : 23 + 1] = [
    "Technocracy",
    "Corporate State",
    "Technocracy",
    "Technocracy",
]
society_types_tree[24 : 25 + 1] = [
    "Technocracy",
    "Technocracy",
    "Technocracy",
    "Technocracy",
]
society_types_tree[26 : 27 + 1] = ["Caste", "Caste", "Caste", "Caste"]
society_types_tree[28 : 100 + 1] = ["Anarchy", "Anarchy", "Anarchy", "Anarchy"]
