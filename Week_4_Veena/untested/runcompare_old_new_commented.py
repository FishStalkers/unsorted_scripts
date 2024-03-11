# this script seemingly performs an analysis on video tracking data
# it calculates various statistics, and visualizes the results using matplotlib
# it also saves the final results into a CSV file

# make imports
import argparse, subprocess, pdb, datetime, os, sys
import pandas as pd

# add a path to the system path
sys.path.append('/data/home/bshi42/CichlidBowerTracking/') 

# import a custom module that fcomes from cichlid_bower_tracking
from cichlid_bower_tracking.helper_modules.file_manager import FileManager as FM


# Define a function that gets projects from the FileManager object created in the previous line 
def get_projects(fm_obj):
    #fm_obj.downloadData(fm_obj.localSummaryFile)
    # read the local summary file into a DataFrame
    dt = pd.read_csv(fm_obj.localSummaryFile, index_col = False, dtype = {'StartingFiles':str, 'RunAnalysis':str, 'Prep':str, 'Depth':str, 'Cluster':str, 'ClusterClassification':str,'TrackFish':str, 'AssociateClustersWithTracks':str, 'LabeledVideos':str,'LabeledFrames': str, 'Summary': str})

    # Identify projects to run on:
    # get a list of projectIDs
    projectIDs = list(dt.projectID)
    return projectIDs

# Identify projects to run analysis on
fm_obj = FM(analysisID = 'Single_nuc_1')
#fm_obj.downloadData(fm_obj.localSummaryFile)
#fm_obj.downloadData(fm_obj.localEuthData)

summary_file = fm_obj.localSummaryFile # Shorthand to make it easier to read
#Obtain projectIDs from the FileManager object
projectIDs = get_projects(fm_obj)

# print all the projectIDs
print('This script will analyze the folllowing projectIDs: ' + ','.join(projectIDs))

# To run analysis efficiently, we download and upload data in the background while the main script runs
uploadProcesses = [] # Keep track of all of the processes still uploading so we don't quit before they finish

dt = pd.read_csv(fm_obj.localSummaryFile, index_col = False, dtype = {'StartingFiles':str, 'RunAnalysis':str, 'Prep':str, 'Depth':str, 'Cluster':str, 'ClusterClassification':str, 'TrackFish':str, 'AssociateClustersWithTracks': str, 'LabeledVideos':str,'LabeledFrames': str, 'Summary': str})
de = pd.read_csv(fm_obj.localEuthData, index_col = False)
trialidx={}
for pid in dt.projectID:
    temp_de=de[de.pid==pid]
    pid_et=datetime.datetime.strptime(str(temp_de.dissection_time.values[0]), "%m/%d/%Y %H:%M")
    fm_obj=FM(projectID = pid, analysisID = "Single_nuc_1")
    videos = fm_obj.lp.movies
    count=0
    for videoIndex in videos:
        delta=videoIndex.endTime-pid_et
        days=delta.total_seconds() / (60*60*24)
        if days<1:
            if days>0:
                trialidx[pid]=count
        count+=1

paths=['/home/bshi/Dropbox (GaTech)/BioSci-McGrath/PublicIndividualData/Breanna/__ProjectData/Single_nuc_1/', '/MasterAnalysisFiles/', 'AllDetectionsFish.csv', 'AllTrackedFish.csv']

# initialize lists and DataFrame
x1=[]
x2=[]
y=[]
count=0
columns=['i' , 'val1', 'val2', 'oldmeantrack', 'newmeantrack', 'nmale_detection', 'nhigh_male_track', 'percent_nmale_detection', 'percent_nhigh_male_track', 'omale_detection', 'ohigh_male_track', 'percent_omale_detection', 'percent_ohigh_male_track', 'nfemale_detection', 'nhigh_female_track', 'percent_nfemale_detection', 'percent_nhigh_female_track', 'ofemale_detection', 'ohigh_female_track', 'percent_ofemale_detection', 'percent_ohigh_female_track','nuk_track','percent_nuk_track', 'ouk_track','percent_ouk_track']
df = pd.DataFrame(columns=columns)

