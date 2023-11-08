import os
from typing import Tuple
from selenium.webdriver.common.options import ArgOptions
import pandas as pd
from pandas import DataFrame

from selenium_automation import SelTrebuchet

parent_directory = os.path.dirname(os.path.abspath(__file__))
valid_headers = {'rel angle', 'length short arm', 'mass of wt'}


def run_design(design: DataFrame, browser: str = 'firefox', options: ArgOptions = None) -> DataFrame:
    distance, height, time = [0] * design.shape[0], [0] * design.shape[0], [0] * design.shape[0]
    with SelTrebuchet(browser, options=options) as trebuchet:
        for idx, row in design.iterrows():
            distance[idx], height[idx], time[idx] = trebuchet.simulate(release_angle=row['rel angle'],
                                                                       shortarm_len=row['length short arm'],
                                                                       weight_mass=row['mass of wt'])

    design['distance'], design['height'], design['time'] = distance, height, time
    return design


def load_design(design_path: str) -> DataFrame:
    return pd.read_excel(design_path)


def validate_design(design: DataFrame) -> Tuple[bool, str]:
    for header in design.columns:
        if header not in valid_headers:
            return False, f'"{header}" is not a valid header'
    return True, ''
