"""
This module contains the Classes and Methods for randomly generating star systems
according to the GURPS Space 4th edition system.

Todo:
    * Finish generation of planetary details
    * Finish documentation, general code maintenance/cleanup
    * Find a cleaner way to print the star, planet, and system information
    * Complete generation of distant companion subcompanions and make sure trinary star
    systems adhere to the suggested guidelines
    * Current calculate_first_orbit allow orbits to fall within forbidden zones
    * Nothing for placing a pre-designed world, not sure if that is a feature or add 
    or not, something that would use the guarantee_garden_world check
    * White Dwarf stars are currently given "None" as temperature since GURPS provides
    no way to calculate it, although it claims to be able to be "quite high"
    * Find someway to fudge all the numbers after calculations have been made to add 
    variance, GURPS has suggestions for variance in corresponding tables
"""

import math
import random
from intervaltree import Interval, IntervalTree
from typing import Any, Union, Optional, List

from . import startables as st

def roll_dice(number_of_dice: int=1, modifier: int=0) -> int:
    """Return the result of a simulated 6-sided die roll

    Args:
        number_of_dice: The number of die to be rolled
        modifier: A number to be added/subtracted to the sum of the die roll
    """
    sum_of_dice = 0
    for _ in range(number_of_dice):
        sum_of_dice += random.randrange(1, 6+1)
    return sum_of_dice + modifier

def look_up(table: IntervalTree, point: Union[float, int]) -> Any:
    """Return data from interval tree at point

    Args:
        table: The interval tree containing data to lookup
        point: The point within range that the data is stored
    """
    return sorted(table[point])[0].data

