import unittest
from selenium.webdriver.common.keys import Keys

from selenium_automation import SelTrebuchet


class TestSelTrebuchet(unittest.TestCase):
    def test_simulate_with_params(self):
        # Create a SelTrebuchet instance for testing
        with SelTrebuchet(browser='firefox') as trebuchet:
            len_shortarm = 1.0
            mass_weight = 50.0
            angle_release = 60.0

            distance, height, time = trebuchet.simulate(
                len_shortarm, mass_weight, angle_release)

        self.assertAlmostEqual(distance, 44.546, places=1)
        self.assertAlmostEqual(height, 34.870, places=1)
        self.assertAlmostEqual(time, 4.033, places=1)


if __name__ == '__main__':
    unittest.main()
