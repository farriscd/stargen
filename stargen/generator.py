"""
This module contains the Classes and Methods for randomly generating star systems
according to the GURPS Space 4th edition system.

Todo:
    * Rewrite generate_rotation_period method so that is_tidally_locked is more clearly set
    * Still calculating separate orbits for close binary pairs rather than as center of mass
    * Complete generation of distant companion subcompanions and make sure trinary star
    systems adhere to the suggested guidelines
    * Current calculate_first_orbit allow orbits to fall within forbidden zones
    * Make use of guarantee_garden_world check
    * White Dwarf stars are currently given "None" as temperature since GURPS provides
    no way to calculate it, although it claims to be able to be "quite high"
    * Add some fine tuned randomization to generated numbers
"""

import math
import random
from typing import Any, Union, Optional, List

from .helpers import roll_dice, look_up
from . import basictrees as bt
from . import startrees as st
from . import worldtrees as wt

size_list = ["Tiny", "Small", "Standard", "Large"]


class Star(object):
    """
    The Star object contains data and methods for the creation of a star

    Args:
        mass (float): the mass of the object in relation to the Earths mass mass measured in solar masses
        age (float): age measured in billions of years
        guarantee_garden_world (bool): increases chances of generating a Garden World type planet

    Attributes:
        mass (float): the mass of the object in relation to the Earths mass mass of the star in solar masses
        age (float): age of the star in billions of years
        type (str or NoneType): most probable spectral type, NoneType for White Dwarf stars
        sequence (str): luminosity class of the star; "III", "IV", "V", and "D"
        temperature (float or NoneType): effective temperature of the star measured in kelvins
        luminosity (float): total energy output of the star measured in solar luminosities
        radius (float or NoneType): radius of the star measured in astronomical units, NoneType for White Dwarf stars
        inner_limit_radius (float): radius used for generating planet generation in astronomical units
        outer_limit_radius (float): radius used for planet generation in astronomical units
        snow_line_radius(float): radius used for planet generation in astronomical units
    """

    def __init__(
        self,
        mass: Optional[float] = None,
        age: Optional[float] = None,
        guarantee_garden_world: bool = False,
    ) -> None:
        self.guarantee_garden_world = guarantee_garden_world

        if mass is None:
            mass = self.generate_stellar_mass()
        self.mass = mass

        if age is None:
            age = self.generate_stellar_age()
        self.age = age

        self.sequence = self.calculate_stellar_sequence()
        if self.sequence == "D":
            self.white_dwarf_death()

        self.temperature = self.calculate_stellar_temperature()
        self.luminosity = self.calculate_stellar_luminosity()
        self.type = self.calculate_stellar_type()
        self.radius = self.calculate_stellar_radius()

        self.inner_limit_radius = self.calculate_inner_limit_radius()
        self.outer_limit_radius = self.calculate_outer_limit_radius()
        self.snow_line_radius = self.calculate_snow_line_radius()

        self.gas_giant_arrangement = []

    def generate_stellar_mass(self) -> float:
        """Return a randomly generated star mass"""
        if self.guarantee_garden_world:
            table = look_up(st.stellar_mass_tree_first_roll_garden_world, roll_dice(1))
            stellar_mass = look_up(table, roll_dice(3))
        else:
            table = look_up(st.stellar_mass_tree_first_roll, roll_dice(3))
            stellar_mass = look_up(table, roll_dice(3))
        return stellar_mass

    def generate_stellar_age(self) -> float:
        """Return a randomly generated system age"""
        if self.guarantee_garden_world:
            base_age, step_a, step_b = look_up(st.stellar_age_tree, roll_dice(2, 2))
        else:
            base_age, step_a, step_b = look_up(st.stellar_age_tree, roll_dice(3))
        stellar_age = base_age + step_a * roll_dice(1, -1) + step_b * roll_dice(1, -1)
        return stellar_age

    def calculate_stellar_sequence(self) -> str:
        """Return a luminosity class based on mass and age of star"""
        *_, m_span, s_span, g_span = look_up(st.stellar_evolution_tree, self.mass)
        if s_span is None:
            stellar_sequence = "V"
        elif self.age > m_span + s_span + g_span:
            stellar_sequence = "D"
        elif self.age > m_span + s_span:
            stellar_sequence = "III"
        elif self.age > m_span:
            stellar_sequence = "IV"
        else:
            stellar_sequence = "V"
        return stellar_sequence

    def white_dwarf_death(self) -> None:
        """Modifies the mass of a white dwarf"""
        self.stellar_mass = 0.9 + 0.05 * roll_dice(2, -2)

    def calculate_stellar_temperature(self) -> Optional[float]:
        """Return an effective temperature based on mass, age, and sequence"""
        _, temp, _, _, m_span, s_span, _ = look_up(st.stellar_evolution_tree, self.mass)
        if self.sequence == "V":
            stellar_temperature = temp
        elif self.sequence == "IV":
            stellar_temperature = temp - (
                ((self.age - m_span) / s_span) * (temp - 4800)
            )
        elif self.sequence == "III":
            stellar_temperature = 3000 + 200 * roll_dice(2, -2)
        else:
            stellar_temperature = None
        return stellar_temperature

    def calculate_stellar_luminosity(self) -> float:
        """Return luminosity based on mass, age, and sequence"""
        _, _, l_min, l_max, m_span, *_ = look_up(st.stellar_evolution_tree, self.mass)
        if self.sequence == "V":
            stellar_luminosity = (
                l_min
                if l_max is None
                else l_min + ((self.age / m_span) * (l_max - l_min))
            )
        elif self.sequence == "IV":
            stellar_luminosity = l_max
        elif self.sequence == "III":
            stellar_luminosity = l_max * 25
        else:
            stellar_luminosity = 0.001
        return stellar_luminosity

    def calculate_stellar_type(self) -> Optional[str]:
        """Return a spectral type based on mass of the star"""
        if self.sequence == "V":
            stellar_type, *_ = look_up(st.stellar_evolution_tree, self.mass)
        elif self.sequence == "IV":
            stellar_type = look_up(st.stellar_evolution_tree_reverse, self.temperature)
        elif self.sequence == "III":
            stellar_type = look_up(st.stellar_evolution_tree_reverse, self.temperature)
        else:
            stellar_type = None
        return stellar_type

    def calculate_stellar_radius(self) -> Optional[float]:
        """Return radius based on temperature and luminosity"""
        if self.temperature is None:
            stellar_radius = None
        else:
            stellar_radius = (155000 * math.sqrt(self.luminosity)) / (
                math.pow(self.temperature, 2)
            )
        return stellar_radius

    def calculate_inner_limit_radius(self) -> float:
        """Return a list of inner limit radii corresponding to each star"""
        inner_limit_radius = max(0.1 * self.mass, 0.01 * math.sqrt(self.luminosity))
        return inner_limit_radius

    def calculate_outer_limit_radius(self) -> float:
        """Return a list of outer limit radii corresponding to each star"""
        outer_limit_radius = 40.0 * self.mass
        return outer_limit_radius

    def calculate_snow_line_radius(self) -> float:
        """Return a list of snow line radii corresponding to each star"""
        _, _, l_min, *_ = look_up(st.stellar_evolution_tree, self.mass)
        snow_line_radius = 4.85 * math.sqrt(l_min)
        return snow_line_radius