class Star(object):
    """
    The Star object contains data generated randomy or by provided mass and age

    Args:
        mass: mass measured in solar masses
        age: age measured in billions of years
        guarantee_garden_world: whether or not a garden world is mandatory

    Attributes:
        mass (float): mass measured in solar masses
        age (float): age measured in billions of years
        type (str or NoneType): most probable spectral type
        sequence (str): luminosity class of the star; "III", "IV", "V", and "D"
        temperature (float or NoneType): effective temperature measured in kelvins
        luminosity (float): total energy output measured in solar luminosities
        radius (float or NoneType): radius measured in astronomical units
        inner_limit_radius (float): radius for planetary formation in astronomical units
        outer_limit_radius (float): radius for planetary formation in astronomical units
        snow_line_radius(float): radius for planetary formation in astronomical units
    """
    
    def __init__(self, mass: Optional[float], age: Optional[float], guarantee_garden_world: bool=False) -> None:
        self.mass = mass if mass else self.calculate_stellar_mass(guarantee_garden_world)
        self.age = age if age else self.calculate_stellar_age(guarantee_garden_world)
        self.guarantee_garden_world = guarantee_garden_world

        self.type = self.calculate_stellar_type(self.mass)
        self.sequence = self.calculate_stellar_sequence(self.mass, self.age)
        self.temperature = self.calculate_stellar_temperature(self.mass, self.age, self.sequence)
        self.luminosity = self.calculate_stellar_luminosity(self.mass, self.age, self.sequence)
        self.radius = self.calculate_stellar_radius(self.temperature, self.luminosity)

        self.inner_limit_radius = self.calculate_inner_limit_radius(self.mass, self.luminosity)
        self.outer_limit_radius = self.calculate_outer_limit_radius(self.mass)
        self.snow_line_radius = self.calculate_snow_line_radius(look_up(st.stellar_evolution_table, self.mass)[2])

        self.readjust_stellar_characteristics(self.sequence, self.temperature)

    def calculate_stellar_mass(self, guarantee_garden_world: bool) -> float:
        """Return a randomly generated star mass"""
        if guarantee_garden_world:
            return look_up(look_up(st.stellar_mass_table_first_roll_garden_world, roll_dice(1)), roll_dice(3))
        else:
            return look_up(look_up(st.stellar_mass_table_first_roll, roll_dice(3)), roll_dice(3))

    def calculate_stellar_age(self, guarantee_garden_world: bool) -> float:
        """Return a randomly generated system age""" 
        base_age, step_a, step_b = look_up(st.stellar_age_table, roll_dice(2,2) if guarantee_garden_world else roll_dice(3))
        return (base_age + step_a*roll_dice(1,-1) + step_b*roll_dice(1,-1))

    def calculate_stellar_type(self, mass: float) -> Optional[str]:
        """Return a spectral type based on mass of the star"""
        return look_up(st.stellar_evolution_table, mass)[0]

    def calculate_stellar_sequence(self, mass: float, age: float) -> str:
        """Return a luminosity class based on mass and age of star"""
        *_,m_span,s_span,g_span = look_up(st.stellar_evolution_table, mass)
        if s_span is None:
            return "V"
        elif age > m_span+s_span+g_span:
            return "D"
        elif age > m_span+s_span:
            return "III"
        elif age > m_span:
            return "IV"
        else:
            return "V"
            
    def calculate_stellar_temperature(self, mass: float, age: float, sequence: str) -> Optional[float]:
        """Return an effective temperature based on mass, age, and sequence"""
        _,temp,_,_,m_span,s_span,_ = look_up(st.stellar_evolution_table, mass)
        if sequence == "V":
            return temp
        elif sequence == "IV":
            return temp-(((age-m_span)/s_span)*(temp-4800))
        elif sequence == "III":
            return 3000+200*roll_dice(2,-2)
        else:
            return None
    
    def calculate_stellar_luminosity(self, mass: float, age: float, sequence: str) -> float:
        """Return luminosity based on mass, age, and sequence"""
        _,_,l_min,l_max,m_span,*_ = look_up(st.stellar_evolution_table, mass)
        if sequence == "V":
            return l_min+((age/m_span)*(l_max-l_min)) if l_max else l_min
        elif sequence == "IV":
            return l_max
        elif sequence == "III":
            return l_max*25
        else:
            return 0.001

    def calculate_stellar_radius(self, temperature: Optional[float], luminosity: float) -> Optional[float]:
        """Return radius based on temperature and luminosity"""
        return (155000*math.sqrt(luminosity))/(math.pow(temperature,2)) if temperature else None

    def calculate_inner_limit_radius(self, mass: float, luminosity: float) -> float:
        """Return a list of inner limit radii corresponding to each star"""
        return max(0.1*mass, 0.01*math.sqrt(luminosity))

    def calculate_outer_limit_radius(self, mass: float) -> float:
        """Return a list of outer limit radii corresponding to each star"""
        return 40.0*mass

    def calculate_snow_line_radius(self, l_min: float) -> float:
        """Return a list of snow line radii corresponding to each star"""
        return 4.85*math.sqrt(l_min)

    def readjust_stellar_characteristics(self, sequence: str, temperature: Optional[float]) -> None:
        """Modifies the type and mass of a non-main sequence star"""
        if sequence == "D":
            self.type = None
            self.mass = 0.9+roll_dice(2,-2)*0.05
        if sequence == "IV":
            self.type = look_up(st.stellar_evolution_table_reverse, temperature)
        if sequence == "III":
            self.type = look_up(st.stellar_evolution_table_reverse, temperature)

    def print_summary(self) -> None:
        """Prints the attributes of the star to console in a human readable format"""
        print(f"Spectral type {self.type} {self.sequence}")
        print(f"mass {self.mass} solar masses")
        print(f"age {self.age} billion years")
        print(f"effective temperature {self.temperature} kelvins")
        print(f"luminosity {self.luminosity} solar luminosities")
        print(f"radius {self.radius} AU")
        print("")
        print(f"inner limit radius {self.inner_limit_radius} AU")
        print(f"snow line radius {self.snow_line_radius} AU")
        print(f"outer limit radius {self.outer_limit_radius} AU")

