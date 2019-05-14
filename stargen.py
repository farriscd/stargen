import argparse
import math
import random
import startables as st
import startables_basic as stb
from intervaltree import Interval, IntervalTree
# todo: most of these calculations are done without assuming the system contains a garden world

def int_or_str(x):
    try:
        return int(x)
    except ValueError:
        return str(x)

# todo: seed argument always taken as string and interpreted as string by random.seed
parser = argparse.ArgumentParser()
#parser.add_argument("-a", "--advanced", action="count", help="enable advanced system generation")
parser.add_argument("-s", "--seed", help="seed to be used for random number generation", type=int_or_str)
args = parser.parse_args()

random.seed(a=args.seed)

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


# class for individual star vs whole system?
class Star():
    def __init__(self, mass=None, age=None):
        self.mass = mass if mass else self.calculate_stellar_mass()
        self.age = age if age else self.calculate_stellar_age()
        self.type = self.calculate_stellar_type(self.mass)
        self.sequence = self.calculate_stellar_sequence(self.mass, self.age)
        self.temperature = self.calculate_stellar_temperature(self.mass, self.age, self.sequence)
        self.luminosity = self.calculate_stellar_luminosity(self.mass, self.age, self.sequence)
        self.radius = self.calculate_stellar_radius(self.temperature, self.luminosity)

        self.readjust_stellar_characteristics(self.sequence, self.temperature)

    def calculate_stellar_mass(self):
        return look_up(look_up(st.stellar_mass_table_first_roll, 3), 3)

    def calculate_stellar_age(self):
        temp = look_up(st.stellar_age_table, 3)
        return round((temp[0] + temp[1]*roll_dice(1,-1) + temp[2]*roll_dice(1,-1)), 3)

    def calculate_stellar_type(self, mass):
        return look_up_value(st.stellar_evolution_table, mass)[0]

    def calculate_stellar_sequence(self, mass, age):
        temp = look_up_value(st.stellar_evolution_table, mass)
        if temp[5] is None:
            return "V"
        elif age > temp[4]+temp[5]+temp[6]:
            return "D"
        elif age > temp[4]+temp[5]:
            return "III"
        elif age > temp[4]:
            return "IV"
        else:
            return "V"
            
    def calculate_stellar_temperature(self, mass, age, sequence):
        temp = look_up_value(st.stellar_evolution_table, mass)
        if sequence == "V":
            return temp[1]
        elif sequence == "IV":
            return temp[1]-(((age-temp[4])/temp[5])*(temp[1]-4800))
        elif sequence == "III":
            return 3000+200*roll_dice(2,-2)
        else:
            return None
    
    def calculate_stellar_luminosity(self, mass, age, sequence):
        temp = look_up_value(st.stellar_evolution_table, mass)
        if sequence == "V":
            return round(temp[2]+((age/temp[4])*(temp[3]-temp[2])),4) if temp[3] else temp[2]
        elif sequence == "IV":
            return temp[3]
        elif sequence == "III":
            return temp[3]*25
        else:
            return 0.001

    def calculate_stellar_radius(self, temperature, luminosity):
        return round((155000*math.sqrt(luminosity))/(math.pow(temperature,2)),4) if temperature else None

    # this is to adjust the stellar type and other stats if they are non main sequence
    def readjust_stellar_characteristics(self, sequence, temperature):
        if sequence == "D":
            self.type = None
            self.mass = round(0.9+roll_dice(2,-2)*0.05,4)
        if sequence == "IV":
            self.type = look_up_value(st.stellar_evolution_table_reverse, temperature)
        if sequence == "III":
            self.type = look_up_value(st.stellar_evolution_table_reverse, temperature)


if __name__ == "__main__":
    test = Star()
    print("Spectral type {0} {1}".format(test.type, test.sequence))
    print("mass {} solar masses".format(test.mass))
    print("age {} billion years".format(test.age))
    print("effective temperature {} kelvin".format(test.temperature))
    print("luminosity {} solar luminosities".format(test.luminosity))
    print("radius {} AU".format(test.radius))