# Loop through projectIds
for i in projectIDs: 
    # initialize FileManager object from the project
    fm=fm_obj = FM(analysisID = 'Single_nuc_1', projectID=i)
    
    # get a video object
    videobj=fm.returnVideoObject(trialidx[i])
    base=videobj.baseName
    sid=i.split('singlenuc')[1].split('_Tk')[0]
    y.append(sid)

    # extract all the relevant data needed
    nt = pd.read_csv(fm.localAllFishTracksFile)
    #fm.downloadData(fm.localAllFishTracksFile)
    nt = nt[nt.base_name==base]
    #fm.downloadData(fm.localAllFishDetectionsFile)
    nd = pd.read_csv(fm.localAllFishDetectionsFile)
    nd = nd[nd.base_name==base]
    fm.downloadData(fm.localAllFishSexFile)
    ns=pd.read_csv(fm.localAllFishSexFile)
    
    # in the following lines, obtain relevant statistics needed
    print(ns.base_name.unique()==base)
    means1 = ns.groupby('track_id')['sex_class'].mean().rename('average_sex_class')
    merged1 = ns.merge(means1, on='track_id')
    ot=pd.read_csv(paths[0]+i+paths[1]+paths[3])
    ot = ot[ot.base_name==base]
    means = ot.groupby('track_id')['track_id'].count().rename('track_length')
    merged = ot.merge(means, on='track_id')
    means2 = ns.groupby('track_id')['class_id'].mean().rename('average_sex_class')
    merged2 = ns.merge(means1, on='track_id')
    merged2['sex_class']=merged2['class_id'].copy()
    oldmean= merged['track_length'].mean()
    od=pd.read_csv(paths[0]+i+paths[1]+paths[2])
    od = od[od.base_name==base]
    #list of things
    # calcualte differences:
    val1=nt.shape[0]-ot.shape[0]
    val2=nd.shape[0]-od.shape[0]
    
    oldmeantrack= merged['track_length'].mean()
    newmeantrack=nt['track_length'].mean()
    
    nmale_detection=merged1[merged1.sex_class<0.4]['track_id'].count()
    nhigh_male_track=len(merged1[merged1.average_sex_class<0.4]['track_id'].unique())
    percent_nmale_detection=nmale_detection/int(merged1.shape[0])
    percent_nhigh_male_track=nhigh_male_track/len(merged1.track_id.unique())
    
    
    nuk_track=len(merged1[(merged1.average_sex_class>=0.4) & (merged1.average_sex_class<=0.6)]['track_id'].unique())
    percent_nuk_track=nuk_track/len(merged1.track_id.unique())
    
    nfemale_detection=merged1[merged1.sex_class>0.6]['track_id'].count()
    nhigh_female_track=len(merged1[merged1.average_sex_class>0.6]['track_id'].unique())
    percent_nfemale_detection=nfemale_detection/int(merged1.shape[0])
    percent_nhigh_female_track=nhigh_female_track/len(merged1.track_id.unique())
    
    
    omale_detection=merged2[merged2.sex_class>0.6]['track_id'].count()
    ohigh_male_track=len(merged2[merged2.average_sex_class>0.6]['track_id'].unique())
    percent_omale_detection=omale_detection/int(merged2.shape[0])
    percent_ohigh_male_track=ohigh_male_track/len(merged2.track_id.unique())
    
    
    ouk_track=len(merged2[(merged2.average_sex_class>=0.4) & (merged2.average_sex_class<=0.6)]['track_id'].unique())
    percent_ouk_track=ouk_track/len(merged2.track_id.unique())
    
    ofemale_detection=merged2[merged2.sex_class<0.4]['track_id'].count()
    ohigh_female_track=len(merged2[merged2.average_sex_class<0.4]['track_id'].unique())
    percent_ofemale_detection=ofemale_detection/int(merged2.shape[0])
    percent_ohigh_female_track=ohigh_female_track/len(merged2.track_id.unique())
    
    # store all of the results in the stuff_list
    stuff_list=[i , val1, val2, oldmeantrack, newmeantrack, nmale_detection, nhigh_male_track, percent_nmale_detection, percent_nhigh_male_track, omale_detection, ohigh_male_track, percent_omale_detection, percent_ohigh_male_track, nfemale_detection, nhigh_female_track, percent_nfemale_detection, percent_nhigh_female_track, ofemale_detection, ohigh_female_track, percent_ofemale_detection, percent_ohigh_female_track,nuk_track,percent_nuk_track, ouk_track,percent_ouk_track]
    
    #concatenate the result with DataFrame
    df = pd.concat([df, pd.DataFrame([stuff_list], columns=df.columns)])
    
    # append to lists
    x1.append(val1)
    x2.append(val2)
    count+=1

    # print the final status
    if count.__mod__(10)==0:
        print(str(count)+' of '+str(len(projectIDs)) )

# calculate additional differences
df['difmdetections']=df['nmale_detection']-df['omale_detection']
df['difhmtrack']=df['nhigh_male_track']-df['ohigh_male_track']
df['difhftrack']=df['nhigh_female_track']-df['ohigh_female_track']
df['difuktrack']=df['nuk_track']-df['ouk_track']
df['y']=y

# save DataFrame to CSV file
df.to_csv('/home/bshi/Desktop/trial_summaries.csv')

# Import plotting libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# plot a bar chart
plt.figure(figsize=(30, 10))
fig, ax = plt.subplots(figsize=(20,5))
ax.bar(y, df['nmale_detection']-df['omale_detection'], width=0.4)
#ax.set_xlim(-0.8, 2.8)
#plt.figure(figsize=(20, 5)) 
#ax.set_aspect(0.2)

# set axis labels and title
formatter = ticker.ScalarFormatter(useMathText=True) 
formatter.set_scientific(False) 
formatter.set_powerlimits((-1,1))
ax = plt.gca()  
ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel('male detections')
ax.set_xlabel('Trials')
ax.set_title('Difference in total male  on euth video')

#display output plot
plt.show()


# Save the figure
fig.savefig('./fruit_quantities.png')

# plot another bar chart
plt.bar(x2, y)
plt.xlabel("ProjectID")
plt.ylabel("Difference of Detections")
plt.title("NEW yolo - OLD yolo number of Detections")

plt.show()