class CompanionStar(Star):
    """
    A Star-based object for non-primary stars in multistar systems

    Args:
        designation (int): number designating which companion this star is
        primary_star (Star):  the Star object around which this object gravitates the 'parent' star

    Attributes:
        designation (int): number designating which companion this star is
        orbital_separation (list: str, float): a list containing seperation and eccentricity
        semi_major_axis (float): the average orbital radius of this object around its primary_star the 'average' radius of orbit in astronomical units
        eccentricity (float): eccentricity of the companion stars orbit
    """

    def __init__(self, designation: int, primary_star: Star) -> None:
        self.designation = designation
        self.primary_star = primary_star
        self.guarantee_garden_world = primary_star.guarantee_garden_world

        self.mass = self.generate_companion_mass()
        self.age = self.primary_star.age
        Star.__init__(self, self.mass, self.age, self.guarantee_garden_world)

        self.separation, radius_multiplier = self.generate_orbital_separation()
        self.eccentricity = self.generate_eccentricity()
        self.semi_major_axis = self.generate_semi_major_axis(radius_multiplier)
        self.orbital_period = self.calculate_stellar_orbital_period()

    def generate_companion_mass(self) -> float:
        """Returns an appropriate mass for a companion of the supplied Star"""
        companion_star_mass_roll = roll_dice(1, -1)
        if companion_star_mass_roll == 0:
            companion_mass = self.primary_star.mass
        else:
            companion_mass = max(
                self.primary_star.mass - 0.05 * roll_dice(companion_star_mass_roll),
                0.10,
            )
        return companion_mass

    def generate_orbital_separation(self) -> List[Union[str, float]]:
        """Return a list containing the companion star 'Separation' and radius multiplier"""
        modifier = 0
        if self.guarantee_garden_world:
            modifier += 4
        if self.designation == 2:
            modifier += 6
        separation, radius_multiplier = look_up(
            st.orbital_separation_tree, roll_dice(3, modifier)
        )
        return separation, radius_multiplier

    def generate_eccentricity(self) -> float:
        """Return the eccentricity for a companion star orbit"""
        if self.separation == "Very Close":
            modifier = -6
        elif self.separation == "Close":
            modifier = -4
        elif self.separation == "Moderate":
            modifier = -2
        else:
            modifier = 0
        eccentricity = look_up(
            st.stellar_orbital_eccentricity_tree, roll_dice(3, modifier)
        )
        return eccentricity

    def generate_semi_major_axis(self, radius_multiplier: float) -> float:
        """Return the average orbital radius (or semi-major axis) of a companion star in AU"""
        semi_major_axis = roll_dice(2) * radius_multiplier
        return semi_major_axis

    def calculate_stellar_orbital_period(self) -> float:
        """Return the orbital period in years"""
        orbital_period = math.sqrt(
            (self.semi_major_axis ** 3) / (self.mass + self.primary_star.mass)
        )
        return orbital_period