class CompanionStar(Star):
    """A Star-based object for non-primary stars in multistar systems

    Args:
        designation: number designating which companion this star is
        mass: mass in solar masses
        age: age in billions of years

    Attributes:
        designation (int): number designating which companion this star is
        orbital_separation (list: str, float): a list containing seperation and eccentricity
        semi_major_axis (float): the 'average' radius of orbit
        eccentricity (float): eccentricity of the companion stars orbit
    """

    def __init__(self, designation: int, mass: float, age: float) -> None:
        Star.__init__(self, mass, age)
        self.designation = designation
        self.orbital_separation = self.calculate_orbital_separation(self.designation, self.guarantee_garden_world)
        self.semi_major_axis = self.calculate_semi_major_axis(self.orbital_separation[1])
        self.eccentricity = self.calculate_eccentricity(self.orbital_separation[0])

    def calculate_orbital_separation(self, designation: int, guarantee_garden_world: bool) -> List[Union[str, float]]:
        """Return a list containing the companion star 'Separation' and radius multiplier"""
        return look_up(st.orbital_separation_table, roll_dice(3,6 if designation == 2 else 0 + 4 if guarantee_garden_world else 0))

    def calculate_semi_major_axis(self, radius_multiplier: float) -> float:
        """Return the average orbital radius (or semi-major axis) of a companion star in AU"""
        return roll_dice(2)*radius_multiplier

    def calculate_eccentricity(self, separation: str) -> float:
        """Return the eccentricity for a companion star orbit"""
        return look_up(st.stellar_orbital_eccentricity_table, roll_dice(3, -6 if separation == "Very Close" else -4 if separation == "Close" else -2 if separation == "Moderate" else 0))

    def print_summary(self) -> None:
        """Print the attributes of the companion star in a human readable format"""
        print(f"Companion Star {self.designation}")
        print(f"semi-major axis {self.semi_major_axis} AU")
        print(f"eccentricity {self.eccentricity}")
        print("")
        Star.print_summary(self)

class Planet(object):
    """
    """
    def __init__(self, orbital_radius: float, size: str) -> None:
        self.orbital_radius = orbital_radius
        self.size = size

class GasGiant(Planet):
    """
    """
    def __init__(self, orbital_radius: float, size: str) -> None:
        Planet.__init__(self, orbital_radius, size)

class TerrestrialPlanet(Planet):
    """
    """
    def __init__(self, orbital_radius: float, size: str) -> None:
        Planet.__init__(self, orbital_radius, size)

