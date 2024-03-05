#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:04:51 2023

@author: bshi
"""
# import the necessary library
import pandas as pd

# path to csv file
# path='/home/bshi/Temp/CichlidAnalyzer/__ProjectData/Single_nuc_1/MC_singlenuc35_11_Tk61_051220/MasterAnalysisFiles/AllTrackedFish.csv'
path = r"C:\Users\veena\Downloads\missing_data\AllTrackedFish.csv"
# reading the CSV file into the DataFrame
df=pd.read_csv(path)
# Filtering the DataFrame to contain only rows where 'track_id' is equal to 6
df=df[df.track_id==6]
# No such column as track_length but using cvat_analysis_commented.py defintion 
#df.track_length.min()
df = df.groupby('track_id')['track_id'].count().rename('track_length')
# df.min()
min_track_length = df.min()

# List of column names for the new DataFrame
columns = ['trial', 'sframe', 'eframe']

# Create an empty DataFrame with specified columns. Renaming because df already used.
new_df = pd.DataFrame(columns=columns)

# Saving the empty DataFrame to a CSV file
new_df.to_csv('Week_2_Veena/last_hour_frame_data.csv')
