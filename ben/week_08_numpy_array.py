#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np

path = "/Users/bfc782/spiced_projects/a-star-anise-student-code/week08_markov/"
os.chdir(path)

#%%
### Read in csv file
mon = pd.read_csv('monday.csv',sep=";")
### Set timestamp to be datetime
ts = pd.to_datetime(mon['timestamp'])
### overwrite timestamp with newly formatted column ts
mon['timestamp']=ts

#%%
### Inspection shows that there are missing timesteps in the data 
    ### (i.e times when nothing changes)
### Create full list of timestamps between opening and closing time
opening = "2019-09-02 07:00:00" # I'm sure they open at 0700!
closing = max(mon['timestamp'])
clean_ts_full = pd.date_range(opening,closing,freq="t")

#%%
## Create 3D numpy array using relevant data limit values
LOCS = ["checkout","dairy","drinks","fruit","spices"]
locs = pd.Index(LOCS)
# locs.get_loc("drinks") = 2
dim_t = len(clean_ts_full)
dim_c = mon['customer_no'].max()+1 #customer_no starts at 1, not the usual zero index
dim_l = len(LOCS) 
dims = (dim_t,dim_c,dim_l)
time_cust_loc = np.zeros(dims) # declare the empty array with zeros

#%%
### 1: iterate through data file, 
### 2: transform the data to coordinates x= time_minute, y=customer_no, z=location mapping
    ### Index.get_loc(df) is useful method. Returns the index integer for the index item.
### 3: insert 1's into the array where the customers are reported in the data file.

for i in range(len(mon)): # step 1
    x = clean_ts_full.get_loc(mon['timestamp'][i]) # step 2
    y = mon['customer_no'][i] # step 2
    z = locs.get_loc(mon['location'][i]) # step 2   
    time_cust_loc[x,y,z]=1 # step 3
    
#%%
### Populate the static customers according to the rules:
    ### 1: rule applies to time steps > 0 (i.e. not for the first item of day's data)
    ### 2: customer exists in previous time slice 
    ###    AND 3: was not in the checkout (i.e. location 0 was not ==1)
    ### 4: if customer does not exist in the current time slice, 
    ###     then: copy prior time slice

for i in range(dim_t):
    for j in range(dim_c):
        if i>0: # rule 1
            if time_cust_loc[i-1,j,:].sum()==1 and time_cust_loc[i-1,j,0]!=1: # rule 2,3
                if time_cust_loc[i,j,:].sum()==0: # rule 4
                    time_cust_loc[i,j,:]=time_cust_loc[i-1,j,:] # then copy prior time slice

#%%%
### now some functions:
    
def customer_duration():
    """ returns the length of time a user-queried customer spent in the shop"""
    
    y = int(input("which customer do you want to query?"))
    return int(time_cust_loc[:,y,:].sum())

#%%

def busiest_aisle():
    """ returns the busiest aisle of the day, where and when"""
    
    cust_load_max = 0
    time = ""
    location = ""
    for x in range(dim_t):
        for z in range(dim_l):
            if time_cust_loc[x,:,z].sum()>cust_load_max:
                cust_load_max = time_cust_loc[x,:,z].sum()
                time = mon['timestamp'][x]
                location = LOCS[z]                
    return (time, location, cust_load_max)



    
    
        
    