class World(object):
    """
    This class is a template with common methods used by the MajorMoon, Terrestrial, and GasGiant classes.

    Args:
        primary_star (Star):  the Star object around which this object gravitates
        orbit (float): the average orbital radius of this object around its primary_star
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large"

    Attributes:
        primary_star (Star):  the Star object around which this object gravitates
        semi_major_axis (float): the average orbital radius of this object around its primary_star
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large"
        temperature (float): the average blackbody temperature of this object
        type (str): a string corresponding to the type of object; i.e. "Gas Giant" or "Hadean"
    """

    def __init__(self, primary_star: Star, orbit: float, size: str) -> None:
        self.primary_star = primary_star
        self.semi_major_axis = orbit

        self.size = size

        self.temperature = self.calculate_blackbody_temperature()
        self.type = self.calculate_world_type()

        self.major_moons = []

        self.mass = None
        self.density = None
        self.diameter = None
        self.surface_gravity = None

        self.orbital_period = None
        self.total_tidal_effect = None
        self.rotation_period = None
        self.is_tidally_locked = False
        self.axial_tilt = None

        # Attributes for Terrestrial/MajorMoon
        self.atmospheric_mass = None
        self.atmospheric_composition = None
        self.hydrographic_coverage = None
        self.atmospheric_pressure = None

        self.volcanic_activity = None
        self.tectonic_activity = None

    def calculate_blackbody_temperature(self) -> float:
        """Return the effective temperature of the planet"""
        blackbody_temperature = (
            278 * (self.primary_star.luminosity ** (1.0 / 4))
        ) / math.sqrt(self.semi_major_axis)
        return blackbody_temperature

    def look_up_world_type(self) -> Union[List[str], str]:
        """Return a string or list of strings of possible world types"""
        if self.size == "Tiny":
            world_type = look_up(wt.tiny_world_type_assignment_tree, self.temperature)
        elif self.size == "Small":
            world_type = look_up(wt.small_world_type_assignment_tree, self.temperature)
        elif self.size == "Standard":
            world_type = look_up(
                wt.standard_world_type_assignment_tree, self.temperature
            )
        elif self.size == "Large":
            world_type = look_up(wt.large_world_type_assignment_tree, self.temperature)
        return world_type

    def calculate_world_type(self) -> str:
        """Return a string describing the world type"""
        world_type = self.look_up_world_type()
        if (self.size == "Tiny") and isinstance(world_type, list):
            world_type = world_type[0]
        if (self.size == "Standard" or self.size == "Large") and isinstance(
            world_type, list
        ):
            if (
                world_type[0] == "Standard (Ice)" or world_type[0] == "Large (Ice)"
            ) and self.primary_star.mass <= 0.65:
                world_type = world_type[1]
            elif (
                world_type[0] == "Standard (Ocean)"
                and roll_dice(3, max(math.floor(self.primary_star.age / 0.5), 10)) >= 18
            ) or (
                world_type[0] == "Large (Ocean)"
                and roll_dice(3, max(math.floor(self.primary_star.age / 0.5), 5)) >= 18
            ):
                world_type = world_type[1]
            else:
                world_type = world_type[0]
        return world_type

    def generate_atmospheric_mass(self) -> float:
        """Return the atmospheric mass of a given world type"""
        if self.type in wt.no_atmosphere_world_types:
            atmospheric_mass = 0
        else:
            atmospheric_mass = roll_dice(3) / 10.0
        return atmospheric_mass

    def generate_atmospheric_composition(self) -> List[str]:
        """Return a list of strings describing atmospheric composition"""
        if self.type == "Small (Ice)":
            if roll_dice(3) <= 15:
                atmospheric_composition = ["Suffocating", "Mildly Toxic"]
            else:
                atmospheric_composition = ["Suffocating", "Highly Toxic"]
        elif self.type in [
            "Standard (Ammonia)",
            "Standard (Greenhouse)",
            "Large (Ammonia)",
            "Large (Greenhouse)",
        ]:
            atmospheric_composition = ["Suffocating", "Lethaly Toxic", "Corrosive"]
        elif self.type in ["Standard (Ice)", "Standard (Ocean)"]:
            if roll_dice(3) <= 12:
                atmospheric_composition = ["Suffocating"]
            else:
                atmospheric_composition = ["Suffocating", "Mildly Toxic"]
        elif self.type in ["Standard (Garden)", "Large (Garden)"]:
            if roll_dice(3) <= 11:
                atmospheric_composition = ["Standard"]
            else:
                atmospheric_composition = [self.generate_marginal_atmosphere()]
        elif self.type in ["Large (Ice)", "Large (Ocean)"]:
            atmospheric_composition = ["Suffocating", "Highly Toxic"]
        elif self.type in ["Small (Rock)", "Standard (Chthonian)", "Large (Chthonian)"]:
            atmospheric_composition = ["Trace Atmosphere"]
        else:
            atmospheric_composition = ["Vacuum"]
        return atmospheric_composition

    def generate_marginal_atmosphere(self) -> List[str]:
        """Return a list of marginal atmospheres"""
        marginal_atmosphere = look_up(bt.marginal_atmospheres_tree, roll_dice(3))
        return marginal_atmosphere

    def generate_hydrographic_coverage(self) -> float:
        """Return the percentage of hydrographic coverage of a planet"""
        if self.type == "Small (Ice)":
            hydrographic_coverage = roll_dice(1, 2) * 0.1
        elif self.type in ["Standard (Ammonia)", "Large (Ammonia)"]:
            hydrographic_coverage = min(roll_dice(2) * 0.1, 1.0)
        elif self.type in ["Standard (Ice)", "Large (Ice)"]:
            hydrographic_coverage = max(roll_dice(2, -10) * 0.1, 0.0)
        elif self.type in ["Standard (Ocean)", "Standard (Garden)"]:
            hydrographic_coverage = roll_dice(1, 4) * 0.1
        elif self.type in ["Large (Ocean)", "Large (Garden)"]:
            hydrographic_coverage = min(roll_dice(1, 6) * 0.1, 1.0)
        elif self.type in ["Standard (Greenhouse)", "Large (Greenhouse)"]:
            hydrographic_coverage = max(roll_dice(2, -7) * 0.1, 0.0)
        else:
            hydrographic_coverage = 0.0
        return hydrographic_coverage

    def calculate_surface_temperature(self) -> float:
        """Return the average surface temperature of a world"""
        absorption_factor, greenhouse_factor = bt.temperature_factors(
            self.type, self.hydrographic_coverage
        )
        blackbody_correction = absorption_factor * (
            1 + (self.atmospheric_mass * greenhouse_factor)
        )
        average_surface_temperature = self.temperature * blackbody_correction
        return average_surface_temperature

    def calculate_climate_type(self) -> str:
        """Return the climate type of the world"""
        climate_type = look_up(bt.world_climate_tree, self.temperature)
        return climate_type

    def generate_density(self) -> float:
        """Return the density of a world in relation to the Earths density"""
        if self.type in wt.icy_core_world_types:
            density = look_up(bt.world_density_tree, roll_dice(3))[0]
        elif self.type in wt.small_iron_core_world_types:
            density = look_up(bt.world_density_tree, roll_dice(3))[1]
        else:
            density = look_up(bt.world_density_tree, roll_dice(3))[2]
        return density

    def generate_diameter(self) -> float:
        """Return the diameter of a world in relation to the Earths"""
        if self.size == "Large":
            minimum_factor = 0.065
            maximum_factor = 0.091
        elif self.size == "Standard":
            minimum_factor = 0.030
            maximum_factor = 0.065
        elif self.size == "Small":
            minimum_factor = 0.024
            maximum_factor = 0.030
        elif self.size == "Tiny":
            minimum_factor = 0.004
            maximum_factor = 0.024
        minimum_diameter = minimum_factor * math.sqrt(self.temperature / self.density)
        maximum_diameter = maximum_factor * math.sqrt(self.temperature / self.density)
        variable_diameter = (
            roll_dice(2, -2) * (maximum_diameter - minimum_diameter) * 0.1
        )
        diameter = minimum_diameter + variable_diameter
        return diameter

    def calculate_surface_gravity(self) -> float:
        """Return the gravity of a world in relation to the Earths"""
        surface_gravity = self.density * self.diameter
        return surface_gravity

    def calculate_mass(self) -> float:
        """Return the mass of a world in relation to the Earths"""
        mass = self.density * (self.diameter ** 3)
        return mass

    def calculate_atmospheric_pressure(self) -> float:
        """Return the atmospheric pressure in relation to the Earths"""
        if self.atmospheric_composition in ["Trace", "Vacuum"]:
            atmospheric_pressure = 0
        elif self.type == "Small (Ice)":
            atmospheric_pressure = self.atmospheric_mass * 10 * self.surface_gravity
        elif self.type == "Standard (Greenhouse)":
            atmospheric_pressure = self.atmospheric_mass * 100 * self.surface_gravity
        elif self.size == "Standard":
            atmospheric_pressure = self.atmospheric_mass * 1 * self.surface_gravity
        elif self.type == "Large (Greenhouse)":
            atmospheric_pressure = self.atmospheric_mass * 500 * self.surface_gravity
        elif self.size == "Large":
            atmospheric_pressure = self.atmospheric_mass * 5 * self.surface_gravity
        return atmospheric_pressure

    def calculate_atmospheric_pressure_category(self) -> str:
        """Return atmospheric pressure category"""
        atmospheric_pressure_category = look_up(
            bt.atmospheric_pressure_categories_tree, self.atmospheric_pressure
        )
        return atmospheric_pressure_category

    def generate_axial_tilt(self) -> int:
        """Return the axial tilt of a planet in degrees"""
        axial_tilt = look_up(wt.axial_tilt_tree, roll_dice(3))
        return axial_tilt

    def generate_volcanic_atmosphere(self) -> None:
        """Adjusts the worlds atmosphere to marginal depending on volcanic activity"""
        if self.type == "Standard (Garden)" or self.type == "Large (Garden)":
            if self.volcanic_activity == "Heavy":
                if roll_dice(3) <= 8:
                    self.atmospheric_composition = random.choice(
                        ["Pollutants", "Sulfur Compounds"]
                    )
            elif self.volcanic_activity == "Extreme":
                if roll_dice(3) <= 14:
                    self.atmospheric_composition = random.choice(
                        ["Pollutants", "Sulfur Compounds"]
                    )

    def generate_tectonic_activity(self) -> str:
        """"""
        if self.size == "Tiny" or self.size == "Small":
            tectonic_activity = "None"
        else:
            modifier = 0
            if self.volcanic_activity == "None":
                modifier -= 8
            if self.volcanic_activity == "Light":
                modifier -= 4
            if self.volcanic_activity == "Heavy":
                modifier += 4
            if self.volcanic_activity == "Extreme":
                modifier += 8
            if self.hydrographic_coverage == 0:
                modifier -= 4
            if self.hydrographic_coverage < 0.50:
                modifier -= 2
            if isinstance(self, Terrestrial):
                if len(self.major_moons) == 1:
                    modifier += 2
                if len(self.major_moons) > 1:
                    modifier += 4
            tectonic_activity = look_up(
                wt.tectonic_activity_tree, roll_dice(3, modifier)
            )
        return tectonic_activity


