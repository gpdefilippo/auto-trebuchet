import os
from typing import Tuple
from selenium.webdriver.common.options import ArgOptions
import pandas as pd
from pandas import DataFrame

from selenium_automation import SelTrebuchet

parent_directory = os.path.dirname(os.path.abspath(__file__))
valid_headers = {
    'lengthArmShort',
    'lengthArmLong',
    'lengthSling',
    'lengthWeight',
    'heightOfPivot',
    'massArm',
    'inertiaArm',
    'pivotToArmCG',
    'massWeight',
    'inertiaWeight',
    'massProjectile',
    'projectileDiameter',
    'windSpeed',
    'releaseAngle',
    'distance',
    'height',
    'time',
}


def run_design(design: DataFrame, browser: str = 'firefox', options: ArgOptions = None) -> DataFrame:
    excluded = {'distance', 'height', 'time'}
    distance, height, time = [0] * design.shape[0], [0] * design.shape[0], [0] * design.shape[0]
    with SelTrebuchet(browser, options=options) as trebuchet:
        for idx, row in design.iterrows():
            cols = [col for col in design.columns if col not in excluded]
            params = row[cols].to_dict()
            distance[idx], height[idx], time[idx] = trebuchet.simulate(params)

    design['distance'], design['height'], design['time'] = distance, height, time
    return design


def load_design(design_path: str) -> DataFrame:
    return pd.read_excel(design_path)


def validate_design(design: DataFrame) -> Tuple[bool, str]:
    for header in design.columns:
        if header not in valid_headers:
            return False, f'"{header}" is not a valid header'
    return True, ''
