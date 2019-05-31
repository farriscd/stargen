"""
This module contains the Classes and Methods for randomly generating star systems
according to the GURPS Space 4th edition system.

Todo:
    * Finish generation of planetary details
    * Refactor World Type Generation for Moons
    * Find a cleaner way to print the star, planet, and system information
    * Still calculating separate orbits for close binary pairs rather than as center of mass
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

from . import startrees as st
from . import worldtrees as wt

size_list = ["Tiny", "Small", "Standard", "Large"]

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

def look_up(tree: IntervalTree, point: Union[float, int]) -> Any:
    """Return data from interval tree at point

    Args:
        tree: The interval tree containing data to lookup
        point: The point within range that the data is stored
    """
    return sorted(tree[point])[0].data

class Star(object):
    """
    The Star object contains data generated randomly or by provided mass and age

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
    
    def __init__(self, mass: Optional[float]=None, age: Optional[float]=None, guarantee_garden_world: bool=False) -> None:
        self.guarantee_garden_world = guarantee_garden_world

        if mass is None:
            mass = self.generate_stellar_mass(self.guarantee_garden_world)
        self.mass = mass

        if age is None:
            age = self.generate_stellar_age(self.guarantee_garden_world)
        self.age = age

        self.sequence = self.calculate_stellar_sequence(self.mass, self.age)
        if self.sequence == "D":
            self.mass = self.white_dwarf_death()

        self.temperature = self.calculate_stellar_temperature(self.mass, self.sequence, self.age)
        self.luminosity = self.calculate_stellar_luminosity(self.mass, self.sequence, self.age)
        self.type = self.calculate_stellar_type(self.sequence, self.mass, self.temperature)
        self.radius = self.calculate_stellar_radius(self.temperature, self.luminosity)

        self.inner_limit_radius = self.calculate_inner_limit_radius(self.mass, self.luminosity)
        self.outer_limit_radius = self.calculate_outer_limit_radius(self.mass)
        self.snow_line_radius = self.calculate_snow_line_radius(self.mass)

    def generate_stellar_mass(self, guarantee_garden_world: bool=False) -> float:
        """Return a randomly generated star mass"""
        if guarantee_garden_world:
            stellar_mass = look_up(look_up(st.stellar_mass_tree_first_roll_garden_world, roll_dice(1)), roll_dice(3))
        else:
            stellar_mass = look_up(look_up(st.stellar_mass_tree_first_roll, roll_dice(3)), roll_dice(3))
        return stellar_mass

    def generate_stellar_age(self, guarantee_garden_world: bool=False) -> float:
        """Return a randomly generated system age"""
        if guarantee_garden_world:
            base_age, step_a, step_b = look_up(st.stellar_age_tree, roll_dice(2,2))
        else:
            base_age, step_a, step_b = look_up(st.stellar_age_tree, roll_dice(3))
        stellar_age = base_age + step_a*roll_dice(1,-1) + step_b*roll_dice(1,-1)
        return stellar_age

    def calculate_stellar_sequence(self, mass: float, age: float) -> str:
        """Return a luminosity class based on mass and age of star"""
        *_,m_span,s_span,g_span = look_up(st.stellar_evolution_tree, mass)
        if s_span is None:
            stellar_sequence = "V"
        elif age > m_span+s_span+g_span:
            stellar_sequence = "D"
        elif age > m_span+s_span:
            stellar_sequence = "III"
        elif age > m_span:
            stellar_sequence = "IV"
        else:
            stellar_sequence = "V"
        return stellar_sequence

    def white_dwarf_death(self) -> float:
        """Modifies the mass of a white dwarf"""
        stellar_mass = 0.9+0.05*roll_dice(2,-2)
        return stellar_mass

    def calculate_stellar_temperature(self, mass: float, sequence: str, age: float) -> Optional[float]:
        """Return an effective temperature based on mass, age, and sequence"""
        _,temp,_,_,m_span,s_span,_ = look_up(st.stellar_evolution_tree, mass)
        if sequence == "V":
            stellar_temperature = temp
        elif sequence == "IV":
            stellar_temperature = temp-(((age-m_span)/s_span)*(temp-4800))
        elif sequence == "III":
            stellar_temperature = 3000+200*roll_dice(2,-2)
        else:
            stellar_temperature = None
        return stellar_temperature
    
    def calculate_stellar_luminosity(self, mass: float, sequence: str, age: float) -> float:
        """Return luminosity based on mass, age, and sequence"""
        _,_,l_min,l_max,m_span,*_ = look_up(st.stellar_evolution_tree, mass)
        if sequence == "V":
            stellar_luminosity = l_min+((age/m_span)*(l_max-l_min)) if l_max else l_min
        elif sequence == "IV":
            stellar_luminosity = l_max
        elif sequence == "III":
            stellar_luminosity = l_max*25
        else:
            stellar_luminosity = 0.001
        return stellar_luminosity

    def calculate_stellar_type(self, sequence: str, mass: float, temperature: float) -> Optional[str]:
        """Return a spectral type based on mass of the star"""
        if sequence == "V":
            stellar_type,*_ = look_up(st.stellar_evolution_tree, mass)
        elif sequence == "IV":
            stellar_type = look_up(st.stellar_evolution_tree_reverse, temperature)
        elif sequence == "III":
            stellar_type = look_up(st.stellar_evolution_tree_reverse, temperature)
        else:
            stellar_type = None
        return stellar_type

    def calculate_stellar_radius(self, temperature: Optional[float], luminosity: float) -> Optional[float]:
        """Return radius based on temperature and luminosity"""
        if temperature is None:
            stellar_radius = None
        else:
            stellar_radius = (155000*math.sqrt(luminosity))/(math.pow(temperature,2))
        return stellar_radius

    def calculate_inner_limit_radius(self, mass: float, luminosity: float) -> float:
        """Return a list of inner limit radii corresponding to each star"""
        inner_limit_radius = max(0.1*mass, 0.01*math.sqrt(luminosity))
        return inner_limit_radius

    def calculate_outer_limit_radius(self, mass: float) -> float:
        """Return a list of outer limit radii corresponding to each star"""
        outer_limit_radius = 40.0*mass
        return outer_limit_radius

    def calculate_snow_line_radius(self, mass: float) -> float:
        """Return a list of snow line radii corresponding to each star"""
        _,_,l_min,*_= look_up(st.stellar_evolution_tree, mass)
        snow_line_radius = 4.85*math.sqrt(l_min)
        return snow_line_radius