class StarSystem(object):
    """
    The Star System object generates and contains multiple Star objects

    Args:
        is_in_open_cluster (bool): whether or not the system is found in an open cluster
        guarantee_garden_world (bool): whether or not the system should favor habitable planets

    Attributes:
        is_in_open_cluster (bool): whether or not the system is found in an open cluster
        guarantee_garden_world (bool): whether or not the system should favor habitable plane
        number_of_stars (int): number, currently between 1-3, of stars found in the system
        stars (list: Star): a list containing the Star objects corresponding to system stars
        forbidden_zone (list: float): list of float pairs corresponding to forbidden zones
        gas_giants (list: str): list of gas giant arrangement corresponding to each star in system
        orbits (list): complex list containing stellar objects and corresponding orbital radii
    """

    def __init__(self, is_in_open_cluster: bool=False, guarantee_garden_world: bool=False) -> None:
        self.is_in_open_cluster = is_in_open_cluster
        self.guarantee_garden_world = guarantee_garden_world

        self.number_of_stars = self.calculate_number_of_stars(self.is_in_open_cluster)
        self.stars = self.calculate_stars(self.number_of_stars, self.guarantee_garden_world)

        self.forbidden_zone = self.calculate_forbidden_zone(self.stars)

        self.gas_giants = self.calculate_gas_giants(self.stars, self.forbidden_zone)
        self.orbits = self.calculate_first_orbit(self.stars, self.gas_giants)
        self.orbits =  self.calculate_orbits(self.orbits, self.forbidden_zone)
        self.orbits = self.place_gas_giants(self.orbits, self.gas_giants)
        self.orbits = self.fill_remaining_orbits(self.orbits, self.forbidden_zone)

    def calculate_number_of_stars(self, is_in_open_cluster: bool) -> int:
        """Return a randomly generated number of stars"""
        return look_up(st.multiple_stars_table, roll_dice(3, 3 if is_in_open_cluster else 0))

    def calculate_stars(self, number_of_stars: int, guarantee_garden_world: bool) -> List[Star]:
        """Return a list containing randomly generated Star objects"""
        stars = []
        for designation in range(number_of_stars):
            if designation > 0:
                companion_star_mass_roll = roll_dice(1, -1)
                if companion_star_mass_roll == 0:
                    stars.append(CompanionStar(designation, stars[0].mass, stars[0].age))
                else:
                    mass = stars[0].mass-0.05*roll_dice(companion_star_mass_roll)
                    stars.append(CompanionStar(designation, (mass if mass >= 0.10 else 0.10), stars[0].age))
            else:
                stars.append(Star(None, None, guarantee_garden_world))
        return stars

    def calculate_forbidden_zone(self, stars: List[Star]) -> List[float]:
        """Return a list containing points designating a system forbidden zone"""
        forbidden_zone = []
        for star in stars:
            if type(star) == CompanionStar:
                forbidden_zone.append([((1-star.eccentricity)*star.semi_major_axis)/3, ((1+star.eccentricity)*star.semi_major_axis)*3])
        return forbidden_zone

    def in_forbidden_zone(self, forbidden_zone: List[float], radius: float) -> bool:
        """Return whether or not a given radius falls within a set of forbidden zones"""
        for inner_radius, outer_radius in forbidden_zone:
            if radius >= inner_radius and radius <= outer_radius:
                return True
        return False

    def calculate_gas_giants(self, stars: List[Star], forbidden_zone: List[float]) -> List[str]:
        """Return a list of gas giant arrangement corresponding to each star in system"""
        gas_giants = []
        for star in stars:
            if self.in_forbidden_zone(forbidden_zone, star.snow_line_radius):
                gas_giants.append("No Gas Giant")
                continue
            else:
                gas_giants.append(look_up(st.gas_giant_arrangement_table, roll_dice(3)))
        return gas_giants

    def calculate_first_orbit(self, stars: List[Star], gas_giants: List[str]) -> Any:
        """Return a list containing stars and their corresponding first gas giant orbit"""
        orbits = []
        for i, star in enumerate(stars):
            orbit = [star]
            if gas_giants[i] == "Conventional Gas Giant":
                orbit.append([(1+roll_dice(2,-2)*0.05)*star.snow_line_radius, "Gas Giant"])
            elif gas_giants[i] == "Eccentric Gas Giant":
                orbit.append([(roll_dice(1)*0.125)*star.snow_line_radius, "Gas Giant"])
            elif gas_giants[i] == "Epistellar Gas Giant":
                orbit.append([(1+roll_dice(3)*0.1)*star.inner_limit_radius, "Gas Giant"])
            orbits.append(orbit)
        return orbits

