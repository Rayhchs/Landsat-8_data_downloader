"""
Created on Fri Sep  4 16:36:17 2021
simple
@author: Ray
"""
from __future__ import print_function
from argparse import ArgumentParser
import sys
import os
from utils.utils import *
from shapely.geometry import box
import pandas as pd
from fiona.crs import from_epsg
import geopandas as gpd

parser = ArgumentParser(description="Landsat-8 satellite image downloader")
parser.add_argument("position", help="Min longtitude, Max longtitude, Min latitude, Max latitude", nargs='+', type=float)
parser.add_argument("-c", "--cloud_cover", help="Cloud cover", type=int, default = 10, dest = "cloud")
parser.add_argument("-n", "--num_of_data", help="How many data to download", type=int, default=10, dest="num")
args = parser.parse_args()

def main():
    
    bbox = box(args.position[0], args.position[2], args.position[1], args.position[3])
    bounds = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))
    
    # System parameters
    surveyed = data_survey(bounds, args.cloud, args.num)
    survey = surveyed.find_current_image()
    
    sys.exit("Found no data") if len(survey) == 0 else print(f"Found {survey} data")
    
    # Download
    download_path = []
    for i in range(args.num):
        download = []
        download.append(survey.iloc[i])
        download_frame = pd.concat(download, 1).T
        downloaded = data_downloader(download_frame)
        download_path.append(downloaded.output_dir())
        print("Saved in {}".format(downloaded.output_dir()))
        
if __name__ == '__main__':
    main()
