import os
import pandas as pd

from selenium_automation import SelTrebuchet

parent_directory = os.path.dirname(os.path.abspath(__file__))


def run_design(design_path: str, browser: str = 'firefox') -> None:
    out_path = os.path.join(parent_directory, 'results', os.path.basename(design_path))
    design = pd.read_excel(design_path)

    distance, height, time = [0] * design.shape[0], [0] * design.shape[0], [0] * design.shape[0]
    with SelTrebuchet(browser) as trebuchet:
        for idx, row in design.iterrows():
            distance[idx], height[idx], time[idx] = trebuchet.simulate(row['rel angle'], row['length short arm'],
                                                                       row['mass of wt'])

    design['distance'], design['height'], design['time'] = distance, height, time

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    design.to_excel(out_path, index=False)
