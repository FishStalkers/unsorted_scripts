# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import all the necessary libraries
import fiftyone as fo
import os
import pdb
import pandas as pd
import numpy as np

# defining root directorie sfor datasets as well as other constants
root_1='/home/bshi/Documents/Patrick_CVAT_dataset/'
root_2='/home/bshi/Documents/Bree_CVAT_dataset/'

labels_start='obj_train_data/obj_train_data/'
label_end='.txt'
annotator1='Patrick'
annotator2='Bree'
annotator3='Tucker'

# import the glob module
# the glob module is short for global, and is a function that is used to search for files
# that match a specific file pattern or name, especially for csv or txt files
import glob
import os
# find all text files in either Patrick_CVAT_dataset or Bree_CVAT_dataset directories
text1 = glob.glob(root_1+labels_start+'*.txt')
text2= glob.glob(root_2+labels_start+'*.txt')

# define function that associates labels from two files together
def associate_files(paths):
    print(paths)
    array=[]
    label=[]
    location=[]
    for i in paths:
        file = open(i, 'r')
        data1=[]
        data2=[]
        for line in file:
            # parse the data from the file into integers and floats
            data=[float(x) for x in line.strip().split(' ')]
            data1.append(int(data[0]))
            data2.append(data[1:])
        label.append(data1)
        location.append(data2)
        file.close()
    # here, check if the difference between each of the locations is less than 0.05
    if np.sum(np.abs(np.array(location[0])-np.array(location[1]))) < 0.05:
        print(np.sum(np.abs(np.array(location[0])-np.array(location[1]))))
        return label
    else:
        # if the difference is greater, enter into debugging mode
        pdb.set_trace()

dataset = fo.load_dataset("master_dataset")

# initialize a DataFrame to store the results
out_count=0
a_df = pd.DataFrame(columns=['trialid', 'imageid', 'detectionid', annotator1, annotator2])

# iterate over the samples in the dataset to check if both annotation files exist for the current sample
# that is being iterated over
for sample in dataset:
    if os.path.exists(root_1+labels_start+sample.image_uid+label_end):
        if os.path.exists(root_2+labels_start+sample.image_uid+label_end):
            print(1)
            path1=root_1+labels_start+sample.image_uid+label_end
            path2=root_2+labels_start+sample.image_uid+label_end
            paths=[path1,path2]
            # if this is the case, associate annotatons from both files together
            data=associate_files(paths)
        else:
            print('something is wrong here 1')
            print(sample)
    elif os.path.exists(root_1+labels_start+sample.image_uid+label_end):
        if os.path.exists(root_2+labels_start+sample.image_uid+label_end):
            print(2)
            path1=root_1+labels_start+sample.image_uid+label_end
            path2=root_2+labels_start+sample.image_uid+label_end
            paths=[path1,path2]
            data=associate_files(paths)
        else:
            print('something is wrong here 2')
            print(sample)
    
    else:
        # if nothing else works, increment the count of the samples with that of the missing annotation files
        out_count+=1
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
