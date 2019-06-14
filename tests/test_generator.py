import unittest
from unittest.mock import patch
import math

from stargen import generator


class TestStar(unittest.TestCase):
    def test_star_stellar_sequence(self):
        data = [
            [0.1, 10.0, "V"],
            [1.0, 10.0, "V"],
            [1.0, 11.5, "IV"],
            [1.0, 12.5, "III"],
            [1.0, 13.5, "D"],
        ]
        for mass, age, sequence in data:
            with self.subTest(mass=mass, age=age, sequence=sequence):
                self.mass = mass
                self.age = age
                self.assertAlmostEqual(
                    generator.Star.calculate_stellar_sequence(self), sequence
                )

    def test_star_stellar_temperature(self):
        data = [
            [1.0, "V", 10.0, 5800.0],
            [1.0, "IV", 11.5, 4862.5],
            [1.0, "D", 13.5, None],
        ]
        for mass, sequence, age, temperature in data:
            with self.subTest(
                mass=mass, sequence=sequence, age=age, temperature=temperature
            ):
                self.mass = mass
                self.sequence = sequence
                self.age = age
                self.assertAlmostEqual(
                    generator.Star.calculate_stellar_temperature(self), temperature
                )

    def test_star_stellar_luminosity(self):
        data = [
            [0.1, "V", 10.0, 0.0012],
            [1.0, "V", 10.0, 1.6],
            [1.0, "IV", 11.5, 1.6],
            [1.0, "III", 12.5, 40.0],
            [1.0, "D", 13.5, 0.001],
        ]
        for mass, sequence, age, luminosity in data:
            with self.subTest(
                mass=mass, sequence=sequence, age=age, luminosity=luminosity
            ):
                self.mass = mass
                self.sequence = sequence
                self.age = age
                self.assertAlmostEqual(
                    generator.Star.calculate_stellar_luminosity(self), luminosity
                )

    def test_star_stellar_radius(self):
        data = [[5800.0, 1.6, 0.0058], [None, 0.001, None]]
        for temperature, luminosity, radius in data:
            with self.subTest(
                temperature=temperature, luminosity=luminosity, radius=radius
            ):
                self.temperature = temperature
                self.luminosity = luminosity
                self.assertAlmostEqual(
                    generator.Star.calculate_stellar_radius(self), radius
                )

    def test_star_inner_limit_radius(self):
        data = [[0.1, 0.0012, 0.01], [1.0, 1.6, 0.1], [2.0, 20, 0.2]]
        for mass, luminosity, inner_limit_radius in data:
            with self.subTest(
                mass=mass, luminosity=luminosity, inner_limit_radius=inner_limit_radius
            ):
                self.mass = mass
                self.luminosity = luminosity
                self.assertAlmostEqual(
                    generator.Star.calculate_inner_limit_radius(self),
                    inner_limit_radius,
                )

    def test_star_outer_limit_radius(self):
        data = [[0.1, 4.0], [1.0, 40.0], [2.0, 80.0]]
        for mass, outer_limit_radius in data:
            with self.subTest(mass=mass, outer_limit_radius=outer_limit_radius):
                self.mass = mass
                self.assertAlmostEqual(
                    generator.Star.calculate_outer_limit_radius(self),
                    outer_limit_radius,
                )

    def test_star_snow_line_radius(self):
        data = [[0.10, 0.168], [1.00, 3.999], [2.00, 19.4]]
        for mass, snow_line_radius in data:
            with self.subTest(mass=mass, snow_line_radius=snow_line_radius):
                self.mass = mass
                self.assertAlmostEqual(
                    generator.Star.calculate_snow_line_radius(self), snow_line_radius
                )


class TestCompanionStar(unittest.TestCase):
    @patch("stargen.generator.Star")
    
    def test_companion_star_generate_companion_mass(self, mock_star):
        self.primary_star = mock_star
        data = [
            [[0, 3], 1.0, 1.0],
            [[2, 6], 1.0, 0.7],
            [[3, 9], 1.0, 0.55],
            [[5, 25], 2.0, 0.5],
            [[4, 12], 0.5, 0.10],
        ]
        for dice_rolls, primary_star_mass, companion_star_mass in data:
            with self.subTest(
                dice_rolls=dice_rolls,
                primary_star_mass=primary_star_mass,
                companion_star_mass=companion_star_mass,
            ):
                generator.roll_dice = lambda n, m=0: dice_rolls.pop(0)
                self.primary_star.mass = primary_star_mass
                self.assertAlmostEqual(
                    generator.CompanionStar.generate_companion_mass(self),
                    companion_star_mass,
                )
