#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:09:00 2023

@author: bshi
"""
import fiftyone as fo
import fiftyone.zoo as foz
import fiftyone.utils.random as four
# dataset_dir = r"C:\Users\veena\Downloads\week1_data\week1_data\my-detection-dataset\data"
# dataset_type = "image"
# dataset = fo.Dataset.from_dir(dataset_dir, dataset_type=dataset_type)
name = "my_detection_dataset"
dataset_dir = r"C:\Users\veena\Downloads\week1_data\week1_data\my-detection-dataset"

# Create the dataset
my_detection_dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.FiftyOneDataset,
    name=name,
)
# dataset = fo.load_dataset(r"C:\Users\veena\Downloads\week1_data\week1_data\my-detection-dataset")
dataset = fo.load_dataset("my_detection_dataset")
# print(dataset)
img=[]
img_id=[]
for sample in dataset: 
    if sample.filepath in img:
        #dataset.delete_sample(sample.id)
        print('skipped')
    # else:
        img.append(sample.filepath)
        img_id.append(sample.id)

# Create a new dataset with unique samples
filtered_dataset = fo.Dataset()

# Iterate over the original dataset and add samples with unique IDs to the new dataset
for sample in dataset:
    if sample.id in img_id:
        filtered_dataset.add_sample(sample)

# Save the new dataset
filtered_dataset.save()

# below line commented - already imported
# import fiftyone as fo

name = "master_dataset"
dataset_dir = r"C:\Users\veena\Downloads\week1_data\week1_data\master_dataset"

# Create the dataset
master_dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.FiftyOneDataset,
    name=name,
)
# commenting out below line - do not see where this dataset is used
# dataset = fo.load_dataset("mc_singlenuc_fo")
# View summary info about the dataset
# print(dataset)

# Print the first few samples in the dataset
# print(dataset.head())

for s1 in filtered_dataset:
    s1.set_field('imageID', s1.filepath.split('/')[-1].split('.')[0])
    s1.save()
filtered_dataset.save()

for s2 in dataset:
    s2.set_field('imageID', s2.filepath.split('/')[-1].split('-')[0])
    s2.save()
dataset.save()

from fiftyone import ViewField as F
import pandas as pd
# field = "imageID" line not used
#one_expr = F(field).contains(['MC_singlenuc43_11_Tk41_060220_0001_vid_121862'])
#both_expr = F(field).contains(["cat", "dog"], all=True)
#ds
# (one_expr & ~both_expr)
#filtered_dataset.match(one_expr)
ds=filtered_dataset.match(F('filepath').ends_with('MC_singlenuc43_11_Tk41_060220_0001_vid_121862.jpg'))

filtered_dataset.match(F('imageID').ends_with('MC_singlenuc43_11_Tk41_060220_0001_vid_121862'))
master1_dataset = fo.Dataset()

old_df = pd.read_csv(r'C:\Users\veena\Downloads\week1_data\week1_data\Fish_Reflection_Annotations_old.csv')

name = "my_detection_dataset2"
dataset_dir = r"C:\Users\veena\Downloads\week1_data\week1_data\my-detection-dataset"

my_detection_dataset2 = fo.Dataset.from_dir(
   dataset_dir=dataset_dir,
   dataset_type=fo.types.FiftyOneDataset,
   name=name,
)
dataset = fo.load_dataset("my_detection_dataset2")
image_id=[]
empty=[]
for sample in filtered_dataset:
    print(sample)
    sub_ds=dataset.match(F('imageID').ends_with(sample.imageID))
    if len(sub_ds)==0:
        empty.append(sample.imageID)
    for sub in sub_ds:
        
        master_sample=fo.Sample(filepath=sample.filepath)
        master_sample.set_field('width', 1296 )
        master_sample.set_field('height', 972 )
        master_sample.set_field('species', sub.species )
        master_sample.set_field('tank', sub.tank )
        master_sample.set_field('projectID',sub.project )
        master_sample.set_field('video', sub.video )
        master_sample.set_field('project_date', sub.project_date)
        master_sample.set_field('frame', sub.frame)
        master_sample.set_field('image_uid', sub.imageID)
        master_sample.set_field('annotator', str(old_df[old_df.imageID==sub.imageID].annotator.unique()[0]))
        
        master_sample.set_field('type_FR', str(old_df[old_df.imageID==sub.imageID].image_type.unique()[0]))
        if sub.predictions!=None:
            master_sample.set_field('type_MF', 'val')
            master_sample.set_field('gt_FR', sample.ground_truth)
            master_sample.set_field('gt_MF', sub.ground_truth)
            master_sample.set_field('predict_MF', sub.predictions)
        else:
            master_sample.set_field('type_MF', 'train')
            master_sample.set_field('gt_FR', sample.ground_truth)
            master_sample.set_field('gt_MF', sub.ground_truth)
        
        
        master1_dataset.add_sample(master_sample)
        master_sample.save()
        image_id.append(sub.imageID)
master1_dataset.save()
export_dir = "./mc_singlenuc_fo/"

# The dataset or view to export

# Export the dataset
dataset.export(
    export_dir=export_dir,
    dataset_type=fo.types.FiftyOneDataset,
)
image_id=[]
#master_dataset = fo.Dataset()
#dataset1 = fo.load_dataset("my-detection-dataset")
for sample in filtered_dataset:
    image_id.append(sample.imageID)

# below line is commented out on Bree's code but I think it is needed
#dataset = fo.load_dataset("mc_singlenuc_fo")
name = "mc_singlenuc_fo"
dataset_dir = r"C:\Users\veena\Downloads\week1_data\week1_data\mc_singlenuc_fo"

mc_singlenuc_fo = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.FiftyOneDataset,
    name=name,
)

dataset = fo.load_dataset("mc_singlenuc_fo")
missing_dataset = fo.Dataset()
for sub in dataset:
    if sub.imageID not in image_id:
        missing_dataset.add_sample(sub)
  #      print(sub)

master_dataset.save()
    
master1_dataset = fo.Dataset()
count1=0
count2=0
for i in master_dataset:
    if i.predict_MF==None:
        count1+=1
    else:
        count2+=1
    
count=0
for sub in missing_dataset:
    master_sample=fo.Sample(filepath=sub.filepath)
    master_sample.set_field('width', 1296 )
    master_sample.set_field('height', 972 )
    try:
        species = sub.species
    except AttributeError:
        species = None
    master_sample.set_field('species', sub.species)
    master_sample.set_field('tank', sub.tank )
    master_sample.set_field('projectID',sub.project )
    master_sample.set_field('video', sub.video )
    master_sample.set_field('project_date', sub.project_date)
    master_sample.set_field('frame', sub.frame)
    master_sample.set_field('image_uid', sub.imageID)
    master_sample.set_field('annotator', None)
    master_sample.set_field('type_MF', 'train')
    master_sample.set_field('type_FR', 'val')
    master_sample.set_field('gt_FR', None)
    master_sample.set_field('gt_MF', None)
    master_sample.set_field('predict_MF', None)
    master_dataset.add_sample(master_sample)
    master_sample.save()
master_dataset.save()

export_dir = "./master_fiftyone_detection_dataset/"

# The dataset or view to export

# Export the dataset
master_dataset.export(
    export_dir=export_dir,
    dataset_type=fo.types.FiftyOneDataset,
)
