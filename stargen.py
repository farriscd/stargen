import argparse
import random
import startables as st
from intervaltree import Interval, IntervalTree
# todo: most of these calculations are done without assuming the system contains a garden world


# todo: seed argument always taken as string and interpreted as string by random.seed
parser = argparse.ArgumentParser()
#parser.add_argument("-a", "--advanced", action="count", help="enable advanced system generation")
parser.add_argument("-s", "--seed", help="seed to be used for random number generation")
args = parser.parse_args()

random.seed(a=args.seed)
sample = {}

# method to generate random numbers as a 6 sided die roll
def roll_dice(number_of_dice=1, modifier=0):
    sum_of_dice = 0
    for _ in range(number_of_dice):
        sum_of_dice += random.randrange(1, 6+1)
    return sum_of_dice + modifier

# manages intervaltree module to roll and lookup tables from startables module
def look_up(table, number_of_dice=1, modifier=0):
    return sorted(table[roll_dice(number_of_dice, modifier)])[0].data

def look_up_value(table, value):
    return sorted(table[value])[0].data

# Calculate number of stars
sample["Number of Stars"] = look_up(st.multiple_stars_table, 3)
sample["Stellar Mass(es)"] = []

# Calculate stellar masses
# todo: this is not how GURPs generates companion masses, the way they do it is more complicated and results
# in companion stars of generally much lower stellar masses
for _ in range(sample["Number of Stars"]):
    sample["Stellar Mass(es)"].append(round(look_up(look_up(st.stellar_mass_table_first_roll, 3), 3)+random.uniform(-0.03,0.03),3))
    sample["Stellar Mass(es)"].sort(reverse=True)
    if min(sample["Stellar Mass(es)"]) < 0.08:
        sample["Stellar Mass(es)"][sample["Stellar Mass(es)"].index(min(sample["Stellar Mass(es)"]))] = 0.08

# Calculate stellar age
temp = look_up(st.stellar_age_table, 3)
sample["Star System Age"] = round((temp[0] + temp[1]*roll_dice(1,-1) + temp[2]*roll_dice(1,-1)), 3)
temp = None

sample["Star Type(s)"] = []
sample["Star Sequence(s)"] = []
sample["Star Effective Temperature(s)"] = []
sample["Star Current Luminosity"] = []
# Calculate stellar characteristics
for i in range(sample["Number of Stars"]):
    temp = look_up_value(st.stellar_evolution_table, sample["Stellar Mass(es)"][i])
    sample["Star Type(s)"].append(temp[0])
    if temp[4] and sample["Star System Age"] <= temp[4] or not temp[4]:
        sample["Star Sequence(s)"].append("V")
    elif temp[4] and temp[5] and sample["Star System Age"] > temp[4] and sample["Star System Age"] <= temp[4]+temp[5]:
        sample["Star Sequence(s)"].append("IV")
    elif temp[4] and temp[5] and temp[6] and sample["Star System Age"] > temp[4]+temp[5] and sample["Star System Age"] <= temp[4]+temp[5]+temp[6]:
        sample["Star Sequence(s)"].append("III")
    else:
        sample["Star Sequence(s)"].append("D")
    temp = None
    
    

print(sample)
