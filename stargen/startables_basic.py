"""
GURPS Space 4th Edition Basic Worldbuilding tables

This module contains some the applicable tables from the Generating Star Systems
section of the Basic Worldbuilding system.

These tables are currently just transcribed but not used by any methods.

Atmospheric Pressure Categories to allow ranges of values.

Todo:
    * Implement any of this stuff
"""

from intervaltree import Interval, IntervalTree

# Step 2: World Type
overall_type_table = IntervalTree()
overall_type_table[3 : 7 + 1] = "Hostile"
overall_type_table[8 : 13 + 1] = "Barren"
overall_type_table[14 : 18 + 1] = "Garden"

world_type_table = IntervalTree()
world_type_table[3 : 3 + 1] = [
    "Standard (Chthonian)",
    "Small (Hadean)",
    "Standard (Garden)",
]
world_type_table[4 : 4 + 1] = [
    "Standard (Chthonian)",
    "Small (Ice)",
    "Standard (Garden)",
]
world_type_table[5 : 5 + 1] = [
    "Standard (Greenhouse)",
    "Small (Rock)",
    "Standard (Garden)",
]
world_type_table[6 : 6 + 1] = [
    "Standard (Greenhouse)",
    "Small (Rock)",
    "Standard (Garden)",
]
world_type_table[7 : 7 + 1] = ["Tiny (Sulfur)", "Tiny (Rock)", "Standard (Garden)"]
world_type_table[8 : 8 + 1] = ["Tiny (Sulfur)", "Tiny (Rock)", "Standard (Garden)"]
world_type_table[9 : 9 + 1] = ["Tiny (Sulfur)", "Tiny (Ice)", "Standard (Garden)"]
world_type_table[10 : 10 + 1] = [
    "Standard (Ammonia)",
    "Tiny (Ice)",
    "Standard (Garden)",
]
world_type_table[11 : 11 + 1] = [
    "Standard (Ammonia)",
    "Asteroid Belt",
    "Standard (Garden)",
]
world_type_table[12 : 12 + 1] = [
    "Standard (Ammonia)",
    "Asteroid Belt",
    "Standard (Garden)",
]
world_type_table[13 : 13 + 1] = [
    "Large (Ammonia)",
    "Standard (Ocean)",
    "Standard (Garden)",
]
world_type_table[14 : 14 + 1] = [
    "Large (Ammonia)",
    "Standard (Ocean)",
    "Standard (Garden)",
]
world_type_table[15 : 15 + 1] = [
    "Large (Greenhouse)",
    "Standard (Ice)",
    "Standard (Garden)",
]
world_type_table[16 : 16 + 1] = [
    "Large (Greenhouse)",
    "Standard (Hadean)",
    "Standard (Garden)",
]
world_type_table[17 : 17 + 1] = ["Large (Chthonian)", "Large (Ocean)", "Large (Garden)"]
world_type_table[18 : 18 + 1] = ["Large (Chthonian)", "Large (Ice)", "Large (Garden)"]

# Step 3: Atmosphere
atmospheric_pressure_categories_table = IntervalTree()
atmospheric_pressure_categories_table[0:0.01] = "Trace"
atmospheric_pressure_categories_table[0.01 : 0.50 + 0.01] = "Very Thin"
atmospheric_pressure_categories_table[0.51 : 0.80 + 0.01] = "Thin"
atmospheric_pressure_categories_table[0.81 : 1.20 + 0.01] = "Standard"
atmospheric_pressure_categories_table[1.21 : 1.50 + 0.01] = "Dense"
atmospheric_pressure_categories_table[1.51 : 10 + 0.01] = "Very Dense"
atmospheric_pressure_categories_table[10.01:100] = "Superdense"

