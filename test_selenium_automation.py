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

            distance, height, time = trebuchet.simulate_with_params(
                len_shortarm, mass_weight, angle_release)

        self.assertEqual(distance, '44.546 ft')
        self.assertEqual(height, '34.870 ft')
        self.assertEqual(time, '4.033 s')


if __name__ == '__main__':
    unittest.main()
