from intervaltree import Interval, IntervalTree
# because the tables being convert to code were written inclusively, and python
# treating interval exclusively, ranges will be written as start:(inclusive stop)+1
# except where noted


# todo: consider removing 'stellar' description from trees, rename whole
#file 'stellar' or keep 'star' tables and have a seperate file for
#planet/orbiting body tables/trees

# Step 15: Number of Stars
multiple_stars_table = IntervalTree()
multiple_stars_table[3:10+1] = 1
multiple_stars_table[11:15+1] = 2
multiple_stars_table[16:30] = 3

# Step 16: Star Masses
# first roll 3
stellar_mass_table_first_roll_3_second_roll = IntervalTree()
stellar_mass_table_first_roll_3_second_roll[3:10+1] = 2.00
stellar_mass_table_first_roll_3_second_roll[11:18+1] = 1.90
# first roll 4
stellar_mass_table_first_roll_4_second_roll = IntervalTree()
stellar_mass_table_first_roll_4_second_roll[3:8+1] = 1.80
stellar_mass_table_first_roll_4_second_roll[9:11+1] = 1.70
stellar_mass_table_first_roll_4_second_roll[12:18+1] = 1.60
# first roll 5
stellar_mass_table_first_roll_5_second_roll = IntervalTree()
stellar_mass_table_first_roll_5_second_roll[3:7+1] = 1.50
stellar_mass_table_first_roll_5_second_roll[8:10+1] = 1.45
stellar_mass_table_first_roll_5_second_roll[11:12+1] = 1.40
stellar_mass_table_first_roll_5_second_roll[13:18+1] = 1.35
# first roll 6
stellar_mass_table_first_roll_6_second_roll = IntervalTree()
stellar_mass_table_first_roll_6_second_roll[3:7+1] = 1.30
stellar_mass_table_first_roll_6_second_roll[8:9+1] = 1.25
stellar_mass_table_first_roll_6_second_roll[10:10+1] = 1.20
stellar_mass_table_first_roll_6_second_roll[11:12+1] = 1.15
stellar_mass_table_first_roll_6_second_roll[13:18+1] = 1.10
# first roll 7
stellar_mass_table_first_roll_7_second_roll = IntervalTree()
stellar_mass_table_first_roll_7_second_roll[3:7+1] = 1.05
stellar_mass_table_first_roll_7_second_roll[8:9+1] = 1.00
stellar_mass_table_first_roll_7_second_roll[10:10+1] = 0.95
stellar_mass_table_first_roll_7_second_roll[11:12+1] = 0.90
stellar_mass_table_first_roll_7_second_roll[13:18+1] = 0.85
# first roll 8
stellar_mass_table_first_roll_8_second_roll = IntervalTree()
stellar_mass_table_first_roll_8_second_roll[3:7+1] = 0.80
stellar_mass_table_first_roll_8_second_roll[8:9+1] = 0.75
stellar_mass_table_first_roll_8_second_roll[10:10+1] = 0.70
stellar_mass_table_first_roll_8_second_roll[11:12+1] = 0.65
stellar_mass_table_first_roll_8_second_roll[13:18+1] = 0.60
# first roll 9
stellar_mass_table_first_roll_9_second_roll = IntervalTree()
stellar_mass_table_first_roll_9_second_roll[3:8+1] = 0.55
stellar_mass_table_first_roll_9_second_roll[9:11+1] = 0.50
stellar_mass_table_first_roll_9_second_roll[12:18+1] = 0.45
# first roll 10
stellar_mass_table_first_roll_10_second_roll = IntervalTree()
stellar_mass_table_first_roll_10_second_roll[3:8+1] = 0.40
stellar_mass_table_first_roll_10_second_roll[9:11+1] = 0.35
stellar_mass_table_first_roll_10_second_roll[12:18+1] = 0.30
# first roll 11
stellar_mass_table_first_roll_11_second_roll = IntervalTree()
stellar_mass_table_first_roll_11_second_roll[3:18+1] = 0.25
# first roll 12
stellar_mass_table_first_roll_12_second_roll = IntervalTree()
stellar_mass_table_first_roll_12_second_roll[3:18+1] = 0.20
# first roll 13
stellar_mass_table_first_roll_13_second_roll = IntervalTree()
stellar_mass_table_first_roll_13_second_roll[3:18+1] = 0.15
# first roll 14-18
stellar_mass_table_first_roll_14_second_roll = IntervalTree()
stellar_mass_table_first_roll_14_second_roll[3:18+1] = 0.10
# stellar mass table assignments
stellar_mass_table_first_roll = IntervalTree()
stellar_mass_table_first_roll[3:3+1] = stellar_mass_table_first_roll_3_second_roll
stellar_mass_table_first_roll[4:4+1] = stellar_mass_table_first_roll_4_second_roll
stellar_mass_table_first_roll[5:5+1] = stellar_mass_table_first_roll_5_second_roll
stellar_mass_table_first_roll[6:6+1] = stellar_mass_table_first_roll_6_second_roll
stellar_mass_table_first_roll[7:7+1] = stellar_mass_table_first_roll_7_second_roll
stellar_mass_table_first_roll[8:8+1] = stellar_mass_table_first_roll_8_second_roll
stellar_mass_table_first_roll[9:9+1] = stellar_mass_table_first_roll_9_second_roll
stellar_mass_table_first_roll[10:10+1] = stellar_mass_table_first_roll_10_second_roll
stellar_mass_table_first_roll[11:11+1] = stellar_mass_table_first_roll_11_second_roll
stellar_mass_table_first_roll[12:12+1] = stellar_mass_table_first_roll_12_second_roll
stellar_mass_table_first_roll[13:13+1] = stellar_mass_table_first_roll_13_second_roll
stellar_mass_table_first_roll[14:18+1] = stellar_mass_table_first_roll_14_second_roll
# garden world modified first roll
stellar_mass_table_first_roll_garden_world = IntervalTree()
stellar_mass_table_first_roll_garden_world[1:1+1] = stellar_mass_table_first_roll_5_second_roll
stellar_mass_table_first_roll_garden_world[2:2+1] = stellar_mass_table_first_roll_6_second_roll
stellar_mass_table_first_roll_garden_world[3:4+1] = stellar_mass_table_first_roll_7_second_roll
stellar_mass_table_first_roll_garden_world[5:6+1] = stellar_mass_table_first_roll_8_second_roll