marginal_atmospheres_tables = IntervalTree()
marginal_atmospheres_tables[3 : 4 + 1] = "Chlorine or Flourine"
marginal_atmospheres_tables[5 : 6 + 1] = "Sulfur Compounds"
marginal_atmospheres_tables[7 : 7 + 1] = "Nitrogen Compounds"
marginal_atmospheres_tables[8 : 9 + 1] = "Organic Toxins"
marginal_atmospheres_tables[10 : 11 + 1] = "Low Oxygen"
marginal_atmospheres_tables[12 : 13 + 1] = "Pollutants"
marginal_atmospheres_tables[14 : 14 + 1] = "High Carbon Dioxide"
marginal_atmospheres_tables[15 : 16 + 1] = "High Oxygen"
marginal_atmospheres_tables[17 : 18 + 1] = "Inert Gases"

# Step 6: World Size
world_density_table = IntervalTree()
world_density_table[3 : 6 + 1] = [0.3, 0.6, 0.8]
world_density_table[7 : 10 + 1] = [0.4, 0.7, 0.9]
world_density_table[11 : 14 + 1] = [0.5, 0.8, 1.0]
world_density_table[15 : 17 + 1] = [0.6, 0.9, 1.1]
world_density_table[18 : 18 + 1] = [0.7, 1.0, 1.2]

# Step 7: Resources and Habitability
resource_value_table_asteroid_belts = IntervalTree()
resource_value_table_asteroid_belts[3 : 3 + 1] = ["Worthless", -5]
resource_value_table_asteroid_belts[4 : 4 + 1] = ["Very Scant", -4]
resource_value_table_asteroid_belts[5 : 5 + 1] = ["Scant", -3]
resource_value_table_asteroid_belts[6 : 7 + 1] = ["Very Poor", -2]
resource_value_table_asteroid_belts[8 : 9 + 1] = ["Poor", -1]
resource_value_table_asteroid_belts[10 : 11 + 1] = ["Average", +0]
resource_value_table_asteroid_belts[12 : 13 + 1] = ["Abundant", +1]
resource_value_table_asteroid_belts[14 : 15 + 1] = ["Very Abundant", +2]
resource_value_table_asteroid_belts[16 : 16 + 1] = ["Rich", +3]
resource_value_table_asteroid_belts[17 : 17 + 1] = ["Very Rich", +4]
resource_value_table_asteroid_belts[18 : 18 + 1] = ["Motherlode", +5]

resource_value_table_other_worlds = IntervalTree()
resource_value_table_other_worlds[0 : 2 + 1] = ["Scant", -3]
resource_value_table_other_worlds[3 : 4 + 1] = ["Very Poor", -2]
resource_value_table_other_worlds[5 : 7 + 1] = ["Poor", -1]
resource_value_table_other_worlds[8 : 13 + 1] = ["Average", +0]
resource_value_table_other_worlds[14 : 16 + 1] = ["Abundant", +1]
resource_value_table_other_worlds[17 : 18 + 1] = ["Very Abundant", +2]
resource_value_table_other_worlds[19 : 100 + 1] = ["Rich", +3]

# Step 9: Technocracylogy Level
tech_level_table = IntervalTree()
tech_level_table[3 : 3 + 1] = "Primitive"
tech_level_table[4 : 4 + 1] = "Standard-3"
tech_level_table[5 : 5 + 1] = "Standard-2"
tech_level_table[6 : 7 + 1] = "Standard-1"
tech_level_table[8 : 11 + 1] = "Standard (Delayed)"
tech_level_table[12 : 15 + 1] = "Standard"
tech_level_table[16 : 100 + 1] = "Standard (Advanced)"


