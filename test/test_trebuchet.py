import unittest
import os
import pandas as pd

from trebuchet import run_design


class TestTrebuchet(unittest.TestCase):

    def setUp(self) -> None:
        parent = os.path.dirname(os.path.abspath(__file__))

        sample_data_path = os.path.join(parent, 'data', 'sample_data.xlsx')
        self.sample_data = pd.read_excel(sample_data_path)

        sample_results_path = os.path.join(parent, 'data', 'sample_results.xlsx')
        self.sample_results = pd.read_excel(sample_results_path)

    def _test_run_design(self, browser: str):
        act_results = run_design(self.sample_data, browser=browser)
        act_distance, act_height, act_time = act_results["distance"], act_results["height"], act_results["time"]

        exp_distance, exp_height, exp_time = self.sample_results["distance"], \
            self.sample_results["height"], self.sample_results["time"]

        tolerance = 0.5

        distance_equal = [abs(a - b) < tolerance for a, b in zip(act_distance, exp_distance)]
        height_equal = [abs(a - b) < tolerance for a, b in zip(act_height, exp_height)]
        time_equal = [abs(a - b) < tolerance for a, b in zip(act_time, exp_time)]

        self.assertTrue(all(distance_equal))
        self.assertTrue(all(height_equal))
        self.assertTrue(all(time_equal))

    def test_run_design_chrome(self):
        self._test_run_design(browser='chrome')

    def test_run_design_firefox(self):
        self._test_run_design(browser='firefox')

    @unittest.skip("Skipping due to Edge giving problems w/ Github Actions")
    def test_run_design_edge(self):
        self._test_run_design(browser='edge')


if __name__ == '__main__':
    unittest.main()
