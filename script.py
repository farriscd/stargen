import argparse
import random
from typing import Union

from stargen import generator

def int_or_str(x: str) -> Union[int, str]:
    """Return argument as integer or string"""
    try:
        return int(x)
    except ValueError:
        return str(x)

parser = argparse.ArgumentParser()
#parser.add_argument("-a", "--advanced", action="count", help="enable advanced system generation")
parser.add_argument("-s", "--seed", help="seed to be used for random number generation", type=int_or_str)
args = parser.parse_args()
random.seed(a=args.seed)

if __name__ == "__main__":
    test_system = generator.StarSystem()
    print("done")
    """
    for orbits in test_system.orbits:
        offset = 0
        for orbit in orbits:
            if type(orbit) == generator.CompanionStar:
                offset = orbit.semi_major_axis
                print([offset, ("" if orbit.type is None else orbit.type) + " " + orbit.sequence])
            elif type(orbit) == generator.Star:
                print([0.0, ("" if orbit.type is None else orbit.type) + " " + orbit.sequence])
            elif isinstance(orbit[1], generator.Planet):
                print([orbit[1].semi_major_axis+offset, orbit[1].type, orbit[1].moons, [ x.type for x in orbit[1].major_moons]])
            else:
                print([orbit[0]+offset, orbit[1]])
    """