class Planet(World):
    """
    This class is a template with common methods used by the Terrestrial and GasGiant classes.

    Args:
        primary_star (Star):  the Star object around which this object gravitates
        orbit (float): the average orbital radius of this object around its primary_star
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large"

    Attributes:
        moons (list[int]): a list containing the number of moons, major moons, or moonlets of this object
        major_moons (list[MajorMoon]): a list containing the MajorMoon objects in rotation around this object
        is_retrograde_orbit (bool): whether or not this object rotations opposite  of its primary_star

    """

    def __init__(self, primary_star: Star, orbit: float, size: str) -> None:
        World.__init__(self, primary_star, orbit, size)

        self.moons = [0, 0]
        self.major_moons = []

        self.is_retrograde_orbit = self.generate_retrograde_orbit()

    def generate_major_moons(self) -> None:
        """Return a list containing MajorMoon objects"""
        for _ in range(self.moons[1]):
            self.major_moons.append(MajorMoon(self))

    def calculate_planetary_orbital_period(self) -> float:
        """Return the orbital period of a planet around its primary star in years"""
        sum_of_masses = self.primary_star.mass + 0.000003 * self.mass
        orbital_period = math.sqrt((self.semi_major_axis ** 3.0) / sum_of_masses)
        return orbital_period

    def generate_planetary_orbital_eccentricity(self) -> float:
        """Return the eccentricity of a planets orbit"""
        modifier = 0
        if isinstance(self, GasGiant):
            if (
                self.semi_major_axis < self.primary_star.snow_line_radius
                and self.primary_star.gas_giant_arrangement == "Eccentric Gas Giant"
            ):
                modifier += 4
            elif (
                self.semi_major_axis <= 1.8 * self.primary_star.inner_limit_radius
                and self.primary_star.gas_giant_arrangement == "Epistellar Gas Giant"
            ):
                modifier -= 6
            elif self.primary_star.gas_giant_arrangement == "Conventional Gas Giant":
                modifier -= 6
        orbital_eccentricity = look_up(
            wt.planetary_orbital_eccentricity_tree, roll_dice(3, modifier)
        )
        return orbital_eccentricity

    def calculate_tidal_force_from_star(self) -> float:
        """Return the tidal effect from a given star"""
        tidal_force = (
            0.46 * self.primary_star.mass * self.diameter
        ) / self.semi_major_axis ** 3
        return tidal_force

    def calculate_tidal_force_from_satellites(self) -> float:
        """Return the sum of tidal effects from a planets satellites"""
        sum_of_tidal_forces = 0
        for satellite in self.major_moons:
            sum_of_tidal_forces += satellite.calculate_tidal_force_from_satellite()
        return sum_of_tidal_forces

    def calculate_total_tidal_effect(self) -> int:
        """Return the total tidal effect on a world"""
        sum_of_tidal_forces = (
            self.calculate_tidal_force_from_satellites()
            + self.calculate_tidal_force_from_star()
        )
        total_tidal_effect = (sum_of_tidal_forces * self.primary_star.age) / self.mass
        total_tidal_effect = round(total_tidal_effect)
        return total_tidal_effect

    def generate_retrograde_orbit(self) -> bool:
        """Return whether a planets orbit is retrograde"""
        roll = roll_dice(3)
        is_retrograde_orbit = False
        if roll >= 13:
            is_retrograde_orbit = True
        return is_retrograde_orbit

    def calculate_local_calendar(self) -> Union[float, str]:
        """Return the apparent day length of a planet"""
        sidereal_period = self.orbital_period
        rotation_period = self.rotation_period
        if self.is_retrograde_orbit:
            rotation_period = -1 * rotation_period
        if rotation_period == sidereal_period:
            apparent_length = "No apparent motion"
        else:
            apparent_length = (sidereal_period * rotation_period) / (
                sidereal_period - rotation_period
            )
        return apparent_length


