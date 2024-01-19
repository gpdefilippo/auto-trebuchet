import unittest

from selenium_automation import SelTrebuchet


class TestSelTrebuchet(unittest.TestCase):
    def test_simulate_firefox(self):
        with SelTrebuchet(browser='firefox') as trebuchet:
            params = {
                'lengthArmShort': 1.0,
                'massWeight': 50.0,
                'releaseAngle': 60.0,
            }

            distance, height, time = trebuchet.simulate(params)

        self.assertAlmostEqual(distance, 44.546, places=1)
        self.assertAlmostEqual(height, 34.870, places=1)
        self.assertAlmostEqual(time, 4.033, places=1)

    def test_simulate_chrome(self):
        with SelTrebuchet(browser='chrome') as trebuchet:
            params = {
                'lengthArmShort': 1.0,
                'massWeight': 50.0,
                'releaseAngle': 60.0,
            }

            distance, height, time = trebuchet.simulate(params)

        self.assertAlmostEqual(distance, 44.546, places=1)
        self.assertAlmostEqual(height, 34.870, places=1)
        self.assertAlmostEqual(time, 4.033, places=1)

    @unittest.skip("Skipping due to Edge giving problems w/ Github Actions")
    def test_simulate_edge(self):
        with SelTrebuchet(browser='edge') as trebuchet:
            params = {
                'lengthArmShort': 1.0,
                'massWeight': 50.0,
                'releaseAngle': 60.0,
            }

            distance, height, time = trebuchet.simulate(params)

        self.assertAlmostEqual(distance, 44.546, places=1)
        self.assertAlmostEqual(height, 34.870, places=1)
        self.assertAlmostEqual(time, 4.033, places=1)


if __name__ == '__main__':
    unittest.main()
