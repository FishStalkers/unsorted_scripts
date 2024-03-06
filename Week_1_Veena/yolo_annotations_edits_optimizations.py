import fiftyone as fo
import pandas as pd
from fiftyone import ViewField as F
import pandas as pd
import fiftyone.zoo as foz
import fiftyone.utils.random as four
#add description of what kinds of data this scripts works with 
# function to load dataset
def load_dataset(dataset_dir, dataset_name):
    return fo.Dataset.from_dir(
        dataset_dir=dataset_dir,
        dataset_type=fo.types.FiftyOneDataset,
        name=dataset_name,
    )
#note
#this is too short to require a function

# function to create filtered dataset
def process_dataset(dataset):
    img_paths = []
    img_ids = []
    for sample in dataset: 
        if sample.filepath in img_paths:
            print('Skipped duplicate:', sample.filepath)
        else:
            img_paths.append(sample.filepath)
            img_ids.append(sample.id)
    
    filtered_dataset = fo.Dataset()
    for sample in dataset:
        if sample.id in img_ids:
            filtered_dataset.add_sample(sample)

    filtered_dataset.save()

    return filtered_dataset

def main():
    dataset_dir = r"C:\Users\veena\Downloads\week1_data\week1_data"
    dataset = load_dataset(dataset_dir + "\my-detection-dataset", "my_detection_dataset")
    master_dataset = load_dataset(dataset_dir + "\master_dataset", "master_dataset")

    filtered_dataset = process_dataset(dataset)

    for s1 in filtered_dataset:
        s1.set_field('imageID', s1.filepath.split('/')[-1].split('.')[0])
        s1.save()
    filtered_dataset.save()

    for s2 in dataset:
        s2.set_field('imageID', s2.filepath.split('/')[-1].split('-')[0])
        s2.save()
    dataset.save()

    ds=filtered_dataset.match(F('filepath').ends_with('MC_singlenuc43_11_Tk41_060220_0001_vid_121862.jpg'))
    filtered_dataset.match(F('imageID').ends_with('MC_singlenuc43_11_Tk41_060220_0001_vid_121862'))
    master1_dataset = fo.Dataset()

    old_df = pd.read_csv(r'C:\Users\veena\Downloads\week1_data\week1_data\Fish_Reflection_Annotations_old.csv')

    dataset = load_dataset(dataset_dir + "\my-detection-dataset", "my_detection_dataset2")

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
    
    dataset = load_dataset(dataset_dir + "\mc_singlenuc_fo", "mc_singlenuc_fo")

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

if __name__ == "__main__":
    main()
