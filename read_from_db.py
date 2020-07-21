'''
Filename: read_from_db.py
Author: Patrick Pickard, Joshua Posyluzny
Date: July 17, 2020 - Friday
Description: This script will read 6 list objects (with nested lists in elements) from the database,
and perform all processing, sorting, and handling required for use in our program.
'''

import pymongo
from pymongo import MongoClient
import pandas as pd

class DBReader:

    # connects to the database when an instance of the DBReader class is created to minimize the number of times we need to
    # connect to the DB (versus connecting in each individual function)
    def __init__(self):
        # connects to the cluster hosted on MongoDB Atlas (cloud database created for this project)
        cluster = pymongo.MongoClient("mongodb+srv://User_1:1234@cluster-project.mmhhg.mongodb.net/ENSF592-DataCity?retryWrites=true&w=majority")
        # clarifies database that will be used for this application
        self.db = cluster["ENSF592-DataCity"]

    # This returns the raw csv data for the traffic volumes files (unsorted) from the db in 
    # the form of a dataframe pandas object
    def traffic_volumes(self,collection_name):
        # connects to collection holding the Traffic Volume document
        collection = self.db[collection_name]

        # this reads the document from the db
        traffic_vol_input_raw = collection.find_one({})

        # this converts the document to a pandas type object    
        df_traffic_vol_input_raw = pd.DataFrame(traffic_vol_input_raw)

        # this removes the obbject _id column MongoDB adds to the document, we will not need this data
        changed_raw = df_traffic_vol_input_raw.drop(columns=['_id'])

        return changed_raw

    # This returns the raw csv data for the traffic incidents files (unsorted) from the db in 
    # the form of a dataframe pandas object
    def traffic_incidents(self,collection_name):
        # connects to collection holding the Traffic Incident document
        collection = self.db[collection_name]

        # this reads the document from the db
        traffic_incident_input_raw = collection.find_one({})

        # this converts the document to a pandas type object    
        df_traffic_incident_input_raw = pd.DataFrame(traffic_incident_input_raw)

        # this removes the obbject _id column MongoDB adds to the document, we will not need this data
        changed_raw = df_traffic_incident_input_raw.drop(columns=['_id'])

        return changed_raw

    # This function sorts the data by descending order of the volume column (highest is top of column)
    def sort(self,data_struct,column):
        temp = data_struct.sort_values(column,ascending=False)
        return temp
    
    # This function will group the data rows by arguement passed to it and will return a 
    # dataframe pandas object with the new dataframe grouping
    def group_by_count(self,data_struct,column):
        wat = data_struct.drop_duplicates(subset="INCIDENT INFO")   # drops duplicate rows
        wat = wat.drop('Count', axis=1) #drops the Count column
        wat = wat.sort_values('INCIDENT INFO', ascending=True)  # sorts the values
        temp1 = data_struct.groupby(['INCIDENT INFO'])[["Count"]].sum() # sums the groups based on the same locations
        temp = pd.merge(wat,temp1,how='right', on='INCIDENT INFO')  # this groups the summed count column with the corresponding columns
        return temp
    
    # This function will return the number of incidents at the location with the maximum incidents
    def get_max_count(self,data_struct,column_head):
        temp = data_struct[column_head].max()
        return temp
    
    # This function will return the coordinates for the location that the maximum number of incidents occurs at
    def get_max_coords(self,data_struct,max_count,column_name):
        if column_name == "volume": # for traffic volume 2016 and 2017 files
            temp = data_struct.loc[data_struct.volume == max_count,'the_geom'].tolist()[0]
            return temp
        if column_name == "VOLUME": # for traffic volume 2018 file
            temp = data_struct.loc[data_struct.VOLUME == max_count,'multilinestring'].tolist()[0]
            return temp
        if column_name == "Count":  # for traffic incidents 2016, 2017, and 2018 files
            temp = data_struct.loc[data_struct.Count == max_count,'location'].tolist()[0]
            return temp


