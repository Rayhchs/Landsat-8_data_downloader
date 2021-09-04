"""
Created on Fri Sep  3 15:26:37 2021

utils

@author: Ray
"""
import pandas as pd
import geopandas as gpd
import os, shutil
import requests
import numpy as np
from bs4 import BeautifulSoup 

class data_survey():
    
    def __init__(self, bounds, cloud_cover, data_num):
        
        self.wrs_path = os.getcwd() + r'\WRS2\WRS2_descending.shp' # WRS2 file
        self.bounds = bounds
        self.cloud_cover = cloud_cover
        self.data_num = data_num
        
    def select_boundary(self):
        
        # Get path and row
        self.wrs = gpd.GeoDataFrame.from_file(self.wrs_path)
        self.wrs_cover = self.wrs[self.wrs.intersects(self.bounds.geometry[0])]
        self.paths, self.rows = self.wrs_cover['PATH'].values,self.wrs_cover['ROW'].values
        
    def find_current_image(self):
        
        self.select_boundary()
        # Read AWS landsat 8 image list
        try:
            self.url = 'http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz'
            self.s3_scenes = pd.read_csv(self.url, compression='gzip')
            
            # Iterate through paths and rows
            for self.path, self.row in zip(self.paths, self.rows):
            
                # Filter the Landsat Google table for images matching path, row.
                scenes = self.s3_scenes[(self.s3_scenes.path == self.path) & (self.s3_scenes.row == self.row) 
                                   & (self.s3_scenes.cloudCover <= self.cloud_cover)] 
                
            # Current files
            self.bulk_frame = scenes.tail(self.data_num)
            return self.bulk_frame
        except:
            return []
        
    
class data_downloader():
    
    def __init__(self, bulk_frame):
        self.LANDSAT_PATH =  os.getcwd()# File storage path
        self.bulk_frame = bulk_frame
        self.download()
    
    def download(self):
        
        # Download and save image files
        for i, self.row in self.bulk_frame.iterrows():
        
            # Request the html text of the download_url from the amazon server. 
            response = requests.get(self.row.download_url)
        
            # If the response status code is fine (200)
            if response.status_code == 200:
        
                # Import the html to beautiful soup
                html = BeautifulSoup(response.content, 'html.parser')
        
                # Create the dir where put these image files.
                self.entity_dir = os.path.join(self.LANDSAT_PATH, self.row.productId)
                os.makedirs(self.entity_dir, exist_ok=True)
        
                # Second loop: for each band of this image that we find using the html <li> tag     
                for li in html.find_all('li'):
        
                    # Get the href tag
                    file = li.find_next('a').get('href')
                    print(file)

                    # Download the files
                    response = requests.get(self.row.download_url.replace('index.html', file), stream=True)
                
                    with open(os.path.join(self.entity_dir, file), 'wb') as output:
                        shutil.copyfileobj(response.raw, output)
                    del response
                            
    def output_dir(self):
        return self.entity_dir
    
    def output_for_test(self):
        return self.entity_dir

# Check is float or not, Used for checking cloud coverage
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False