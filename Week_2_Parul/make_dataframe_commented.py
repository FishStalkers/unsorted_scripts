#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:04:51 2023

@author: bshi
"""
# import the necessary library
import pandas as pd

# path to csv file
path='/home/bshi/Temp/CichlidAnalyzer/__ProjectData/Single_nuc_1/MC_singlenuc35_11_Tk61_051220/MasterAnalysisFiles/AllTrackedFish.csv'

# reading the CSV file into the DataFrame
df=pd.read_csv(path)

# Filtering the DataFrame to contain only rows where 'track_id' is equal to 6
df=df[df.track_id==6]
df.track_length.min()

# List of clumn names for the new DataFrame
columns = ['trial', 'sframe', 'eframe']

# Create an empty DataFrame with specified columns
df = pd.DataFrame(columns=columns)

# Saving the empty DataFrame to a CSV file
df.to_csv('~/last_hour_frame_data.csv')