class CompanionStar(Star):
    """
    A Star-based object for non-primary stars in multistar systems

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

    def __init__(self, designation: int, mass: float, age: float, guarantee_garden_world: bool) -> None:
        Star.__init__(self, mass, age)
        self.designation = designation
        self.orbital_separation = self.generate_orbital_separation(self.guarantee_garden_world, self.designation)
        self.semi_major_axis = self.generate_semi_major_axis(self.orbital_separation[1])
        self.eccentricity = self.generate_eccentricity(self.orbital_separation[0])

    def generate_orbital_separation(self, guarantee_garden_world: bool, designation: int) -> List[Union[str, float]]:
        """Return a list containing the companion star 'Separation' and radius multiplier"""
        modifier = 0
        if guarantee_garden_world:
            modifier += 4
        if designation == 2:
            modifier += 6
        orbital_separation = look_up(st.orbital_separation_tree, roll_dice(3, modifier))
        return orbital_separation

    def generate_semi_major_axis(self, radius_multiplier: float) -> float:
        """Return the average orbital radius (or semi-major axis) of a companion star in AU"""
        semi_major_axis = roll_dice(2)*radius_multiplier
        return semi_major_axis

    def generate_eccentricity(self, separation: str) -> float:
        """Return the eccentricity for a companion star orbit"""
        if separation == "Very Close":
            modifier = -6
        elif separation == "Close":
            modifier = -4
        elif separation == "Moderate":
            modifier = -2
        else:
            modifier = 0
        eccentricity = look_up(st.stellar_orbital_eccentricity_tree, roll_dice(3, modifier))
        return eccentricity

class Planet(object):
    """
    The Planet object contains randomly generated data based on a given Star

    Args:
        primary_star: The closest Star object around which the planet orbits
        orbit: The average distance between its primary star
        size: The size of the planet

    Attributes:
        relative_orbital_radius (float): The average distance between its primary star
        absolute_orbital_radius (float): The average distance between the system center
        size (str): The size of the planet
        temperature (float): The effective temperature of the planet in Kelvins
        moons (List[int]): The list of counts major moons/moonlets in orbit
        major_moons (List[str or NoneType]): The list of sizes of major moons
        ring_system (str or NoneType): The visibility of any ring system
        type (str or NoneType): The world type
    """
    def __init__(self, primary_star: Star, orbit: float, size: str) -> None:

        self.relative_orbital_radius = orbit
        self.absolute_orbital_radius = orbit + (primary_star.semi_major_axis if type(primary_star) == CompanionStar else 0)
        self.size = size
        self.temperature = self.calculate_temperature(primary_star.luminosity, self.relative_orbital_radius)
        self.moons = None
        self.major_moons = None
        self.ring_system = None
        self.type = None

    def calculate_moon_size(self, moons: List[int], size: str) -> List[str]:
        """Return a list containing the sizes of a planets major moons"""
        major_moons = []
        if moons[1] == 0:
            return major_moons
        else:
            for _ in range(moons[1]):
                major_moons.append(size_list[max(size_list.index(size)+look_up(st.moon_size_tree, roll_dice(3)), 0)])
        return major_moons

    def calculate_temperature(self, luminosity: float, radius: float) -> float:
        """Return the effective temperature of the planet"""
        return (278*luminosity**(1./4))/math.sqrt(radius)

    def calculate_world_type(self, blackbody_temperature: float, size_class: str) -> Union[List[str], str]:
        if size_class == "Tiny":
            return look_up(wt.tiny_world_type_assignment_tree, blackbody_temperature)
        if size_class == "Small":
            return look_up(wt.small_world_type_assignment_tree, blackbody_temperature)
        if size_class == "Standard":
            return look_up(wt.standard_world_type_assignment_tree, blackbody_temperature)
        if size_class == "Large":
            return look_up(wt.large_world_type_assignment_tree, blackbody_temperature)

class GasGiant(Planet):
    """
    """
    def __init__(self, primary_star: Star, orbit: float, size: str) -> None:
        Planet.__init__(self, primary_star, orbit, size)

        self.moons = self.generate_moons(self.relative_orbital_radius)
        self.major_moons = self.calculate_moon_size(self.moons, "Large")
        self.major_moons = self.calculate_moon_type(self.temperature, self.major_moons, primary_star)
        self.ring_system = self.generate_rings(self.moons)
        self.type = size + " Gas Giant"

    def generate_moons(self, orbital_radius: float) -> List[int]:
        """Return a list containing number of moons in each family of satellites"""
        if orbital_radius < 0.1:
            modifiers = [-10, -6, -6]
        elif orbital_radius < 0.5:
            modifiers = [-8, -5, -6]
        elif orbital_radius < 0.75:
            modifiers = [-6, -4, -5]
        elif orbital_radius < 1.5:
            modifiers = [-3, -1, -4]
        elif orbital_radius < 3:
            modifiers = [0, 0, -1]
        else:
            modifiers = [0, 0, 0]
        inner_moonlets = max(roll_dice(2, modifiers[0]), 0)
        major_moons = max(roll_dice(1, modifiers[1]), 0)
        irregular_moonlets = max(roll_dice(1, modifiers[2]), 0)
        return [inner_moonlets, major_moons, irregular_moonlets]

    def generate_rings(self, moons: List[int]) -> str:
        """Return the visibility of a gas giants rings based on moons"""
        if moons[0] >= 10:
            return "High Visibility"
        elif moons[0] >= 6:
            return "Moderate Visibility"
        else:
            return "Low Visibility"

    def calculate_gas_giant_type(self, blackbody_temperature: float, size_class: str, primary_star: Star, sulfur_check: bool) -> str:
        world_type = self.calculate_world_type(blackbody_temperature, size_class)
        if size_class == "Tiny" and type(world_type) == list:
            if sulfur_check:
                return world_type[1]
            else:
                return world_type[0]
        if (size_class == "Standard" or size_class == "Large") and type(world_type) == list:
            if (world_type[0] == "Standard (Ice)" or world_type[0] == "Large (Ice)") and primary_star.mass <= 0.65:
                return world_type[1]
            elif (world_type[0] == "Standard (Ocean)" and roll_dice(3, max(math.floor(primary_star.age/.5), 10)) >= 18) or (world_type[0] == "Large (Ocean)" and roll_dice(3, max(math.floor(primary_star.age/.5), 5)) >= 18):
                return world_type[1]
            else:
                return world_type[0]
        return world_type

    def calculate_moon_type(self, blackbody_temperature: float, major_moons: List[str], primary_star: Star) -> List[Optional[str]]:
        sulfur_check = True if roll_dice(1) <= 3 else False
        for idx, moon in enumerate(major_moons):
            major_moons[idx] = self.calculate_gas_giant_type(blackbody_temperature, moon, primary_star, sulfur_check)
            if major_moons[idx] == "Tiny (Sulfur)":
                sulfur_check = False
        return major_moons

class TerrestrialPlanet(Planet):
    """
    """
    def __init__(self, primary_star: Star, orbit: float, size: str) -> None:
        Planet.__init__(self, primary_star, orbit, size)
        
        self.moons = self.generate_moons(self.relative_orbital_radius, self.size)
        self.major_moons = self.calculate_moon_size(self.moons, self.size)
        self.major_moons = self.calculate_moon_type(self.temperature, self.major_moons, primary_star)
        self.type = self.calculate_terrestrial_type(self.temperature, self.size, primary_star)

    def generate_moons(self, orbital_radius: float, size: str) -> List[int]:
        """Return a list containing number of moons in each family of satellites"""
        if orbital_radius < 0.5:
            modifier = -6
        elif orbital_radius < 0.75:
            modifier = -3
        elif orbital_radius < 1.5:
            modifier = -1
        else:
            modifier = 0
        if size == "Tiny":
            modifier = modifier - 2
        elif size == "Small":
            modifier = modifier - 1
        elif size == "Large":
            modifier = modifier + 1
        major_moons = max(roll_dice(1,-4+modifier), 0)
        moonlets = max(roll_dice(1,-2+modifier), 0) if major_moons == 0 else 0
        return [moonlets, major_moons]

    def calculate_terrestrial_type(self, blackbody_temperature: float, size_class: str, primary_star: Star) -> str:
        world_type = self.calculate_world_type(blackbody_temperature, size_class)
        if size_class == "Tiny" and type(world_type) == list:
            return world_type[0]
        if (size_class == "Standard" or size_class == "Large") and type(world_type) == list:
            if (world_type[0] == "Standard (Ice)" or world_type[0] == "Large (Ice)") and primary_star.mass <= 0.65:
                return world_type[1]
            elif (world_type[0] == "Standard (Ocean)" and roll_dice(3, max(math.floor(primary_star.age/.5), 10)) >= 18) or (world_type[0] == "Large (Ocean)" and roll_dice(3, max(math.floor(primary_star.age/.5), 5)) >= 18):
                return world_type[1]
            else:
                return world_type[0]
        return world_type
    
    def calculate_moon_type(self, blackbody_temperature: float, major_moons: List[str], primary_star: Star) -> List[Optional[str]]:
        for idx, moon in enumerate(major_moons):
            major_moons[idx] = self.calculate_terrestrial_type(blackbody_temperature, moon, primary_star)
        return major_moons

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
        return look_up(st.multiple_stars_tree, roll_dice(3, 3 if is_in_open_cluster else 0))

    def calculate_stars(self, number_of_stars: int, guarantee_garden_world: bool) -> List[Star]:
        """Return a list containing randomly generated Star objects"""
        stars = []
        for designation in range(number_of_stars):
            if designation > 0:
                companion_star_mass_roll = roll_dice(1, -1)
                if companion_star_mass_roll == 0:
                    stars.append(CompanionStar(designation, stars[0].mass, stars[0].age, guarantee_garden_world))
                else:
                    mass = stars[0].mass-0.05*roll_dice(companion_star_mass_roll)
                    stars.append(CompanionStar(designation, (mass if mass >= 0.10 else 0.10), stars[0].age, guarantee_garden_world))
            else:
                stars.append(Star(guarantee_garden_world=guarantee_garden_world))
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
                gas_giants.append(look_up(st.gas_giant_arrangement_tree, roll_dice(3)))
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
                if temp_radius/look_up(st.orbital_spacing_tree, roll_dice(3)) > temp_radius - 0.15:
                    temp_radius = temp_radius - 0.15
                else:
                    temp_radius = temp_radius/look_up(st.orbital_spacing_tree, roll_dice(3))
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
                if temp_radius*look_up(st.orbital_spacing_tree, roll_dice(3)) < temp_radius + 0.15:
                    temp_radius = temp_radius + 0.15
                else:
                    temp_radius = temp_radius*look_up(st.orbital_spacing_tree, roll_dice(3))
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
                    orbit[i][1] = GasGiant(orbit[0], orbit[i][0], look_up(st.gas_giant_size_tree, roll_dice(3, 4)))
                    continue
                if gas_giants[idx] == "Conventional Gas Giant" and orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 15:
                    orbit[i].append(GasGiant(orbit[0], orbit[i][0], look_up(st.gas_giant_size_tree, roll_dice(3))))
                elif gas_giants[idx] == "Eccentric Gas Giant" and ((orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 14) or (orbit[i][0] <= orbit[0].snow_line_radius and roll_dice(3) <= 8)):
                    orbit[i].append(GasGiant(orbit[0], orbit[i][0], look_up(st.gas_giant_size_tree, roll_dice(3, 4 if orbit[i][0] <= orbit[0].snow_line_radius else 0))))
                elif gas_giants[idx] == "Epistellar Gas Giant" and ((orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 14) or (orbit[i][0] <= orbit[0].snow_line_radius and roll_dice(3) <= 6)):
                    orbit[i].append(GasGiant(orbit[0], orbit[i][0], look_up(st.gas_giant_size_tree, roll_dice(3, 4 if orbit[i][0] <= orbit[0].snow_line_radius else 0))))
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
                orbit_contents = look_up(st.orbit_contents_tree, roll)
                if type(orbit_contents) == list:
                    orbit[i].append(TerrestrialPlanet(orbit[0], orbit[i][0], orbit_contents[1]))
                else:
                    orbit[i].append(orbit_contents)
        return orbits
