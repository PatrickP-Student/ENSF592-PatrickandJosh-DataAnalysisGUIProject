'''
Filename: read_from_db.py
Author: Patrick Pickard
Date: July 17, 2020 - Friday
Description: This script will read 6 list objects (with nested lists in elements) from the database,
and perform all processing, sorting, and handling required for use in our program.
'''

import pymongo
from pymongo import MongoClient
import pandas as pd

#******************************************************************************************************#

#TODO LIST: Need to figure out how we are going to sort incidents for the max value, and implement method
##Ideas - Possibly append data to a new list, count instances (of whatever our criteria is to be), and 
## return the max value? ****How is this value/location max incidents value to be "displayed"

#******************************************************************************************************#

class DBReader:

    def traffic_volumes(self,collection_name):
        # connects to collection holding the 2016 Traffic Volume object
        collection = db[collection_name]

        # this reads the document from the db
        traffic_vol_input_raw = collection.find_one({})

        # this converts the document to a pandas type object    
        df_traffic_vol_input_raw = pd.DataFrame(traffic_vol_input_raw)

        # this removes the obbject _id column MongoDB adds to the document, we will not need this data
        changed_raw = df_traffic_vol_input_raw.drop(columns=['_id'])

        # this sorts the data by descending order of the volume column
        # this will handle the 2 different naming conventions for the column headers in the different
        # files being read, ie, lowercase 'volume', and uppercase 'VOLUME'.
        ## TODO There has got to be a better way to do this....
        try:
            temp = changed_raw.sort_values('volume',ascending=False)
            return temp
        except KeyError as e:
            temp = changed_raw.sort_values('VOLUME',ascending=False)
            return temp
    
    def traffic_incidents(self,collection_name):
        # connects to collection holding the 2016 Traffic Volume object
        collection = db[collection_name]

        # this reads the document from the db
        traffic_incident_input_raw = collection.find_one({})

        # this converts the document to a pandas type object    
        df_traffic_incident_input_raw = pd.DataFrame(traffic_incident_input_raw)

        # this removes the obbject _id column MongoDB adds to the document, we will not need this data
        changed_raw = df_traffic_incident_input_raw.drop(columns=['_id'])

        # this sorts the data by descending order of the volume column
        ## TODO Need to specific correct column header ' ' to sort dataframe by....
        temp = changed_raw.sort_values('START_DT',ascending=False)
        return temp

class Analyzer:

    def read_all_traffic_volumes(self):
        #This is for traffic volumes

        year1a = "2016"
        collection1a = db["CityofCalgary - Traffic Volumes"]
        t_v_input_raw1a = collection1a.find_one({})
        df_t_v_input_raw1a = pd.DataFrame(t_v_input_raw1a)
        changed_raw1a = df_t_v_input_raw1a.drop(columns=['_id'])
        temps1a = changed_raw1a['volume'].sum()

        year2a = "2017"
        collection2a = db["CityofCalgary - Traffic Volumes 2"]
        t_v_input_raw2a = collection2a.find_one({})
        df_t_v_input_raw2a = pd.DataFrame(t_v_input_raw2a)
        changed_raw2a = df_t_v_input_raw2a.drop(columns=['_id'])
        temps2a = changed_raw2a['volume'].sum()

        year3a = "2018"
        collection3a = db["CityofCalgary - Traffic Volumes 3"]
        t_v_input_raw3a = collection3a.find_one({})
        df_t_v_input_raw3a = pd.DataFrame(t_v_input_raw3a)
        changed_raw3a = df_t_v_input_raw3a.drop(columns=['_id'])
        temps3a = changed_raw3a['VOLUME'].sum()

        result = self.create_dict( year1a, temps1a, year2a, temps2a, year3a, temps3a)
        return result
    
    #TODO COMPLETE THIS SECTION
    def read_all_traffic_incidents(self):
        #This is for traffic Incidents

        collection1 = db["CityofCalgary - Traffic Incidents"]
        t_i_input_raw1 = collection1.find_one({})
        df_t_i_input_raw1 = pd.DataFrame(t_i_input_raw1)
        changed_raw1 = df_t_i_input_raw1.drop(columns=['_id'])
        #TODO Specify the axis name to sum
        changed_raw1.sum(axis = 'TBD')

        collection2 = db["CityofCalgary - Traffic Incidents 2"]
        traffic_incident_input_raw = collection2.find_one({})

        collection3 = db["CityofCalgary - Traffic Incidents 3"]
        traffic_incident_input_raw = collection3.find_one({})
        

    def create_dict(self,year1,val1,year2,val2,year3,val3):
        sum_dict = {
            year1: val1,
            year2: val2,
            year3: val3,
        }
        return sum_dict


    # def histogram_plot(self)
    

if __name__ == "__main__":
    ## TODO Maybe this should go in an __init__ ??
    # connects to the cluster hosted on MongoDB Atlas (cloud database created for this project)
    cluster = pymongo.MongoClient("mongodb+srv://User_1:1234@cluster-project.mmhhg.mongodb.net/ENSF592-DataCity?retryWrites=true&w=majority")
    #clairifies database that will be used for this application
    db = cluster["ENSF592-DataCity"]

    ####################################################################################################

    # Instantiate the DBReader class
    db_reader = DBReader()

    ## TODO will need to have the selection the user makes populate this function parameter
    ## ie, if user selects traffic volume and year 2017, we will need to pass "CityofCalgary - Traffic Volumes"
    ## collection to this argument in order to fetch the correct data from the db
    # this will pass the collection to be read from (off of the db) specific to what the user requests
    
    # temp = db_reader.traffic_volumes("CityofCalgary - Traffic Volumes 3")
    # print(temp)
    
    temp = db_reader.traffic_incidents("CityofCalgary - Traffic Incidents")
    print(temp)

    file_analyzer = Analyzer()
    other = file_analyzer.read_all_traffic_volumes()
    print(other)