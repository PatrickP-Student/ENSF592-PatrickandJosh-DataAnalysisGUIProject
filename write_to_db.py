import pymongo
from pymongo import MongoClient
import pandas as pd

'''
Traffic Incidents
'''

cluster = pymongo.MongoClient("mongodb+srv://User_1:1234@cluster-project.mmhhg.mongodb.net/ENSF592-DataCity?retryWrites=true&w=majority")
db = cluster["ENSF592-DataCity"]

#TODO CREATE A COLLECTION FOR EACH CSV FILE ON MONGODB

collection1 = db["CityofCalgary - Traffic Incidents"]
df1 = pd.read_csv("Traffic_Incidents_Archive_2016.csv") 
records1 = df1.to_dict(orient = 'dict')

collection2 = db["CityofCalgary - Traffic Incidents 2"]
df2 = pd.read_csv("Traffic_Incidents_Archive_2017.csv")
records2 = df2.to_dict(orient = 'dict')

collection3 = db["CityofCalgary - Traffic Incidents 3"]
df3 = pd.read_csv("Traffic_Incidents.csv")
records3 = df3.to_dict(orient = 'dict')

# result = collection.insert_many(records ) ## THIS WILL UPLOAD THE OBJECT TO THE DB

#####################################################################################################
'''
Traffic Volumes
'''

#TODO CREATE A COLLECTION FOR EACH CSV FILE ON MONGODB

collection1 = db["CityofCalgary - Traffic Volumes"]
df1 = pd.read_csv("TrafficFlow2016_OpenData.csv") 
records = df1.to_dict(orient = 'dict')

collection2 = db["CityofCalgary - Traffic Volumes 2"]
df2 = pd.read_csv("2017_Traffic_Volume_Flow.csv") 
records = df2.to_dict(orient = 'dict')

collection3 = db["CityofCalgary - Traffic Volumes 3"]
df3 = pd.read_csv("Traffic_Volumes_for_2018.csv") 
records = df3.to_dict(orient = 'dict')


# result = collection.insert_many(records ) ## THIS WILL UPLOAD THE OBJECT TO THE DB
