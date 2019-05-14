import unittest

import stargen

class TestStar(unittest.TestCase):
    def test_star_stellar_sequence(self):
        data = [[0.1, 10.0, "V"], [1.0, 10.0, "V"], [1.0, 11.5, "IV"], [1.0, 12.5, "III"], [1.0, 13.5, "D"]]
        for mass, age, sequence in data:
            with self.subTest(mass=mass, age=age, sequence=sequence):
                self.assertEqual(stargen.Star.calculate_stellar_sequence(self, mass, age), sequence)

    def test_star_stellar_temperature(self):
        data = [[1.0, 10.0, "V", 5800], [1.0, 11.5, "IV", 4862.5], [1.0, 13.5, "D", None]]
        for mass, age, sequence, temperature in data:
            with self.subTest(mass=mass, age=age, sequence=sequence, temperature=temperature):
                self.assertEqual(stargen.Star.calculate_stellar_temperature(self, mass, age, sequence), temperature)

    def test_star_stellar_luminosity(self):
        data = [[0.1, 10, "V", 0.0012], [1.0, 10, "V", 1.6], [1.0, 11.5, "IV", 1.6], [1.0, 12.5, "III", 40], [1.0, 13.5, "D", 0.001]]
        for mass, age, sequence, luminosity in data:
            with self.subTest(mass=mass, age=age, sequence=sequence, luminosity=luminosity):
                self.assertEqual(stargen.Star.calculate_stellar_luminosity(self, mass, age, sequence), luminosity)

    def test_star_stellar_radius(self):
        data = [[5800, 1.6, 0.0058], [None, 0.001, None]]
        for temperature, luminosity, radius in data:
            with self.subTest(temperature=temperature, luminosity=luminosity, radius=radius):
                self.assertEqual(stargen.Star.calculate_stellar_radius(self, temperature, luminosity), radius)

if __name__ == "__main__":
    unittest.main()
