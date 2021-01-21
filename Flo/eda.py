#%%

from typing import DefaultDict
from numpy.core.fromnumeric import sort
import pandas as pd
import numpy as np
from pandas.core.tools.datetimes import to_datetime
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(11.7,8.27)})

#%%

monday = pd.read_csv('data/monday.csv', sep=';', date_parser=True)
tuesday = pd.read_csv('data/tuesday.csv', sep=';')
wednesday = pd.read_csv('data/wednesday.csv', sep=';')
thursday = pd.read_csv('data/thursday.csv', sep=';')
friday = pd.read_csv('data/friday.csv', sep=';')

#%%
monday['timestamp'] = to_datetime(monday['timestamp'],format='%Y-%m-%d %H:%M:%S')
#%%
# Creating checkout for last consumers 
monday['checkout'] = monday.duplicated(subset = 'customer_no', keep = 'last')
monday.loc[monday['checkout'] == False, 'location'] = 'checkout'
monday.drop('checkout', axis=1, inplace=True)

#%%
#Show the distribution of locations per user
count_location = monday.groupby('customer_no')[['location']].count()
count_location.hist()

#%%%
# 
#? Q1. Calculate the total number of customers in each section

q1 = monday.groupby('location')[['location']].count()
q1.plot(kind='bar')

#%%
#? Q2 : Calculate the total number of customers in each section over time

monday['hour'] = monday['timestamp'].dt.hour
no_checkout = monday[monday['location'] != 'checkout']
q2 = no_checkout.groupby(['hour','location'])[['timestamp']].count()
sns.lineplot(x='hour',y='timestamp', data=q2, hue='location')

#%%

#? Q3: Display the number of customers at checkout over time

checkout = monday[monday['location'] == 'checkout']
q3 = checkout.groupby(['hour','location'])[['timestamp']].count()
sns.lineplot(x='hour',y='timestamp', data=q3, hue='location')
#%%
monday['last_loc']= monday[monday['timestamp'] == monday.groupby(['customer_no'])['timestamp'].transform(max)]
#%%
last_location = monday[monday['timestamp'] == monday.groupby(['customer_no'])['timestamp'].transform(max)]


location_bug = last_location[last_location['location']!='checkout']
location_bug.drop('location', axis=1)
location_bug['location'] = 'checkout'
location_bug

#%%
monday.groupby(['customer_no'])['timestamp'].transform(range(10))


#%%

#%%
monday_up = monday.merge(location_bug, on['timestamp','customer_no'])
#%%
location_bug
#%%
df7 = monday.groupby(['customer_no'])['timestamp'].max()

df7
#%%
monday

#Testing Testing Yes I saw! Try to run something
#%%
#? Q4. Calculate the time each customer spent in the market
time_spent = monday.groupby('customer_no')[['timestamp']].agg(np.ptp)

time = pd.to_timedelta(time_spent.timestamp).dt.total_seconds() / 60
#(time_spent.timestamp - pd.to_datetime('1970-01-01')).dt.total_seconds()

time.hist()
