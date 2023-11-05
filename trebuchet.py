import os
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pandas as pd
from pandas import DataFrame

from selenium_automation import SelTrebuchet

parent_directory = os.path.dirname(os.path.abspath(__file__))


def run_design(design_path: str, browser: str = 'firefox', options=None) -> DataFrame:
    out_path = os.path.join(parent_directory, 'results', os.path.basename(design_path))
    design = pd.read_excel(design_path)

    distance, height, time = [0] * design.shape[0], [0] * design.shape[0], [0] * design.shape[0]
    with SelTrebuchet(browser, options=options) as trebuchet:
        for idx, row in design.iterrows():
            distance[idx], height[idx], time[idx] = trebuchet.simulate(release_angle=row['rel angle'],
                                                                       shortarm_len=row['length short arm'],
                                                                       weight_mass=row['mass of wt'])

    design['distance'], design['height'], design['time'] = distance, height, time

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    design.to_excel(out_path, index=False)

    return design