class MajorMoon(World):
    """
    A World-type object that contains methods and attributes of major moons.

    Args:
        primary_planet (Planet): The Terrestrial or GasGiant object which this moon orbits

    Attributes:
        primary_planet (Planet): The Terrestrial or GasGiant object which this moon orbits
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large" 
        primary_star (Star):  the Star object around which this object gravitates
        semi_major_axis (float): the average orbital radius of this object around its primary_star
        temperature (float): the average blackbody temperature of this object
        type (str): a string corresponding to the type of object; i.e. "Gas Giant" or "Hadean"
        atmospheric_mass (float): the rough estimate of gaseous volatiles in this objects atmosphere
        atmospheric_composition (list[str]): a list of strings describing the breathability of this objects atompshere
        hydrographic_coverage (float): a float from 0 to 1 describing the percentage of the object covered in water
        surface_temperature (float): the average surface temperature of the object
        climate_type (str): a string describing the average climate of this object
        density (float):  the density of this object in relation to the Earths density
        diameter (float): the diameter of this object in relation to the Earths diameter
        surface_gravity (float): the gravity at this objects surface in relation to the Earths gravity
        mass (float): the mass of the object in relation to the Earths mass
        satellite_orbital_radius (float): the average orbital radius of this object around its primary_planet
        satellite_orbital_period (float): the average orbital period of this object around its primary_planet
        total_tidal_effect (int): an int used in calculating tidal effects on this object
        rotation_period (float): the average orbital period of this object around its primary_star
        is_tidally_locked (bool): whether or not this object is tidally locked to its primary_planet
        axial_tilt (int): the axial tilt of this object in degrees
        is_retrograde_orbit (bool): whether or not this object rotations opposite  of its primary_star
        apparent_length (float): the length of a 'day' on this object
        apparent_length_as_seen_by_planet:
        volcanic_activity (str): a string describing the level of volcanic activity on this object
        tectonic_activity (str): a string describing the level of tectonic activity on this object
    """

    def __init__(self, primary_planet: Planet) -> None:
        self.primary_planet = primary_planet
        if isinstance(primary_planet, GasGiant):
            self.size = self.generate_moon_size(planet_size="Large")
        else:
            self.size = self.generate_moon_size(self.primary_planet.size)

        World.__init__(
            self,
            self.primary_planet.primary_star,
            self.primary_planet.semi_major_axis,
            self.size,
        )
        delattr(self, "major_moons")

        self.atmospheric_mass = self.generate_atmospheric_mass()
        self.atmospheric_composition = self.generate_atmospheric_composition()
        self.hydrographic_coverage = self.generate_hydrographic_coverage()
        self.surface_temperature = self.calculate_surface_temperature()
        self.climate_type = self.calculate_climate_type()

        self.density = self.generate_density()
        self.diameter = self.generate_diameter()
        self.surface_gravity = self.calculate_surface_gravity()
        self.mass = self.calculate_mass()

        self.satellite_orbital_radius = self.generate_satellite_orbital_radius()
        if len(self.primary_planet.major_moons) >= 1:
            self.readjust_satellite_orbital_radius()

        self.satellite_orbital_period = self.calculate_satellite_orbital_period()
        self.total_tidal_effect = self.calculate_total_tidal_effect()
        self.rotation_period = self.generate_rotation_period()
        if not self.is_tidally_locked:
            self.axial_tilt = self.generate_axial_tilt()

        self.is_retrograde_orbit = self.generate_retrograde_orbit()
        self.apparent_length = self.calculate_local_calendar()
        # self.apparent_length_as_seen_by_planet = self.calculate_calendar_as_seen()

        self.volcanic_activity = self.generate_volcanic_activity()
        self.generate_volcanic_atmosphere()
        self.tectonic_activity = self.generate_tectonic_activity()

    def generate_moon_size(self, planet_size: str) -> str:
        """Return a string describing the size of the moon"""
        moon_size_relation = look_up(st.moon_size_tree, roll_dice(3))
        enum_planet_size = size_list.index(planet_size)
        moon_size = size_list[max(enum_planet_size + moon_size_relation, 0)]
        return moon_size

    def generate_satellite_orbital_radius(self) -> float:
        """Return the orbital radius of the satellite around its planet"""
        if isinstance(self.primary_planet, GasGiant):
            orbital_radius = roll_dice(3, 3)
            if orbital_radius >= 15:
                orbital_radius += roll_dice(2)
            orbital_radius = (orbital_radius / 2.0) * self.primary_planet.diameter
        elif isinstance(self.primary_planet, Terrestrial):
            modifier = 0
            enum_planet_size = size_list.index(self.primary_planet.size)
            enum_moon_size = size_list.index(self.size)
            if enum_planet_size - enum_moon_size == 2:
                modifier = 2
            elif enum_planet_size - enum_moon_size == 1:
                modifier = 4
            orbital_radius = roll_dice(2, modifier)
            orbital_radius = orbital_radius * 2.5 * self.primary_planet.diameter
        return orbital_radius

    def illegal_orbit(self) -> bool:
        """Check if a given orbital radius is possible given already generated moon orbits"""
        if isinstance(self.primary_planet, Terrestrial):
            modifier = 5
        else:
            modifier = 1
        for moon in self.primary_planet.major_moons:
            if (
                abs(self.satellite_orbital_radius - moon.satellite_orbital_radius)
                < self.primary_planet.diameter * modifier
            ):
                return True
        return False

    def readjust_satellite_orbital_radius(self) -> None:
        """Readjust the orbital radius if currently within an illegal orbit"""
        while self.illegal_orbit() is True:
            self.satellite_orbital_radius = self.generate_satellite_orbital_radius()

    def calculate_satellite_orbital_period(self) -> float:
        """Return the orbital period of the moon around its planet in Earth diameters"""
        sum_of_masses = self.primary_planet.mass + self.mass
        satellite_orbital_period = 0.0588 * math.sqrt(
            (self.satellite_orbital_radius ** 3.0) / sum_of_masses
        )
        return satellite_orbital_period

    def calculate_tidal_force_from_satellite(self) -> float:
        """Return the tidal effect from a given satellite"""
        tidal_force = (
            17_800_000 * self.mass * self.primary_planet.diameter
        ) / self.satellite_orbital_radius ** 3
        return tidal_force

    def calculate_tidal_force_from_planet(self) -> float:
        """Return the tidal effect from a given planet"""
        tidal_force = (
            17_800_000 * self.primary_planet.mass * self.diameter
        ) / self.satellite_orbital_radius ** 3
        return tidal_force

    def calculate_total_tidal_effect(self) -> int:
        """Return the total tidal effect on a world"""
        sum_of_tidal_forces = self.calculate_tidal_force_from_planet()
        total_tidal_effect = (sum_of_tidal_forces * self.primary_star.age) / self.mass
        total_tidal_effect = round(total_tidal_effect)
        return total_tidal_effect

    def calculate_rotational_period_modifier(self) -> int:
        """Return the modifier to the Satellite rotation period"""
        modifier = 0
        if self.size == "Large":
            modifier = 6
        elif self.size == "Standard":
            modifier = 10
        elif self.size == "Small":
            modifier = 14
        elif self.size == "Tiny":
            modifier = 18
        return modifier

    def generate_rotation_period(self) -> Union[int, float]:
        """Return the rotation period of the Satellite"""
        rotation_period_roll = roll_dice(3)
        rotation_period = (
            self.total_tidal_effect
            + rotation_period_roll
            + self.calculate_rotational_period_modifier()
        )
        if rotation_period_roll >= 16 or rotation_period > 36:
            special_rotation_roll = roll_dice(2)
            if special_rotation_roll > 6:
                rotation_period = look_up(
                    wt.special_rotation_tree, special_rotation_roll
                )
        if (
            self.total_tidal_effect >= 50
            or rotation_period > self.satellite_orbital_period
        ):
            self.is_tidally_locked = True
            rotation_period = self.satellite_orbital_period
        return rotation_period

    def generate_retrograde_orbit(self) -> bool:
        """Return whether a satellite has a retrograde orbit"""
        roll = roll_dice(3)
        is_retrograde_orbit = False
        if roll >= 17:
            is_retrograde_orbit = True
        return is_retrograde_orbit

    def calculate_local_calendar(self) -> Union[float, str]:
        """Return the apparent day length of a moon"""
        sidereal_period = self.primary_planet.orbital_period
        rotation_period = self.rotation_period
        if self.is_retrograde_orbit:
            rotation_period = -1 * rotation_period
        if rotation_period == sidereal_period:
            apparent_length = "No apparent motion"
        else:
            apparent_length = (sidereal_period * rotation_period) / (
                sidereal_period - rotation_period
            )
        return apparent_length

    def calculate_calendar_as_seen(self) -> Union[float, str]:
        """Return the apparent day length of a moon as seen by host planet"""
        sidereal_period = self.satellite_orbital_period
        rotation_period = self.primary_planet.rotation_period
        if self.is_retrograde_orbit:
            rotation_period = -1 * rotation_period
        if rotation_period == sidereal_period:
            apparent_length = "No apparent motion"
        else:
            apparent_length = (sidereal_period * rotation_period) / (
                sidereal_period - rotation_period
            )
        return apparent_length

    def generate_volcanic_activity(self) -> str:
        """Return the level of volcanic activity of a moon"""
        modifier = round(40 * (self.surface_gravity / self.primary_star.age))
        if self.type == "Tiny (Sulfur)":
            modifier += 60
        if isinstance(self.primary_planet, GasGiant):
            modifier += 5
        volcanic_activity = look_up(wt.volcanic_activity_tree, roll_dice(3, modifier))
        return volcanic_activity


