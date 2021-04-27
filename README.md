# CSE573-Project

Download the dataset(DS-1) using this link:</br >
https://drive.google.com/file/d/14lKOu5i-d3SrDuhe7iRzS0RSEpRTMHjh/view?usp=sharing</br >
</br >

</br>
The data folder contains actual bots in 2016 and 2018 datasets of DS-1 and Preprocessed Dataset 2.

</br >
The code folder contains the following:
</br>
DS_2016_tier_approach.ipynb  - Contains code related to calculating the bots based on tier 1 and tier 2 approach along with evaluation metrics code.This file requires input intermediate results from after calculating Threshold 1 and this file yields output total bots predicted from tier 1 approach , total bots predicted from tier 2 approach , total bots correctly predicted.
</br >
<br>
Ds_2_preprocess.ipynb - This file takes raw DS-2 datafile and converts it to coornet datafile format.
</br >
</br>
coor_net.py - This file contains code related to calculating Threshold-1(coordination interval) and code to construct highly coordinated graph.
</br >
<br>
dataset2_second_threshold_calculation.py - This file contains code related to calculating the second threshold in DS-2 and also code for most boosted accounts and most boosted domains.
</br >

