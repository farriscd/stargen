import unittest
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
                self.assertEqual(
                    generator.Star.calculate_stellar_sequence(self, mass, age), sequence
                )

    def test_star_stellar_temperature(self):
        data = [
            [1.0, 10.0, "V", 5800.0],
            [1.0, 11.5, "IV", 4862.5],
            [1.0, 13.5, "D", None],
        ]
        for mass, age, sequence, temperature in data:
            with self.subTest(
                mass=mass, age=age, sequence=sequence, temperature=temperature
            ):
                self.assertEqual(
                    generator.Star.calculate_stellar_temperature(
                        self, mass, age, sequence
                    ),
                    temperature,
                )

    def test_star_stellar_luminosity(self):
        data = [
            [0.1, 10.0, "V", 0.0012],
            [1.0, 10.0, "V", 1.6],
            [1.0, 11.5, "IV", 1.6],
            [1.0, 12.5, "III", 40.0],
            [1.0, 13.5, "D", 0.001],
        ]
        for mass, age, sequence, luminosity in data:
            with self.subTest(
                mass=mass, age=age, sequence=sequence, luminosity=luminosity
            ):
                self.assertEqual(
                    generator.Star.calculate_stellar_luminosity(
                        self, mass, age, sequence
                    ),
                    luminosity,
                )

    def test_star_stellar_radius(self):
        data = [[5800.0, 1.6, 0.0058], [None, 0.001, None]]
        for temperature, luminosity, radius in data:
            with self.subTest(
                temperature=temperature, luminosity=luminosity, radius=radius
            ):
                self.assertEqual(
                    generator.Star.calculate_stellar_radius(
                        self, temperature, luminosity
                    ),
                    radius,
                )

    def test_star_inner_limit_radius(self):
        data = [[0.1, 0.0012, 0.01], [1.0, 1.6, 0.1], [2.0, 20, 0.2]]
        for mass, luminosity, inner_limit_radius in data:
            with self.subTest(
                mass=mass, luminosity=luminosity, inner_limit_radius=inner_limit_radius
            ):
                self.assertEqual(
                    generator.Star.calculate_inner_limit_radius(self, mass, luminosity),
                    inner_limit_radius,
                )

    def test_star_outer_limit_radius(self):
        data = [[0.1, 4.0], [1.0, 40.0], [2.0, 80.0]]
        for mass, outer_limit_radius in data:
            with self.subTest(mass=mass, outer_limit_radius=outer_limit_radius):
                self.assertEqual(
                    generator.Star.calculate_outer_limit_radius(self, mass),
                    outer_limit_radius,
                )

    def test_star_snow_line_radius(self):
        data = [[0.0012, 0.168], [0.68, 3.999], [16, 19.4]]
        for l_min, snow_line_radius in data:
            with self.subTest(l_min=l_min, snow_line_radius=snow_line_radius):
                self.assertEqual(
                    generator.Star.calculate_snow_line_radius(self, l_min),
                    snow_line_radius,
                )
