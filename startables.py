from intervaltree import Interval, IntervalTree

# Step 15: Number of Stars
# modifiers: +3 if system is located within an open cluster
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
stellar_evolution_table = IntervalTree()
stellar_evolution_table[0.08:0.13] = ["M7", 3100, 0.0012, None, None, None, None]
stellar_evolution_table[0.13:0.18] = ["M6", 3200, 0.0036, None, None, None, None]
stellar_evolution_table[0.18:0.23] = ["M5", 3200, 0.0079, None, None, None, None]
stellar_evolution_table[0.23:0.28] = ["M4", 3300, 0.015, None, None, None, None]
stellar_evolution_table[0.28:0.33] = ["M4", 3300, 0.024, None, None, None, None]
stellar_evolution_table[0.33:0.38] = ["M3", 3400, 0.037, None, None, None, None]
stellar_evolution_table[0.38:0.43] = ["M2", 3500, 0.054, None, None, None, None]
stellar_evolution_table[0.43:0.48] = ["M1", 3600, 0.07, 0.08, 70, None, None]
stellar_evolution_table[0.48:0.53] = ["M0", 3800, 0.09, 0.11, 59, None, None]
stellar_evolution_table[0.53:0.58] = ["K8", 4000, 0.11, 0.15, 50, None, None]
stellar_evolution_table[0.58:0.63] = ["K6", 4200, 0.13, 0.20, 42, None, None]
stellar_evolution_table[0.63:0.68] = ["K5", 4400, 0.15, 0.25, 37, None, None]
stellar_evolution_table[0.68:0.73] = ["K4", 4600, 0.19, 0.35, 30, None, None]
stellar_evolution_table[0.73:0.78] = ["K2", 4900, 0.23, 0.48, 24, None, None]
stellar_evolution_table[0.78:0.83] = ["K0", 5200, 0.28, 0.65, 20, None, None]
stellar_evolution_table[0.83:0.88] = ["G8", 5400, 0.36, 0.84, 17, None, None]
stellar_evolution_table[0.88:0.93] = ["G6", 5500, 0.45, 1.0, 14, None, None]
stellar_evolution_table[0.93:0.98] = ["G4", 5700, 0.56, 1.3, 12, 1.8, 1.1]
stellar_evolution_table[0.98:1.03] = ["G2", 5800, 0.68, 1.6, 10, 1.6, 1.0]
stellar_evolution_table[1.03:1.08] = ["G1", 5900, 0.87, 1.9, 8.8, 1.4, 0.8]
stellar_evolution_table[1.08:1.13] = ["G0", 6000, 1.1, 2.2, 7.7, 1.2, 0.7]
stellar_evolution_table[1.13:1.18] = ["F9", 6100, 1.4, 2.6, 6.7, 1.0, 0.6]
stellar_evolution_table[1.18:1.23] = ["F8", 6300, 1.7, 3.0, 5.9, 0.9, 0.6]
stellar_evolution_table[1.23:1.28] = ["F7", 6400, 2.1, 3.5, 5.2, 0.8, 0.5]
stellar_evolution_table[1.28:1.33] = ["F6", 6500, 2.5, 3.9, 4.6, 0.7, 0.4]
stellar_evolution_table[1.33:1.38] = ["F5", 6600, 3.1, 4.5, 4.1, 0.6, 0.4]
stellar_evolution_table[1.38:1.43] = ["F4", 6700, 3.7, 5.1, 3.7, 0.6, 0.4]
stellar_evolution_table[1.43:1.48] = ["F3", 6900, 4.3, 5.7, 3.3, 0.5, 0.3]
stellar_evolution_table[1.48:1.55] = ["F2", 7000, 5.1, 6.5, 3.0, 0.5, 0.3]
stellar_evolution_table[1.55:1.65] = ["F0", 7300, 6.7, 8.2, 2.5, 0.4, 0.2]
stellar_evolution_table[1.65:1.75] = ["A9", 7500, 8.6, 10, 2.1, 0.3, 0.2]
stellar_evolution_table[1.75:1.85] = ["A7", 7800, 11, 13, 1.8, 0.3, 0.2]
stellar_evolution_table[1.85:1.95] = ["A6", 8000, 13, 16, 1.5, 0.2, 0.1]
stellar_evolution_table[1.95:2.05] = ["A5", 8200, 16, 20, 1.3, 0.2, 0.1]

# Step 19:  Companion Star Orbits