class GasGiant(Planet):
    """
    A Planet-type object containing methods and attributes for Gas Giant type planets

    Args:
        primary_star (Star):  the Star object around which this object gravitates
        orbit (float): the average orbital radius of this object around its primary_star
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large"

    Attributes:
        primary_star (Star):  the Star object around which this object gravitates
        semi_major_axis (float): the average orbital radius of this object around its primary_star
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large"
        temperature (float): the average blackbody temperature of this object
        type (str): a string corresponding to the type of object; i.e. "Gas Giant" or "Hadean"
        moons (list[int]): a list containing the number of moons, major moons, or moonlets of this object
        major_moons (list[MajorMoon]): a list containing the MajorMoon objects in rotation around this object
        is_retrograde_orbit (bool): whether or not this object rotations opposite  of its primary_star
        mass (float): the mass of the object in relation to the Earths mass
        diameter (float): the diameter of this object in relation to the Earths diameter
        surface_gravity (float): the gravity at this objects surface in relation to the Earths gravity
        orbital_period (float): the average orbital period of this object around its primary_star
        orbital_eccentricity (float): the eccentricity of this objects orbit aroudn its primary_star
        is_tiny_sulfur_moon_possible (bool): whether or not a MajorMoon of the "Tiny (Sulfur)" type is legal for this object
        ring_system (str): a string describing the visibility of this objects possible ring system
        total_tidal_effect (int): an int used in calculating tidal effects on this object
        rotation_period (float): the average orbital period of this object around its primary_star
        axial_tilt (int): the axial tilt of this object in degrees
        apparent_length (float): the length of a 'day' on this object
    """

    def __init__(self, primary_star: Star, orbit: float, size: str) -> None:
        Planet.__init__(self, primary_star, orbit, size)
        delattr(self, "atmospheric_mass")
        delattr(self, "atmospheric_composition")
        delattr(self, "hydrographic_coverage")
        delattr(self, "atmospheric_pressure")
        delattr(self, "volcanic_activity")
        delattr(self, "tectonic_activity")

        self.type = size + " (Gas Giant)"
        self.mass, self.density = self.generate_world_size()
        self.diameter = self.calculate_diameter()
        self.surface_gravity = self.calculate_surface_gravity()

        self.orbital_period = self.calculate_planetary_orbital_period()
        self.orbital_eccentricity = self.generate_planetary_orbital_eccentricity()

        is_tiny_sulfur_moon_possible = True if roll_dice(1) <= 3 else False
        self.moons = self.generate_moons()
        self.generate_major_moons()
        self.ring_system = self.calculate_ring_visibility()

        if is_tiny_sulfur_moon_possible is True:
            self.ice_or_sulfur()

        self.total_tidal_effect = self.calculate_total_tidal_effect()
        self.rotation_period = self.generate_rotation_period()
        if not self.is_tidally_locked:
            self.axial_tilt = self.generate_axial_tilt()

        self.apparent_length = self.calculate_local_calendar()

    def generate_moons(self) -> List[int]:
        """Return a list containing number of moons in each family of satellites"""
        modifiers = look_up(st.gas_giant_moon_size_modifiers, self.semi_major_axis)
        inner_moonlets = max(roll_dice(2, modifiers[0]), 0)
        major_moons = max(roll_dice(1, modifiers[1]), 0)
        irregular_moonlets = max(roll_dice(1, modifiers[2]), 0)
        return [inner_moonlets, major_moons, irregular_moonlets]

    def calculate_ring_visibility(self) -> str:
        """Return the visibility of a gas giants rings based on moons"""
        if self.moons[0] >= 10:
            ring_visibility = "High Visibility"
        elif self.moons[0] >= 6:
            ring_visibility = "Moderate Visibility"
        else:
            ring_visibility = "Low Visibility"
        return ring_visibility

    def ice_or_sulfur(self) -> None:
        """Check for existing sulfur moons, if possible will adjust first moon"""
        for moon in self.major_moons:
            if moon.type == "Tiny (Ice)":
                moon.type = "Tiny (Sulfur)"
                break

    def generate_world_size(self) -> float:
        """Return mass and density of gas giant"""
        if self.type == "Small (Gas Giant)":
            mass, density = look_up(wt.gas_giant_size_tree, roll_dice(3))[0]
        elif self.type == "Standard (Gas Giant)":
            mass, density = look_up(wt.gas_giant_size_tree, roll_dice(3))[1]
        elif self.type == "Large (Gas Giant)":
            mass, density = look_up(wt.gas_giant_size_tree, roll_dice(3))[2]
        return mass, density

    def calculate_diameter(self) -> float:
        """Return planet diameter as ratio of earth diameter"""
        diameter = (self.mass / self.density) ** (1.0 / 3)
        return diameter

    def calculate_rotational_period_modifier(self) -> int:
        """Return the modifier to the Gas Giants rotation period"""
        modifier = 0
        if self.type == "Small (Gas Giant)":
            modifier = 6
        return modifier

    def generate_rotation_period(self) -> Union[float, int]:
        """Return the rotation period of the Gas Giant"""
        rotation_period_roll = roll_dice(3)
        rotation_period = (
            self.total_tidal_effect
            + rotation_period_roll
            + self.calculate_rotational_period_modifier()
        )
        if rotation_period_roll >= 16 or rotation_period > 36:
            special_rotation_roll = roll_dice(2)
            if special_rotation_roll > 6:
                rotation_period = look_up(
                    wt.special_rotation_tree, special_rotation_roll
                )
        if (
            self.total_tidal_effect >= 50
            or rotation_period > self.orbital_period * 365.26
        ):
            self.is_tidally_locked = True
            rotation_period = self.orbital_period * 365.26
        return rotation_period


