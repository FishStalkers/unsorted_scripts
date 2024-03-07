# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import all the necessary libraries
import fiftyone as fo
import os
import glob
import pdb
import pandas as pd
import numpy as np

# using a function I made last time just for ease of loading
def load_dataset_from_dir(directory, dataset_name):
    dataset = fo.Dataset.from_dir(
        dataset_dir=directory,
        dataset_type=fo.types.FiftyOneDataset,
        name=dataset_name
    )
    return fo.load_dataset(dataset_name)

# defining root directorie sfor datasets as well as other constants
root_1= r"C:\Users\parul\OneDrive - Georgia Institute of Technology\Documents\mcgrath_research\week_2\week_2_data\Patrick_CVAT_dataset"
root_2= r"C:\Users\parul\OneDrive - Georgia Institute of Technology\Documents\mcgrath_research\week_2\week_2_data\Bree_CVAT_dataset"

labels_start='obj_train_data/obj_train_data/'
label_end='.txt'
annotator1='Patrick'
annotator2='Bree'
annotator3='Tucker'

# import the glob module
# the glob module is short for global, and is a function that is used to search for files
# that match a specific file pattern or name, especially for csv or txt files
# optimization 1: deleting these imports because glob and os don't need to be imported twice
# import glob
# import os
# find all text files in either Patrick_CVAT_dataset or Bree_CVAT_dataset directories
text1 = glob.glob(root_1+labels_start+'*.txt')
text2= glob.glob(root_2+labels_start+'*.txt')

# optimization: rewrote the associate_files function with a different imported package in numpy to make it more efficient + less lines
# this is because Using numpy.loadtxt or numpy.genfromtxt for reading data from files directly into NumPy arrays. 
# These functions automatically handle the parsing of floating-point numbers and integers from text files.
def associate_files(paths):
    labels = []
    locations = []
    for path in paths:
        # Assuming each line in the file has an integer followed by space-separated floats
        data = np.loadtxt(path)
        #diagnostics test:
        print(f"Data shape: {data.shape}")
        labels.append(data[:, 0].astype(int))
        locations.append(data[:, 1:])
    
    # Compute the sum of absolute differences between locations of the first two files
    diff = np.sum(np.abs(locations[0] - locations[1]))
    if diff < 0.05:
        print(diff)
        return labels
    else:
        # Use logging, exceptions, or other mechanisms for error handling
        print("Difference is greater than 0.05. Consider manual debugging.")
        return None

dataset = load_dataset_from_dir(r"C:\Users\parul\OneDrive - Georgia Institute of Technology\Documents\mcgrath_research\data_week_1\week1_data\master_dataset", "master_dataset")

# initialize a DataFrame to store the results
out_count=0
a_df = pd.DataFrame(columns=['trialid', 'imageid', 'detectionid', annotator1, annotator2])

# introducing a new Path package to simplify reading a path into the script
from pathlib import Path
# iterate over the samples in the dataset to check if both annotation files exist for the current sample
# that is being iterated over
for sample in dataset:
    # Define data with a default value
    # data = np.empty((0, 0))
    # for sample in dataset:
    #     if os.path.exists(root_1+labels_start+sample.image_uid+label_end):
    #         if os.path.exists(root_2+labels_start+sample.image_uid+label_end):
    #             print(1)
    #             path1=root_1+labels_start+sample.image_uid+label_end
    #             path2=root_2+labels_start+sample.image_uid+label_end
    #             paths=[path1,path2]
    #             # if this is the case, associate annotatons from both files together
    #             data=associate_files(paths)
    #         else:
    #             print('something is wrong here 1')
    #             print(sample)
    #     elif os.path.exists(root_1+labels_start+sample.image_uid+label_end):
    #         if os.path.exists(root_2+labels_start+sample.image_uid+label_end):
    #             print(2)
    #             path1=root_1+labels_start+sample.image_uid+label_end
    #             path2=root_2+labels_start+sample.image_uid+label_end
    #             paths=[path1,path2]
    #             data=associate_files(paths)
    #         else:
    #             print('something is wrong here 2')
    #             print(sample)
    # optimizing the above code below through importing Path package from pathlib:

    # def pathsdef(path1, path2):
        

    # Constructing file paths using pathlib for clarity and robustness
    # This approach leverages pathlib's object-oriented path construction
    # which is more readable and less prone to errors related to path separator inconsistencies across different operating systems. 
    path1 = Path(root_1) / f"{labels_start}{sample.image_uid}{label_end}"
    path2 = Path(root_2) / f"{labels_start}{sample.image_uid}{label_end}"

    if path1.exists():
        if path2.exists():
            print(1)
            path1 = Path(root_1) / f"{labels_start}{sample.image_uid}{label_end}"
            path2 = Path(root_2) / f"{labels_start}{sample.image_uid}{label_end}"
            paths = [path1,path2]
            print(*paths)
            data = associate_files(paths)
        else:
            print('something is wrong here 1')
            print(sample)
    elif path1.exists():
        if path2.exists():
            print(2)
            path1= Path(root_1) / f"{labels_start}{sample.image_uid}{label_end}"
            path2= Path(root_2) / f"{labels_start}{sample.image_uid}{label_end}"
            paths=[path1,path2]
            print(*paths)
            data = associate_files(paths)
        else:
            print('something is wrong here 2')
            print(sample)
    
    else:
        # if nothing else works, increment the count of the samples with that of the missing annotation files
        out_count+=1
    #debugged the following by setting data to None and adding this condition so that this block below isn't accessed unconditionally:
    if data is not None and len(data) > 0:
        # Extract label information and then append it to the DataFrame
        detection_num=len(data[0])
        # extract labels for annotator1 and annotator2
        label1=data[0]
        label2=data[1]
        # iterate over each detection in the sample
        for i in range(detection_num):
            # create a new row for the DataFrame with information about the current detection
            new_row = {'trialid': sample.projectID, 'imageid': sample.image_uid, 'detectionid': i, annotator1: label1[i], annotator2: label2[i]}
            
            # append the new row to the DataFrame, ignoring the index to ensure continuous indexing
            a_df = pd.concat([a_df, pd.DataFrame([new_row])], ignore_index=True)

        # convert the columns into integer types
        a_df['Bree'] = a_df['Bree'].astype(int)
        a_df['Patrick'] = a_df['Patrick'].astype(int)

        # now calculate the absolute difference between the annotations
        a_df['difference']=abs(a_df.Bree-a_df.Patrick)

        # group by trial id and calculate accuracy
        df1 = a_df.groupby('trialid')['difference'].sum()
        df2 = a_df.groupby('trialid')['trialid'].count()
        acc=[1]*len(df1.values)-(df1.values/df2.values)
        df=pd.DataFrame(columns=['trial', 'acc'])
        df['trial']=list(df1.index)
        df['acc']=acc

        # select subset of data where the difference is 1 and group by trial id and Bree's annotation
        sub_df=a_df[a_df.difference==1]
        sub_df.groupby(['trialid', 'Bree'])[['Bree','Tucker']].count()