# Step 17: Star System Age
stellar_age_table = IntervalTree()
stellar_age_table[3:3+1] = [0, 0, 0]
stellar_age_table[4:6+1] = [0.1, 0.3, 0.05]
stellar_age_table[7:10+1] = [2, 0.6, 0.1]
stellar_age_table[11:14+1] = [5.6, 0.6, 0.1]
stellar_age_table[15:17+1] = [8, 0.6, 0.1]
stellar_age_table[18:18+1] = [10, 0.6, 0.1]

# Step 18: Stellar Characteristics
# this table has been modified to allow for a range of stellar masses
# might return to [0.10:0.10+0.01] style, but ranges allow for easier
# calculations for multistar systems
stellar_evolution_table = IntervalTree()
stellar_evolution_table[0.10:0.15] = ["M7", 3100.0, 0.0012, None, None, None, None]
stellar_evolution_table[0.15:0.20] = ["M6", 3200.0, 0.0036, None, None, None, None]
stellar_evolution_table[0.20:0.25] = ["M5", 3200.0, 0.0079, None, None, None, None]
stellar_evolution_table[0.25:0.30] = ["M4", 3300.0, 0.015, None, None, None, None]
stellar_evolution_table[0.30:0.35] = ["M4", 3300.0, 0.024, None, None, None, None]
stellar_evolution_table[0.35:0.40] = ["M3", 3400.0, 0.037, None, None, None, None]
stellar_evolution_table[0.40:0.45] = ["M2", 3500.0, 0.054, None, None, None, None]
stellar_evolution_table[0.45:0.50] = ["M1", 3600.0, 0.07, 0.08, 70, None, None]
stellar_evolution_table[0.50:0.55] = ["M0", 3800.0, 0.09, 0.11, 59, None, None]
stellar_evolution_table[0.55:0.60] = ["K8", 4000.0, 0.11, 0.15, 50, None, None]
stellar_evolution_table[0.60:0.65] = ["K6", 4200.0, 0.13, 0.20, 42, None, None]
stellar_evolution_table[0.65:0.70] = ["K5", 4400.0, 0.15, 0.25, 37, None, None]
stellar_evolution_table[0.70:0.75] = ["K4", 4600.0, 0.19, 0.35, 30, None, None]
stellar_evolution_table[0.75:0.80] = ["K2", 4900.0, 0.23, 0.48, 24, None, None]
stellar_evolution_table[0.80:0.85] = ["K0", 5200.0, 0.28, 0.65, 20, None, None]
stellar_evolution_table[0.85:0.90] = ["G8", 5400.0, 0.36, 0.84, 17, None, None]
stellar_evolution_table[0.90:0.95] = ["G6", 5500.0, 0.45, 1.0, 14, None, None]
stellar_evolution_table[0.95:1.00] = ["G4", 5700.0, 0.56, 1.3, 12, 1.8, 1.1]
stellar_evolution_table[1.00:1.05] = ["G2", 5800.0, 0.68, 1.6, 10, 1.6, 1.0]
stellar_evolution_table[1.05:1.10] = ["G1", 5900.0, 0.87, 1.9, 8.8, 1.4, 0.8]
stellar_evolution_table[1.10:1.15] = ["G0", 6000.0, 1.1, 2.2, 7.7, 1.2, 0.7]
stellar_evolution_table[1.15:1.20] = ["F9", 6100.0, 1.4, 2.6, 6.7, 1.0, 0.6]
stellar_evolution_table[1.20:1.25] = ["F8", 6300.0, 1.7, 3.0, 5.9, 0.9, 0.6]
stellar_evolution_table[1.25:1.30] = ["F7", 6400.0, 2.1, 3.5, 5.2, 0.8, 0.5]
stellar_evolution_table[1.30:1.35] = ["F6", 6500.0, 2.5, 3.9, 4.6, 0.7, 0.4]
stellar_evolution_table[1.35:1.40] = ["F5", 6600.0, 3.1, 4.5, 4.1, 0.6, 0.4]
stellar_evolution_table[1.40:1.45] = ["F4", 6700.0, 3.7, 5.1, 3.7, 0.6, 0.4]
stellar_evolution_table[1.45:1.50] = ["F3", 6900.0, 4.3, 5.7, 3.3, 0.5, 0.3]
stellar_evolution_table[1.50:1.60] = ["F2", 7000.0, 5.1, 6.5, 3.0, 0.5, 0.3]
stellar_evolution_table[1.60:1.70] = ["F0", 7300.0, 6.7, 8.2, 2.5, 0.4, 0.2]
stellar_evolution_table[1.70:1.80] = ["A9", 7500.0, 8.6, 10, 2.1, 0.3, 0.2]
stellar_evolution_table[1.80:1.90] = ["A7", 7800.0, 11, 13, 1.8, 0.3, 0.2]
stellar_evolution_table[1.90:2.00] = ["A6", 8000.0, 13, 16, 1.5, 0.2, 0.1]
stellar_evolution_table[2.00:2.10] = ["A5", 8200.0, 16, 20, 1.3, 0.2, 0.1]