class Terrestrial(Planet):
    World
    """
    A Planet-type object containing methods and attributes for Terrestrial planets.

    Args:
        primary_star (Star):  the Star object around which this object gravitates
        orbit (float): the average orbital radius of this object around its primary_star
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large"

    Attributes:
        primary_star (Star):  the Star object around which this object gravitates
        semi_major_axis (float): the average orbital radius of this object around its primary_star
        size (str): a string corresponding to the size of the object; "Tiny", "Small", "Standard" or "Large"
        temperature (float): the average blackbody temperature of this object
        type (str): a string corresponding to the type of object; i.e. "Gas Giant" or "Hadean"
        moons (list[int]): a list containing the number of moons, major moons, or moonlets of this object
        major_moons (list[MajorMoon]): a list containing the MajorMoon objects in rotation around this object
        is_retrograde_orbit (bool): whether or not this object rotations opposite  of its primary_star
        atmospheric_mass (float): the rough estimate of gaseous volatiles in this objects atmosphere
        atmospheric_composition (list[str]): a list of strings describing the breathability of this objects atompshere
        hydrographic_coverage (float): a float from 0 to 1 describing the percentage of the object covered in water
        surface_temperature (float): the average surface temperature of the object
        climate_type (str):  a string describing the average climate of this object
        density (float):  the density of this object in relation to the Earths density
        diameter (float): the diameter of this object in relation to the Earths diameter
        surface_gravity (float): the gravity at this objects surface in relation to the Earths gravity
        mass (float): the mass of the object in relation to the Earths mass
        orbital_period (float): the average orbital period of this object around its primary_star
        orbital_eccentricity (float): the eccentricity of this objects orbit aroudn its primary_star
        total_tidal_effect (int): an int used in calculating tidal effects on this object
        rotation_period (float): the average orbital period of this object around its primary_star
        is_tidally_locked (bool): whether or not this object is tidally locked to its primary_star
        axial_tilt (int): the axial tilt of this object in degrees
        apparent_length (float): the length of a 'day' on this object
        volcanic_activity (str): a string describing the level of volcanic activity on this object
        tectonic_activity (str): a string describing the level of tectonic activity on this object
    """

    def __init__(self, primary_star: Star, orbit: float, size: str) -> None:
        Planet.__init__(self, primary_star, orbit, size)

        self.atmospheric_mass = self.generate_atmospheric_mass()
        self.atmospheric_composition = self.generate_atmospheric_composition()
        self.hydrographic_coverage = self.generate_hydrographic_coverage()
        self.surface_temperature = self.calculate_surface_temperature()
        self.climate_type = self.calculate_climate_type()

        self.density = self.generate_density()
        self.diameter = self.generate_diameter()
        self.surface_gravity = self.calculate_surface_gravity()
        self.mass = self.calculate_mass()

        self.orbital_period = self.calculate_planetary_orbital_period()
        self.orbital_eccentricity = self.generate_planetary_orbital_eccentricity()

        self.moons = self.generate_moons()
        self.generate_major_moons()

        self.total_tidal_effect = self.calculate_total_tidal_effect()
        self.rotation_period = self.generate_rotation_period()
        if not self.is_tidally_locked:
            self.axial_tilt = self.generate_axial_tilt()
        self.apparent_length = self.calculate_local_calendar()

        self.volcanic_activity = self.generate_volcanic_activity()
        self.generate_volcanic_atmosphere()
        self.tectonic_activity = self.generate_tectonic_activity()

    def generate_moons(self) -> List[int]:
        """Return a list containing number of moons in each family of satellites"""
        modifier = look_up(
            st.terrestrial_planet_moon_size_modifier, self.semi_major_axis
        )
        if self.size == "Tiny":
            modifier -= 2
        elif self.size == "Small":
            modifier -= 1
        elif self.size == "Large":
            modifier += 1
        major_moons = max(roll_dice(1, -4 + modifier), 0)
        moonlets = 0 if major_moons > 0 else max(roll_dice(1, -2 + modifier), 0)
        return [moonlets, major_moons]

    def calculate_rotational_period_modifier(self) -> int:
        """Return the modifier to the Terrestrial rotation period"""
        modifier = 0
        if self.size == "Large":
            modifier = 6
        elif self.size == "Standard":
            modifier = 10
        elif self.size == "Small":
            modifier = 14
        elif self.size == "Tiny":
            modifier = 18
        return modifier

    def generate_rotation_period(self) -> Union[int, float]:
        """Return the rotation period of the Terrestrial"""
        rotation_period_roll = roll_dice(3)
        rotation_period = (
            self.total_tidal_effect
            + rotation_period_roll
            + self.calculate_rotational_period_modifier()
        )
        if rotation_period_roll >= 16 or rotation_period > 36:
            special_rotation_roll = roll_dice(2)
            if special_rotation_roll > 6:
                rotation_period = look_up(
                    wt.special_rotation_tree, special_rotation_roll
                )
        if (
            self.total_tidal_effect >= 50
            or rotation_period > self.orbital_period * 365.26
        ):
            self.is_tidally_locked = True
            rotation_period = self.orbital_period * 365.26
        return rotation_period

    def generate_volcanic_activity(self) -> str:
        """Return the level of volcanic activity of a planet"""
        modifier = round(40 * (self.surface_gravity / self.primary_star.age))
        if self.type == "Tiny (Sulfur)":
            modifier += 60
        if len(self.major_moons) == 1:
            modifier += 5
        elif len(self.major_moons) > 1:
            modifier += 10
        volcanic_activity = look_up(wt.volcanic_activity_tree, roll_dice(3, modifier))
        return volcanic_activity


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

    def __init__(
        self, is_in_open_cluster: bool = False, guarantee_garden_world: bool = False
    ) -> None:
        self.number_of_stars = self.generate_number_of_stars(is_in_open_cluster)
        self.stars = self.generate_stars(guarantee_garden_world)

        self.forbidden_zone = self.calculate_forbidden_zone()

        self.gas_giants = self.calculate_gas_giants()
        self.set_gas_giant_arrangements()

        self.orbits = self.calculate_first_orbit()
        self.calculate_orbits()
        self.place_gas_giants()
        self.fill_remaining_orbits()

    def generate_number_of_stars(self, is_in_open_cluster: bool) -> int:
        """Return a randomly generated number of stars"""
        return look_up(
            st.multiple_stars_tree, roll_dice(3, 3 if is_in_open_cluster else 0)
        )

    def generate_stars(self, guarantee_garden_world: bool) -> List[Star]:
        """Return a list containing randomly generated Star objects"""
        stars = []
        for i in range(self.number_of_stars):
            if i > 0:
                stars.append(CompanionStar(designation=i, primary_star=stars[0]))
            else:
                stars.append(Star(guarantee_garden_world=guarantee_garden_world))
        return stars

    def calculate_forbidden_zone(self) -> List[float]:
        """Return a list containing points designating a system forbidden zone"""
        forbidden_zone = []
        for star in self.stars:
            if type(star) == CompanionStar:
                forbidden_zone.append(
                    [
                        ((1 - star.eccentricity) * star.semi_major_axis) / 3,
                        ((1 + star.eccentricity) * star.semi_major_axis) * 3,
                    ]
                )
        return forbidden_zone

    def in_forbidden_zone(self, radius: float) -> bool:
        """Return whether or not a given radius falls within a set of forbidden zones"""
        for inner_radius, outer_radius in self.forbidden_zone:
            if radius >= inner_radius and radius <= outer_radius:
                return True
        return False

    def calculate_gas_giants(self) -> List[str]:
        """Return a list of gas giant arrangement corresponding to each star in system"""
        gas_giants = []
        for star in self.stars:
            if self.in_forbidden_zone(star.snow_line_radius):
                gas_giants.append("No Gas Giant")
                continue
            else:
                gas_giants.append(look_up(st.gas_giant_arrangement_tree, roll_dice(3)))
        return gas_giants

    def set_gas_giant_arrangements(self) -> None:
        """Set the gas_giant_arrangement attribute in systems Star objects"""
        for idx, star in enumerate(self.stars):
            star.gas_giant_arrangement = self.gas_giants[idx]

    def calculate_first_orbit(self) -> List[Any]:
        """Return a list containing stars and their corresponding first gas giant orbit"""
        orbits = []
        for star in self.stars:
            orbit = [star]
            if star.gas_giant_arrangement == "Conventional Gas Giant":
                orbit.append(
                    [(1 + roll_dice(2, -2) * 0.05) * star.snow_line_radius, "Gas Giant"]
                )
            elif star.gas_giant_arrangement == "Eccentric Gas Giant":
                orbit.append(
                    [(roll_dice(1) * 0.125) * star.snow_line_radius, "Gas Giant"]
                )
            elif star.gas_giant_arrangement == "Epistellar Gas Giant":
                orbit.append(
                    [(1 + roll_dice(3) * 0.1) * star.inner_limit_radius, "Gas Giant"]
                )
            orbits.append(orbit)
        return orbits

    # Man this is just gross looking
    def calculate_orbits(self) -> Any:
        """Returns the given 'orbits' object with a systems full orbital radii"""
        for orbit in self.orbits:
            if len(orbit) > 1:
                temp_radius = orbit[1][0]
            else:
                temp_radius = orbit[0].outer_limit_radius / (1 + 0.05 * roll_dice(1))
                if not self.in_forbidden_zone(temp_radius):
                    orbit.append([temp_radius])
            while True:
                if (
                    temp_radius / look_up(st.orbital_spacing_tree, roll_dice(3))
                    > temp_radius - 0.15
                ):
                    temp_radius = temp_radius - 0.15
                else:
                    temp_radius = temp_radius / look_up(
                        st.orbital_spacing_tree, roll_dice(3)
                    )
                if (
                    not self.in_forbidden_zone(temp_radius)
                    and temp_radius >= orbit[0].inner_limit_radius
                ):
                    orbit.append([temp_radius])
                if temp_radius >= orbit[0].inner_limit_radius:
                    continue
                else:
                    break
            if len(orbit) > 1:
                temp_radius = orbit[1][0]
            else:
                temp_radius = (1 + 0.05 * roll_dice(1)) / orbit[0].outer_limit_radius
                if not self.in_forbidden_zone(temp_radius):
                    orbit.append([temp_radius])
            while True:
                if (
                    temp_radius * look_up(st.orbital_spacing_tree, roll_dice(3))
                    < temp_radius + 0.15
                ):
                    temp_radius = temp_radius + 0.15
                else:
                    temp_radius = temp_radius * look_up(
                        st.orbital_spacing_tree, roll_dice(3)
                    )
                if (
                    not self.in_forbidden_zone(temp_radius)
                    and temp_radius <= orbit[0].outer_limit_radius
                ):
                    orbit.append([temp_radius])
                if temp_radius <= orbit[0].outer_limit_radius:
                    continue
                else:
                    break
            if len(orbit) > 1:
                orbit[1:] = sorted(orbit[1:])

    def place_gas_giants(self) -> Any:
        """Returns the given 'orbits' object with GasGiant objects assigned"""
        for idx, orbit in enumerate(self.orbits):
            if self.gas_giants[idx] == "No Gas Giant":
                continue
            for i in range(1, len(orbit)):
                # I am assuming that this is the pre-assigned gas giant and that it is either inside
                #   the snow line or is the first orbit beyond the snow line
                if len(orbit[i]) > 1 and orbit[i][1] == "Gas Giant":
                    orbit[i][1] = GasGiant(
                        orbit[0],
                        orbit[i][0],
                        look_up(st.gas_giant_size_tree, roll_dice(3, 4)),
                    )
                    continue
                if (
                    self.gas_giants[idx] == "Conventional Gas Giant"
                    and orbit[i][0] >= orbit[0].snow_line_radius
                    and roll_dice(3) <= 15
                ):
                    orbit[i].append(
                        GasGiant(
                            orbit[0],
                            orbit[i][0],
                            look_up(st.gas_giant_size_tree, roll_dice(3)),
                        )
                    )
                elif self.gas_giants[idx] == "Eccentric Gas Giant" and (
                    (orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 14)
                    or (orbit[i][0] <= orbit[0].snow_line_radius and roll_dice(3) <= 8)
                ):
                    orbit[i].append(
                        GasGiant(
                            orbit[0],
                            orbit[i][0],
                            look_up(
                                st.gas_giant_size_tree,
                                roll_dice(
                                    3,
                                    4
                                    if orbit[i][0] <= orbit[0].snow_line_radius
                                    else 0,
                                ),
                            ),
                        )
                    )
                elif self.gas_giants[idx] == "Epistellar Gas Giant" and (
                    (orbit[i][0] >= orbit[0].snow_line_radius and roll_dice(3) <= 14)
                    or (orbit[i][0] <= orbit[0].snow_line_radius and roll_dice(3) <= 6)
                ):
                    orbit[i].append(
                        GasGiant(
                            orbit[0],
                            orbit[i][0],
                            look_up(
                                st.gas_giant_size_tree,
                                roll_dice(
                                    3,
                                    4
                                    if orbit[i][0] <= orbit[0].snow_line_radius
                                    else 0,
                                ),
                            ),
                        )
                    )

    def fill_remaining_orbits(self) -> Any:
        """Returns the given 'orbits' object with the remaining radii filled"""
        for orbit in self.orbits:
            for i in range(1, len(orbit)):
                if len(orbit[i]) > 1:
                    continue
                modifier = 0
                # this should find the closest radii to the inner and outer limit radii
                if (
                    orbit[i][0]
                    == min(
                        orbit[1:], key=lambda x: abs(x[0] - orbit[0].inner_limit_radius)
                    )[0]
                    or orbit[i][0]
                    == min(
                        orbit[1:], key=lambda x: abs(x[0] - orbit[0].outer_limit_radius)
                    )[0]
                ):
                    modifier = modifier - 3
                # this should find if the next orbit is a gas giant
                if (
                    i < len(orbit) - 1
                    and len(orbit[i + 1]) > 1
                    and type(orbit[i + 1][1]) == GasGiant
                ):
                    modifier = modifier - 6
                # this should find if the previous orbit is a gas giant
                if (
                    i > 1
                    and len(orbit[i - 1]) > 1
                    and type(orbit[i - 1][1]) == GasGiant
                ):
                    modifier = modifier - 3
                # this should find the radii closest to the forbidden zone limits
                for zone in self.forbidden_zone:
                    if (
                        orbit[i][0]
                        == min(orbit[1:], key=lambda x: abs(x[0] - zone[0]))[0]
                        or orbit[i][0]
                        == min(orbit[1:], key=lambda x: abs(x[0] - zone[1]))[0]
                    ):
                        modifier = modifier - 6
                        break
                roll = roll_dice(3, modifier)
                orbit_contents = look_up(st.orbit_contents_tree, roll)
                if type(orbit_contents) == list:
                    orbit[i].append(
                        Terrestrial(orbit[0], orbit[i][0], orbit_contents[1])
                    )
                else:
                    orbit[i].append(orbit_contents)
