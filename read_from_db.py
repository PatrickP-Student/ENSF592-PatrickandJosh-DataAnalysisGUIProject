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
import matplotlib.pyplot as plt
import numpy as np

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

        return changed_raw

    
    def traffic_incidents(self,collection_name):
        # connects to collection holding the 2016 Traffic Volume object
        collection = db[collection_name]

        # this reads the document from the db
        traffic_incident_input_raw = collection.find_one({})

        # this converts the document to a pandas type object    
        df_traffic_incident_input_raw = pd.DataFrame(traffic_incident_input_raw)

        # this removes the obbject _id column MongoDB adds to the document, we will not need this data
        changed_raw = df_traffic_incident_input_raw.drop(columns=['_id'])

        return changed_raw
    

    # this sorts the data by descending order of the volume column
    def sort(self,data_struct,column):
        temp = data_struct.sort_values(column,ascending=False)
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

        result = self.create_lists(temps1a, temps2a, temps3a)
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
        

    def create_lists(self,val1,val2,val3):
        sum_list = [val1,val2,val3]
        return sum_list

    #TODO Might need to pass a y-axis label to this as well, based on an if statement
    def histogram_plot(self,list_x,list_y):
        y_pos = np.arange(len(list_x))
        plt.bar(y_pos, list_y, align='center', alpha=0.5)
        plt.xticks(y_pos, list_x)
        plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        plt.xlabel('Years')
        plt.ylabel('TBD*****')
        plt.show()


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
    # collection_name = "CityofCalgary - Traffic Volumes 3"
    # temp_raw = db_reader.traffic_volumes(collection_name)
    # # print(temp_raw)

    # #if sort button is clicked
    # if collection_name == "CityofCalgary - Traffic Volumes" or collection_name == "CityofCalgary - Traffic Volumes 2":
    #     temp_sorted = db_reader.sort(temp_raw,'volume')
    # if collection_name == "CityofCalgary - Traffic Volumes 3":
    #     temp_sorted = db_reader.sort(temp_raw,'VOLUME')
    # ##TODO Need to specific correct column header ' ' to sort dataframe by....
    # if collection_name == "CityofCalgary - Traffic Incidents" or collection_name == "CityofCalgary - Traffic Incidents2" or collection_name == "CityofCalgary - Traffic Incidents 3":
    #     temp_sorted = db_reader.sory(temp_raw,'START_DT')
    
    # print(temp_sorted)

    # temp = db_reader.traffic_incidents("CityofCalgary - Traffic Incidents")
    # print(temp)

    file_analyzer = Analyzer()
    other = file_analyzer.read_all_traffic_volumes()
    print(other)
    years = ["2016", "2017", "2018"]
    file_analyzer.histogram_plot(years, other)