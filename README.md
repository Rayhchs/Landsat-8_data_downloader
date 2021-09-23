# Landsat-8 data downloader
This repo constructs a GUI to search and download the Landsat-8 satellite data from AWS: https://registry.opendata.aws/landsat-8/.  The GUI needs users to define cloud coverage, number of data, and coordinate when searching the data. Users can search data by giving those parameters. Afterward, users can select and download the data. Also, a simply version (without search function) for using is uploaded. It provides users to download latest satellite images from giving coordinate, cloud coverage and numbers of data to download.

## Requisite
python 3.8

## Getting Started
Tips about building environment are described in howtouse.txt
* Clone repository

      git clone https://github.com/Rayhchs/Landsat-8_data_downloader.git
      cd Landsat-8_data_downloader
      
* Usage

      python -m GUI
      
 The interface:
 
 <img src="https://github.com/Rayhchs/Landsat-8_data_downloader/blob/main/GUI_ex.png" alt="Editor" width="600" title="GUI">
 
 The searching interface, in here you can select multiple data for downloading.
 
 <img src="https://github.com/Rayhchs/Landsat-8_data_downloader/blob/main/GUI_ex2.png" alt="Editor" width="250" title="Searching panel">
      
* For simple usage

      python -m solution <Min longtitude> <Max longtitude> <Min latitude> <Max latitude> -c=<cloud coverage> -n=<number of data>
  
 The users need to input position where you want to download images, cloud coverage, number of data to download.
 
 
 | Positional arguments | Description |
 | ------------- | ------------- |
 | Coordinate | Min & Max longtitude, Min & Max latitude |
 
 | Optional arguments | prefix_char | Description |
 | ------------- | ------------- |------------- |
 | --cloud_cover | -c | cloud coverage (1~100) |
 | --num_of_data | -n | number of data (within 50) |
 
 ## Reference
 
 https://github.com/awslabs/open-data-docs/tree/main/docs/landsat-pds