class Analyzer:

    def __init__(self):
        # connects to the cluster hosted on MongoDB Atlas (cloud database created for this project)
        cluster = pymongo.MongoClient("mongodb+srv://User_1:1234@cluster-project.mmhhg.mongodb.net/ENSF592-DataCity?retryWrites=true&w=majority")
        # clarifies database that will be used for this application
        self.db = cluster["ENSF592-DataCity"]

    # This will read all of the traffic volume documents from the database and get the max volume for
    # each year. It will return a list of these volume maxes.
    def read_all_traffic_volumes(self):
        # This will read the 2016 traffic volume document from the db, convert it to a pandas dataframe
        # object, remove the _id column MongoDB adds (we won't need to work or display this column),
        # and find the max value in the column labeled 'volume'.
        year1a = "2016"
        collection1a = self.db["CityofCalgary - Traffic Volumes"]
        t_v_input_raw1a = collection1a.find_one({})
        df_t_v_input_raw1a = pd.DataFrame(t_v_input_raw1a)
        changed_raw1a = df_t_v_input_raw1a.drop(columns=['_id'])
        temps1a = changed_raw1a['volume'].max()

        # This will read the 2017 traffic volume document from the db, convert it to a pandas dataframe
        # object, remove the _id column MongoDB adds (we won't need to work or display this column),
        # and find the max value in the column labeled 'volume'.
        year2a = "2017"
        collection2a = self.db["CityofCalgary - Traffic Volumes 2"]
        t_v_input_raw2a = collection2a.find_one({})
        df_t_v_input_raw2a = pd.DataFrame(t_v_input_raw2a)
        changed_raw2a = df_t_v_input_raw2a.drop(columns=['_id'])
        temps2a = changed_raw2a['volume'].max()

        # This will read the 2018 traffic volume document from the db, convert it to a pandas dataframe
        # object, remove the _id column MongoDB adds (we won't need to work or display this column),
        # and find the max value in the column labeled 'volume'.
        year3a = "2018"
        collection3a = self.db["CityofCalgary - Traffic Volumes 3"]
        t_v_input_raw3a = collection3a.find_one({})
        df_t_v_input_raw3a = pd.DataFrame(t_v_input_raw3a)
        changed_raw3a = df_t_v_input_raw3a.drop(columns=['_id'])
        temps3a = changed_raw3a['VOLUME'].max()

        # This calls the create_lists function to create a list of the 3 max values calculated above
        # representing the traffic volumes for 2016, 2017, and 2018.
        result = self.create_lists(temps1a, temps2a, temps3a)
        return result
    
    # This will read all of the traffic incidents documents from the database and return the max incidents for
    # a location for each year. It will return a list of these incident max values.
    def read_all_traffic_incidents(self):
        # Creates an instance of the DBReader class so we can access and use the functions we need
        temp_reader = DBReader()

        # This will read the 2016 traffic incidents document from the db, convert it to a pandas dataframe
        # object, remove the _id column MongoDB adds (we won't need to work or display this column),
        # and get the max incident value from the column labeled 'Count'.
        collection1 = self.db["CityofCalgary - Traffic Incidents"]
        column_head = 'Count'
        t_i_input_raw1 = collection1.find_one({})
        df_t_i_input_raw1 = pd.DataFrame(t_i_input_raw1)
        changed_raw1 = df_t_i_input_raw1.drop(columns=['_id'])
        placeholder_1 = temp_reader.group_by_count(changed_raw1,column_head)
        temps1 = temp_reader.get_max_count(placeholder_1,column_head)

        # This will read the 2017 traffic incidents document from the db, convert it to a pandas dataframe
        # object, remove the _id column MongoDB adds (we won't need to work or display this column),
        # and get the max incident value from the column labeled 'Count'.
        collection2 = self.db["CityofCalgary - Traffic Incidents 2"]
        column_head = 'Count'
        t_i_input_raw2 = collection2.find_one({})
        df_t_i_input_raw2 = pd.DataFrame(t_i_input_raw2)
        changed_raw2 = df_t_i_input_raw2.drop(columns=['_id'])
        placeholder_2 = temp_reader.group_by_count(changed_raw2,column_head)
        temps2 = temp_reader.get_max_count(placeholder_2,column_head)

        # This will read the 2018 traffic incidents document from the db, convert it to a pandas dataframe
        # object, remove the _id column MongoDB adds (we won't need to work or display this column),
        # and get the max incident value from the column labeled 'Count'.
        collection3 = self.db["CityofCalgary - Traffic Incidents 3"]
        column_head = 'Count'
        t_i_input_raw3 = collection3.find_one({})
        df_t_i_input_raw3 = pd.DataFrame(t_i_input_raw3)
        changed_raw3 = df_t_i_input_raw3.drop(columns=['_id'])
        placeholder_3 = temp_reader.group_by_count(changed_raw3,column_head)
        temps3 = temp_reader.get_max_count(placeholder_3,column_head)

        # This calls the creat_lists function to create a list of the 3 max values calculated above
        # representing the traffic incident counts for 2016, 2017, and 2018.
        result = self.create_lists(temps1, temps2, temps3)
        return result
        
    # This function will accept three values and create a list of those 3 values.
    def create_lists(self,val1,val2,val3):
        max_list = [val1,val2,val3]
        return max_list