stellar_evolution_table_reverse = IntervalTree()
stellar_evolution_table_reverse[0.0:3150.0] = "M7" 
stellar_evolution_table_reverse[3150.0:3200.0] = "M6"
stellar_evolution_table_reverse[3200.0:3250.0] = "M5"
stellar_evolution_table_reverse[3250.0:3350.0] = "M4"
stellar_evolution_table_reverse[3350.0:3450.0] = "M3"
stellar_evolution_table_reverse[3450.0:3550.0] = "M2"
stellar_evolution_table_reverse[3550.0:3650.0] = "M1"
stellar_evolution_table_reverse[3650.0:3900.0] = "M0"
stellar_evolution_table_reverse[3900.0:4100.0] = "K8"
stellar_evolution_table_reverse[4100.0:4300.0] = "K6"
stellar_evolution_table_reverse[4300.0:4500.0] = "K5"
stellar_evolution_table_reverse[4500.0:4700.0] = "K4"
stellar_evolution_table_reverse[4700.0:5050.0] = "K2"
stellar_evolution_table_reverse[5050.0:5300.0] = "K0"
stellar_evolution_table_reverse[5300.0:5450.0] = "G8"
stellar_evolution_table_reverse[5450.0:5600.0] = "G6"
stellar_evolution_table_reverse[5600.0:5750.0] = "G4"
stellar_evolution_table_reverse[5750.0:5850.0] = "G2"
stellar_evolution_table_reverse[5850.0:5950.0] = "G1"
stellar_evolution_table_reverse[5950.0:6050.0] = "G0"
stellar_evolution_table_reverse[6050.0:6200.0] = "F9"
stellar_evolution_table_reverse[6200.0:6350.0] = "F8"
stellar_evolution_table_reverse[6350.0:6450.0] = "F7"
stellar_evolution_table_reverse[6450.0:6550.0] = "F6"
stellar_evolution_table_reverse[6550.0:6650.0] = "F5"
stellar_evolution_table_reverse[6650.0:6800.0] = "F4"
stellar_evolution_table_reverse[6800.0:6950.0] = "F3"
stellar_evolution_table_reverse[6950.0:7150.0] = "F2"
stellar_evolution_table_reverse[7150.0:7400.0] = "F0"
stellar_evolution_table_reverse[7400.0:7650.0] = "A9"
stellar_evolution_table_reverse[7650.0:7900.0] = "A7"
stellar_evolution_table_reverse[7900.0:8100.0] = "A6"
stellar_evolution_table_reverse[8100.0:10000.0] = "A5"

