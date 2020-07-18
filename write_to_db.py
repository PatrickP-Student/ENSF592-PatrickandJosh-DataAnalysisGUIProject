'''
Filename: write_to_db.py
Author: Patrick Pickard
Date: July 17, 2020 - Friday
Description: This script will read 6 .csv files from the local repository location into
panda objects for formatting, perform additional formatting on the data read (removing unneeded 
data from any data sets, ordering columns, etc), convert the data structure to a list[] type, and 
write the lists to the database specified
'''

import pymongo
from pymongo import MongoClient
import pandas as pd

####################################################################################################

'''
Traffic Incidents - 2016 to 2018
'''

# connects to the cluster hosted on MongoDB Atlas (cloud database created for this project)
cluster = pymongo.MongoClient("mongodb+srv://User_1:1234@cluster-project.mmhhg.mongodb.net/ENSF592-DataCity?retryWrites=true&w=majority")
#clairifies database that will be used for this application
db = cluster["ENSF592-DataCity"]

## this is for the 2016 data file
# sets the collection inside the database to the specifically chosen one
collection1 = db["CityofCalgary - Traffic Incidents"]
#reads the csv file and into a panda type object data structure
df1 = pd.read_csv("Traffic_Incidents_Archive_2016.csv")
# formats the order of the columns
df1 = df1[['INCIDENT INFO', 'DESCRIPTION', 'START_DT', 'MODIFIED_DT', 'QUADRANT', 'Longitude', 'Latitude', 'location', 'Count']] 
# converts the data structure to a dictionary
records1 = df1.to_dict(orient = 'list')

# writes the dictionaries holding the data into the database
collection1.insert_one(records1) ## THIS WILL UPLOAD THE DICTS TO THE DB

# this above code will be repeated (in general template format) for all files to be written to the
# database. Subsequent files code blocks are shown below.

## this is for the 2017 data file
collection2 = db["CityofCalgary - Traffic Incidents 2"]
df2 = pd.read_csv("Traffic_Incidents_Archive_2017.csv")
df2 = df2[['INCIDENT INFO', 'DESCRIPTION', 'START_DT', 'MODIFIED_DT', 'QUADRANT', 'Longitude', 'Latitude', 'location', 'Count']]
records2 = df2.to_dict(orient = 'list')

collection2.insert_one(records2)

## this is for the 2018 data file
collection3 = db["CityofCalgary - Traffic Incidents 3"]
df3 = pd.read_csv("Traffic_Incidents.csv")
df3 = df3[['INCIDENT INFO', 'DESCRIPTION', 'START_DT', 'MODIFIED_DT', 'QUADRANT', 'Longitude', 'Latitude', 'location', 'Count', 'id']]
# the below lines will remove all rows in the START_DT column that contain the 2020, 2019, 2017, 2016 
# string (ie, it will remove all non 2018 data) . **** I know this is likely a way to do this in one line
# of code, but I could not get it to work properly so I simply did the following in 4 individual
# contains() function calls instead to remove the rows needed. ****
df3 = df3[~df3.START_DT.str.contains("/2016 ")]
df3 = df3[~df3.START_DT.str.contains("/2017 ")]
df3 = df3[~df3.START_DT.str.contains("/2019 ")]
df3 = df3[~df3.START_DT.str.contains("/2020 ")]
records3 = df3.to_dict(orient = 'list')

###### THIS IS FOR TESTING TO SEE IF ALL NON 2018 ROWS HAVE BEEN REMOVED ######
# for column_header, data in records3.items():
#     print(column_header)
#     for key in data:
#         print(key)

collection3.insert_one(records3)

#####################################################################################################

'''
Traffic Volumes - 2016 to 2018
'''

## this is for the 2016 data file
collection1a = db["CityofCalgary - Traffic Volumes"]
df1a = pd.read_csv("TrafficFlow2016_OpenData.csv") 
df1a = df1a[['secname', 'the_geom', 'year_vol', 'shape_leng', 'volume']]   
records1a = df1a.to_dict(orient = 'list')

collection1a.insert_one(records1a) ## THIS WILL UPLOAD THE DICTS TO THE DB

## this is for the 2017 data file
collection2a = db["CityofCalgary - Traffic Volumes 2"]
df2a = pd.read_csv("2017_Traffic_Volume_Flow.csv") 
df2a = df2a[['segment_name', 'the_geom', 'year', 'length_m', 'volume']]   
records2a = df2a.to_dict(orient = 'list')

collection2a.insert_one(records2a)

## this is for the 2018 data file
collection3a = db["CityofCalgary - Traffic Volumes 3"]
df3a = pd.read_csv("Traffic_Volumes_for_2018.csv") 
df3a = df3a[['SECNAME', 'multilinestring', 'YEAR', 'Shape_Leng', 'VOLUME']] 
records3a = df3a.to_dict(orient = 'list')

collection3a.insert_one(records3a)