# Man this is just gross looking
    def calculate_orbits(self, orbits: Any, forbidden_zone: List[float]) -> Any:
        """Returns the given 'orbits' object with a systems full orbital radii"""
        for orbit in orbits:
            if len(orbit) > 1:
                temp_radius = orbit[1][0]
            else:
                temp_radius = orbit[0].outer_limit_radius/(1+0.05*roll_dice(1))
                if not self.in_forbidden_zone(forbidden_zone, temp_radius):
                    orbit.append([temp_radius])
            while True:
                if temp_radius/look_up(st.orbital_spacing_table, roll_dice(3)) > temp_radius - 0.15:
                    temp_radius = temp_radius - 0.15
                else:
                    temp_radius = temp_radius/look_up(st.orbital_spacing_table, roll_dice(3))
                if not self.in_forbidden_zone(forbidden_zone, temp_radius) and temp_radius >= orbit[0].inner_limit_radius:
                    orbit.append([temp_radius])
                if temp_radius >= orbit[0].inner_limit_radius:
                    continue
                else:
                    break
            if len(orbit) > 1:
                temp_radius = orbit[1][0]
            else:
                temp_radius = (1+0.05*roll_dice(1))/orbit[0].outer_limit_radius
                if not self.in_forbidden_zone(forbidden_zone, temp_radius):
                    orbit.append([temp_radius])
            while True:
                if temp_radius*look_up(st.orbital_spacing_table, roll_dice(3)) < temp_radius + 0.15:
                    temp_radius = temp_radius + 0.15
                else:
                    temp_radius = temp_radius*look_up(st.orbital_spacing_table, roll_dice(3))
                if not self.in_forbidden_zone(forbidden_zone, temp_radius) and temp_radius <= orbit[0].outer_limit_radius:
                    orbit.append([temp_radius])
                if temp_radius <= orbit[0].outer_limit_radius:
                    continue
                else:
                    break
            if len(orbit) > 1:
                orbit[1:] = sorted(orbit[1:])                
        return orbits

    def place_gas_giants(self, orbits: Any, gas_giants: List[str]) -> Any:
        """Returns the given 'orbits' object with GasGiant objects assigned"""
        for idx, orbit in enumerate(orbits):
            if gas_giants[idx] == "No Gas Giant":
                continue
            for i in range(1, len(orbit)):
                # I am assuming that this is the pre-assigned gas giant and that it is either inside
                #   the snow line or is the first orbit beyond the snow line
                if len(orbit[i]) > 1 and orbit[i][1] == "Gas Giant":
                    orbit[i][1] = GasGiant(orbit[i][0], look_up(st.gas_giant_size_table, roll_dice(3, 4)))
                    continue
                if gas_giants[idx] == "Conventional Gas Giant" and orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 15:
                    orbit[i].append(GasGiant(orbit[i][0], look_up(st.gas_giant_size_table, roll_dice(3))))
                elif gas_giants[idx] == "Eccentric Gas Giant" and ((orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 14) or (orbit[i][0] <= orbit[0].snow_line_radius and roll_dice(3) <= 8)):
                    orbit[i].append(GasGiant(orbit[i][0], look_up(st.gas_giant_size_table, roll_dice(3, 4 if orbit[i][0] <= orbit[0].snow_line_radius else 0))))
                elif gas_giants[idx] == "Epistellar Gas Giant" and ((orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 14) or (orbit[i][0] <= orbit[0].snow_line_radius and roll_dice(3) <= 6)):
                    orbit[i].append(GasGiant(orbit[i][0], look_up(st.gas_giant_size_table, roll_dice(3, 4 if orbit[i][0] <= orbit[0].snow_line_radius else 0))))
        return orbits

    def fill_remaining_orbits(self, orbits: Any, forbidden_zone: List[float]) -> Any:
        """Returns the given 'orbits' object with the remaining radii filled"""
        for orbit in orbits:
            for i in range(1, len(orbit)):
                if len(orbit[i]) > 1:
                    continue
                modifier = 0
                # this should find the closest radii to the inner and outer limit radii
                if orbit[i][0] == min(orbit[1:], key=lambda x:abs(x[0]-orbit[0].inner_limit_radius))[0] or orbit[i][0] == min(orbit[1:], key=lambda x:abs(x[0]-orbit[0].outer_limit_radius))[0]:
                    modifier = modifier - 3
                # this should find if the next orbit is a gas giant
                if i < len(orbit)-1 and len(orbit[i+1]) > 1 and type(orbit[i+1][1]) == GasGiant:
                    modifier = modifier - 6
                # this should find if the previous orbit is a gas giant
                if i > 1 and len(orbit[i-1]) > 1 and type(orbit[i-1][1]) == GasGiant:
                    modifier = modifier - 3
                # this should find the radii closest to the forbidden zone limits
                for zone in forbidden_zone:
                    if orbit[i][0] == min(orbit[1:], key=lambda x:abs(x[0]-zone[0]))[0] or orbit[i][0] == min(orbit[1:], key=lambda x:abs(x[0]-zone[1]))[0]:
                        modifier = modifier -6
                        break
                roll = roll_dice(3, modifier)
                orbit_contents = look_up(st.orbit_contents_table, roll)
                if type(orbit_contents) == list:
                    orbit[i].append(TerrestrialPlanet(orbit[i][0], orbit_contents[1]))
                else:
                    orbit[i].append(orbit_contents)
        return orbits

    def print_summary(self) -> None:
        """Prints the attributes of all system stars in a human readable format"""
        print("")
        print("Primary Star")
        for i in self.stars:
            i.print_summary()
            print("")
        print(f"forbidden zone(s) {self.forbidden_zone}")
        print(f"gas giant arrangement(s) {self.gas_giants}")
        print(f"orbits {self.orbits}")