# Step 19:  Companion Star Orbits
orbital_separation_table = IntervalTree()
orbital_separation_table[0:6+1] = ["Very Close", 0.05]
orbital_separation_table[7:9+1] = ["Close", 0.5]
orbital_separation_table[10:11+1] = ["Moderate", 2.0]
orbital_separation_table[12:14+1] = ["Wide", 10.0]
orbital_separation_table[15:100+1] = ["Distant", 50.0]

stellar_orbital_eccentricity_table = IntervalTree()
stellar_orbital_eccentricity_table[-3:3+1] = 0
stellar_orbital_eccentricity_table[4:4+1] = 0.1
stellar_orbital_eccentricity_table[5:5+1] = 0.2
stellar_orbital_eccentricity_table[6:6+1] = 0.3
stellar_orbital_eccentricity_table[7:8+1] = 0.4
stellar_orbital_eccentricity_table[9:11+1] = 0.5
stellar_orbital_eccentricity_table[12:13+1] = 0.6
stellar_orbital_eccentricity_table[14:15+1] = 0.7
stellar_orbital_eccentricity_table[16:16+1] = 0.8
stellar_orbital_eccentricity_table[17:17+1] = 0.9
stellar_orbital_eccentricity_table[18:100+1] = 0.95

# Step 21: Placing First Planets
gas_giant_arrangement_table = IntervalTree()
gas_giant_arrangement_table[0:10+1]= "No Gas Giant"
gas_giant_arrangement_table[11:12+1]= "Conventional Gas Giant"
gas_giant_arrangement_table[13:14+1]= "Eccentric Gas Giant"
gas_giant_arrangement_table[15:18+1]= "Epistellar Gas Giant"

# Step 22: Place Planetary Orbits
orbital_spacing_table = IntervalTree()
orbital_spacing_table[3:4+1] = 1.4
orbital_spacing_table[5:6+1] = 1.5
orbital_spacing_table[7:8+1] = 1.6
orbital_spacing_table[9:12+1] = 1.7
orbital_spacing_table[13:14+1] = 1.8
orbital_spacing_table[15:16+1] = 1.9
orbital_spacing_table[17:18+1] = 2.0

# Step 23: Place Worlds
gas_giant_size_table = IntervalTree()
gas_giant_size_table[3:10+1] = "Small"
gas_giant_size_table[11:16+1] = "Medium"
gas_giant_size_table[17:100+1] = "Large"

orbit_contents_table = IntervalTree()
orbit_contents_table[-100:3+1] = "Empty Orbit"
orbit_contents_table[4:6+1] = "Asteroid Belt"
orbit_contents_table[7:8+1] = ["Terrestrial Planet", "Tiny"]
orbit_contents_table[9:11+1] = ["Terrestrial Planet", "Small"]
orbit_contents_table[12:15+1] = ["Terrestrial Planet", "Standard"]
orbit_contents_table[16:100+1] = ["Terrestrial Planet", "Large"]

# Stepd 24: Place Moons
moon_size_table = IntervalTree()
moon_size_table[0:11+1] = "Three size classes smaller"
moon_size_table[12:14+1] = "Two size classes smaller"
moon_size_table[15:100+1] = "One size classes smaller"