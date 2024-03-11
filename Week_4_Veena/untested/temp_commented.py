# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# make necessary imports
import fiftyone as fo
import os
import pdb
import pandas as pd
import numpy as np


# define the paths to datasets as well as their file extensions
# root_1='/home/bshi/Documents/Patrick_CVAT_dataset'
root_1 = r"C:\Users\veena\Downloads\missing_data\Patrick_CVAT_dataset"
# root_2='/home/bshi/Tucker_annotation_validation/'
root_2 = r"c:\Users\veena\Downloads\missing_data\Tucker_annotation_validation"
images_start=['train/images/', 'valid/images/']
labels_start=['train/labels/', 'valid/labels/']
image_end='.jpg'
label_end='.txt'

# define annotators
annotator1='Bree'
annotator2='Tucker'

# define a function to associate label files with image files
def associate_files(paths):
    array=[]
    label=[]
    location=[]
    for i in paths:
        file = open(i, 'r')
        data1=[]
        data2=[]
        for line in file:
            data=[float(x) for x in line.strip().split(' ')]
            data1.append(int(data[0]))
            data2.append(data[1:])
        label.append(data1)
        location.append(data2)
        file.close()
    
    # check if the defference in locations between annotators is within a threshold
    # Optimization: Broke up the code for readability
    diff = np.sum(np.abs(locations[0] - locations[1]))
    if diff < 0.05:
        print(diff)
        return label
    else:
        # otherwise initiate debugging mode
        pdb.set_trace()
        return []  # Return an empty list if the condition is not met


# load the dataset using FiftyOne import
name = "master_dataset"
dataset_dir = r"C:\Users\veena\Downloads\week1_data\week1_data\master_dataset"

# Create the dataset
master_dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.FiftyOneDataset,
    name=name,
)
# dataset = load_dataset_from_dir(r"C:\Users\veena\Downloads\week1_data\week1_data\master_dataset", "master_dataset")
dataset = fo.load_dataset("master_dataset")

# initialize counters and a DataFrame
out_count=0
a_df = pd.DataFrame(columns=['trialid', 'imageid', 'detectionid', annotator1, annotator2])

# Iterate over each sample in the dataset
for sample in dataset:
    data = None
    # check if image files exist for both annotators
    if os.path.exists(root_1+images_start[0]+sample.image_uid+image_end):
        if os.path.exists(root_2+images_start[0]+sample.image_uid+image_end):
            # define paths for label files
            path1=root_1+labels_start[0]+sample.image_uid+label_end
            path2=root_2+labels_start[0]+sample.image_uid+label_end
            paths=[path1,path2]
            # associate label files with image files
            data=associate_files(paths)
        else:
            print('something is wrong here 1')
            print(sample)
    elif os.path.exists(root_1+images_start[1]+sample.image_uid+image_end):
        if os.path.exists(root_2+images_start[1]+sample.image_uid+image_end):
            # define paths for label files
            path1=root_1+labels_start[1]+sample.image_uid+label_end
            path2=root_2+labels_start[1]+sample.image_uid+label_end
            paths=[path1,path2]
            # associate label files with image files once more
            data=associate_files(paths)
        else:
            print('something is wrong here 2')
            print(sample)
    else:
        out_count+=1

    # Extract the number of detections and labels for each annotator
    detection_num=len(data[0])
    label1=data[0]
    label2=data[1]

    # Iterate over each detection and create a new associated row in the DataFrame
    for i in range(detection_num):
        new_row = {'trialid': sample.projectID, 'imageid': sample.image_uid, 'detectionid': i, annotator1: label1[i], annotator2: label2[i]}
        a_df = pd.concat([a_df, pd.DataFrame([new_row])], ignore_index=True)

a_df['Bree'] = a_df['Bree'].astype(int)
a_df['Patrick'] = a_df['Patrick'].astype(int)

# Calculate the absolute difference between annotators' labels
a_df['difference']=abs(a_df.Bree-a_df.Tucker)

# calculate accuracy per trial
df1 = a_df.groupby('trialid')['difference'].sum()
df2 = a_df.groupby('trialid')['trialid'].count()
acc=[1]*len(df1.values)-(df1.values/df2.values)

# create DataFrame for accuracy results
df=pd.DataFrame(columns=['trial', 'acc'])
df['trial']=list(df1.index)
df['acc']=acc

# Filter DataFrame for detections with a difference of 1
sub_df=a_df[a_df.difference==1]
sub_df.groupby(['trialid', 'Bree'])[['Bree','Tucker']].count()