# Step 10: Population
colony_population_table = IntervalTree()
colony_population_table[0 : 25 + 1] = 10000
colony_population_table[26 : 26 + 1] = 13000
colony_population_table[27 : 27 + 1] = 15000
colony_population_table[28 : 28 + 1] = 20000
colony_population_table[29 : 29 + 1] = 25000
colony_population_table[30 : 30 + 1] = 30000
colony_population_table[31 : 31 + 1] = 40000
colony_population_table[32 : 32 + 1] = 50000
colony_population_table[33 : 33 + 1] = 60000
colony_population_table[34 : 34 + 1] = 80000
colony_population_table[35 : 35 + 1] = 100000
colony_population_table[36 : 36 + 1] = 130000
colony_population_table[37 : 37 + 1] = 150000
colony_population_table[38 : 38 + 1] = 200000
colony_population_table[39 : 39 + 1] = 250000
colony_population_table[40 : 40 + 1] = 300000
colony_population_table[41 : 41 + 1] = 400000
colony_population_table[42 : 42 + 1] = 500000
colony_population_table[43 : 43 + 1] = 600000
colony_population_table[44 : 44 + 1] = 800000

colony_population_table[45 : 45 + 1] = 1000000
colony_population_table[46 : 46 + 1] = 1300000
colony_population_table[47 : 47 + 1] = 1500000
colony_population_table[48 : 48 + 1] = 2000000
colony_population_table[49 : 49 + 1] = 2500000
colony_population_table[50 : 50 + 1] = 3000000
colony_population_table[51 : 51 + 1] = 4000000
colony_population_table[52 : 52 + 1] = 5000000
colony_population_table[53 : 53 + 1] = 6000000
colony_population_table[54 : 54 + 1] = 8000000
colony_population_table[55 : 55 + 1] = 10000000
colony_population_table[56 : 56 + 1] = 13000000
colony_population_table[57 : 57 + 1] = 15000000
colony_population_table[58 : 58 + 1] = 20000000
colony_population_table[59 : 59 + 1] = 25000000
colony_population_table[60 : 60 + 1] = 30000000
colony_population_table[61 : 61 + 1] = 40000000
colony_population_table[62 : 62 + 1] = 50000000
colony_population_table[63 : 63 + 1] = 60000000
colony_population_table[64 : 64 + 1] = 80000000

colony_population_table[65 : 65 + 1] = 100000000
colony_population_table[66 : 66 + 1] = 130000000
colony_population_table[67 : 67 + 1] = 150000000
colony_population_table[68 : 68 + 1] = 200000000
colony_population_table[69 : 69 + 1] = 250000000
colony_population_table[70 : 70 + 1] = 300000000
colony_population_table[71 : 71 + 1] = 400000000
colony_population_table[72 : 72 + 1] = 500000000
colony_population_table[73 : 73 + 1] = 600000000
colony_population_table[74 : 74 + 1] = 800000000
colony_population_table[75 : 75 + 1] = 1000000000
colony_population_table[76 : 76 + 1] = 1300000000
colony_population_table[77 : 77 + 1] = 1500000000
colony_population_table[78 : 78 + 1] = 2000000000
colony_population_table[79 : 79 + 1] = 2500000000
colony_population_table[80 : 80 + 1] = 3000000000
colony_population_table[81 : 81 + 1] = 4000000000
colony_population_table[82 : 82 + 1] = 5000000000
colony_population_table[83 : 83 + 1] = 6000000000

outpost_population_table = IntervalTree()
outpost_population_table[3 : 3 + 1] = 100
outpost_population_table[4 : 4 + 1] = 150
outpost_population_table[5 : 5 + 1] = 250
outpost_population_table[6 : 6 + 1] = 400
outpost_population_table[7 : 7 + 1] = 600
outpost_population_table[8 : 8 + 1] = 1000
outpost_population_table[9 : 9 + 1] = 1500
outpost_population_table[10 : 10 + 1] = 2500
outpost_population_table[11 : 11 + 1] = 4000
outpost_population_table[12 : 12 + 1] = 6000
outpost_population_table[13 : 13 + 1] = 10000
outpost_population_table[14 : 14 + 1] = 15000
outpost_population_table[15 : 15 + 1] = 25000
outpost_population_table[16 : 16 + 1] = 40000
outpost_population_table[17 : 17 + 1] = 60000
outpost_population_table[18 : 19 + 1] = 100000

