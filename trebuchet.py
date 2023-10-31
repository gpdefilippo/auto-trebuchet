import os
import pandas as pd

from selenium_automation import SelTrebuchet

design_file = 'CCF desing 10 29.xlsx'


def run_design(design_file: str) -> None:
    out_path = os.path.join('results', design_file)
    design_path = os.path.join('designs', design_file)
    design = pd.read_excel(design_path)

    distance, height, time = [0] * design.shape[0], [0] * design.shape[0], [0] * design.shape[0]
    with SelTrebuchet('firefox') as trebuchet:
        for idx, row in design.iterrows():
            distance[idx], height[idx], time[idx] = trebuchet.simulate(row['rel angle'], row['length short arm'],
                                                                       row['mass of wt'])

    design['distance'], design['height'], design['time'] = distance, height, time

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    design.to_excel(out_path, index=False)


if __name__ == "__main__":
    run_design(design_file)
