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
#? Q4: Calculate the time each customer spent in the market

time_left = monday.groupby('customer_no')['timestamp'].max()#.apply(lambda x: x[x == 'checkout'])
time_entered = monday.groupby('customer_no')['timestamp'].min()
time_spent = time_left - time_entered
time_spent_minutes = time_spent / np.timedelta64(1, 'm')
time_spent_minutes.hist()

#%%
#? Q5: Calculate the total number of customers in the supermarket over time.
#*Complex way: I take the 1st entry and generate a new timestamp of 1 minute based on how long the person stays

#times = [(datetime.datetime(2017, 7, 17, 9, 10, 0) + datetime.timedelta(minutes=5*x)).time() for x in range(5)]

#%%
#? Q6: Plot location by visit step

def count_up(x):
    return list(range(len(x))) 

monday['step'] = monday.groupby('customer_no')['timestamp'].transform(count_up)
step_0 = monday[monday['step']==0]
q6 = step_0.groupby(['hour','location'])[['timestamp']].count()
sns.lineplot(x='hour',y='timestamp', data=q6, hue='location')
step_6 = monday[monday['step']<7]
step_6 = step_6[step_6['location'] != 'checkout']
q6_1 = step_6.groupby(['hour','location','step'])[['timestamp']].count()
q6_1 = q6_1.reset_index()
q6_1.set_index('hour',inplace=True)
#g = sns.FacetGrid(q6_1,col='step')
#g.map(sns.histplot, x='location')
#g.map(sns.barplot,x='hour',y='timestamp',hue='location', kind='line')
sns.relplot(data=q6_1,x='hour',y='timestamp',col='step',hue='location',kind='line')

#estimator=lambda x: len(x) / len(q6_1) * 100

#%%

#monday['last_loc']= monday[monday['timestamp'] == monday.groupby(['customer_no'])['timestamp'].transform(max)]