# Step 11: Society Type
world_unity_table = IntervalTree()
world_unity_table[0 : 5 + 1] = "Diffuse"
world_unity_table[6 : 6 + 1] = "Factionalized"
world_unity_table[7 : 7 + 1] = "Coalition"
world_unity_table[8 : 8 + 1] = "World Government (Special Condition)"
world_unity_table[9 : 100 + 1] = "World Government"

special_conditions_table = IntervalTree()
special_conditions_table[3 : 5 + 1] = "Subjugated"
special_conditions_table[6 : 6 + 1] = "Sanctuary"
special_conditions_table[7 : 8 + 1] = "Military Government"
special_conditions_table[9 : 9 + 1] = "Socialist"
special_conditions_table[10 : 10 + 1] = "Bureaucracy"
special_conditions_table[11 : 12 + 1] = "Colony"
special_conditions_table[13 : 14 + 1] = "Oligarchy"
special_conditions_table[15 : 15 + 1] = "Meritocracy"
special_conditions_table[16 : 16 + 1] = "Matriarchy/Patriacry"
special_conditions_table[17 : 17 + 1] = "Utopia"
special_conditions_table[18 : 18 + 1] = "Cybercracy"

society_types_table = IntervalTree()
society_types_table[3 : 6 + 1] = ["Anarchy", "Anarchy", "Anarchy", "Anarchy"]
society_types_table[7 : 8 + 1] = [
    "Clan/Tribal",
    "Clan/Tribal",
    "Clan/Tribal",
    "Clan/Tribal",
]
society_types_table[9 : 9 + 1] = ["Caste", "Caste", "Caste", "Caste"]
society_types_table[10 : 10 + 1] = ["Feudal", "Feudal", "Theocracy", "Feudal"]
society_types_table[11 : 11 + 1] = ["Feudal", "Theocracy", "Feudal", "Feudal"]
society_types_table[12 : 12 + 1] = ["Theocracy", "Dictatorship", "Feudal", "Feudal"]
society_types_table[13 : 13 + 1] = [
    "Dictatorship",
    "Dictatorship",
    "Dictatorship",
    "Theocracy",
]
society_types_table[14 : 14 + 1] = [
    "Dictatorship",
    "Dictatorship",
    "Dictatorship",
    "Dictatorship",
]
society_types_table[15 : 15 + 1] = [
    "Dictatorship",
    "Representative Democracy",
    "Dictatorship",
    "Dictatorship",
]
society_types_table[16 : 16 + 1] = [
    "Representative Democracy",
    "Representative Democracy",
    "Representative Democracy",
    "Dictatorship",
]
society_types_table[17 : 17 + 1] = [
    "Representative Democracy",
    "Representative Democracy",
    "Representative Democracy",
    "Dictatorship",
]
society_types_table[18 : 18 + 1] = [
    "Representative Democracy",
    "Representative Democracy",
    "Athenian Democracy",
    "Representative Democracy",
]
society_types_table[19 : 19 + 1] = [
    "Athenian Democracy",
    "Representative Democracy",
    "Corporate State",
    "Representative Democracy",
]
society_types_table[20 : 20 + 1] = [
    "Athenian Democracy",
    "Athenian Democracy",
    "Corporate State",
    "Corporate State",
]
society_types_table[21 : 21 + 1] = [
    "Corporate State",
    "Athenian Democracy",
    "Corporate State",
    "Corporate State",
]
society_types_table[22 : 22 + 1] = [
    "Corporate State",
    "Athenian Democracy",
    "Technocracy",
    "Corporate State",
]
society_types_table[23 : 23 + 1] = [
    "Technocracy",
    "Corporate State",
    "Technocracy",
    "Technocracy",
]
society_types_table[24 : 25 + 1] = [
    "Technocracy",
    "Technocracy",
    "Technocracy",
    "Technocracy",
]
society_types_table[26 : 27 + 1] = ["Caste", "Caste", "Caste", "Caste"]
society_types_table[28 : 100 + 1] = ["Anarchy", "Anarchy", "Anarchy", "Anarchy"]
