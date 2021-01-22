import pandas as pd
import numpy as np
import glob
import os
import datetime

def import_data(data_folder_path,seperator,col_index=None):
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df = pd.concat((pd.read_csv(f,sep=seperator,parse_dates=True, index_col=col_index ) for f in all_files))
    return df

path ="/mnt/c/Users/Mustafa/Desktop/Data_Sceince/Spiced/spiced_projects/data/doodl_supermarket/"

df = import_data(path,";")

df['timestamp'] = pd.to_datetime(df['timestamp'])

df.sort_values(by=['timestamp'], inplace=True)

df['on_day'] = df.timestamp.dt.day_name().str[:2]

df["cus_day_index"] = df.apply(lambda row: str(row.customer_no) + str(row.on_day),axis=1)

df.drop("on_day",axis=1, inplace=True)

df.set_index('cus_day_index',inplace=True,drop=True)

last_stat = df['timestamp'] == df.groupby(['customer_no'])['timestamp'].transform(max)

df.location[last_stat] = 'checkout' 

time_left = df.groupby('cus_day_index')['timestamp'].max()
time_entered = df.groupby('cus_day_index')['timestamp'].min()

first_stat = df['timestamp'] == df.groupby(['cus_day_index'])['timestamp'].transform(min)
#last_stat = df['timestamp'] == df.groupby(['cus_day_index'])['timestamp'].transform(max)

cus_first_stat= df[(first_stat==True)]['location'].values.tolist()

cus_first_stat_time = time_left.values.tolist()


def int_to_str_datetime(int_nums):
    dates_times = []
    for int_num in int_nums:
        date_time = str(datetime.datetime.utcfromtimestamp(int_num / 1e9 ))
        dates_times.append(date_time)
    return dates_times

dates_times = int_to_str_datetime(cus_first_stat_time)

cus_first_stat_time=list(zip(dates_times,cus_first_stat))

#print(cus_first_stat_time[0])

def create_prob_mat():
    df["next_state"] = df.groupby("customer_no")["location"].shift(-1)
    prob_mat = pd.crosstab(df["location"], df["next_state"], normalize = 0)
    prob_mat.loc["checkout"] = [1,0,0,0,0]
    return prob_mat

first_state_prop = df[df["customer_no"].duplicated() == False]["location"].value_counts(normalize = True)

