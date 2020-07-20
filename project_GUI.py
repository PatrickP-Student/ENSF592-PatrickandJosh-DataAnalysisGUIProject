"""
The purpose of this program is to build the GUI that will read, sort, and analyze the provided traffic data.
"""

import tkinter as tk
from tkinter import ttk

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas
import read_from_db as rfd
import pymongo
from pymongo import MongoClient
import folium
import re
from pandas import DataFrame
import matplotlib.pyplot as plt


class GUI:

    # gives objects holding the dataframes full class scope so we don't need to read them from the
    # db everytime we want to do something with thme
    def __init__(self):
        self.temp = None
        self.tempSorted = None
        

    # Returns collection_name string for read_from_db's method parameters based on the selection of the comboboxes
    def data_types(self):
        reader_obj = rfd.DBReader() # Object used to do things
        # Each statement accounts for a scenario based on the users choice in the combo-boxes
        # and returns the corresponding dataframe displayed in the GUI
        if type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
            collection_name = "CityofCalgary - Traffic Incidents"
            self.temp = reader_obj.traffic_incidents(collection_name)
            self.tree_insert(self.temp)
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
            collection_name = "CityofCalgary - Traffic Incidents 2"
            self.temp = reader_obj.traffic_incidents(collection_name)
            self.tree_insert(self.temp)
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
            collection_name = "CityofCalgary - Traffic Incidents 3"
            self.temp = reader_obj.traffic_incidents(collection_name)
            self.tree_insert(self.temp)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
            collection_name = "CityofCalgary - Traffic Volumes"
            self.temp = reader_obj.traffic_volumes(collection_name)
            self.tree_insert(self.temp)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
            collection_name = "CityofCalgary - Traffic Volumes 2"
            self.temp = reader_obj.traffic_volumes(collection_name)
            self.tree_insert(self.temp)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
            collection_name = "CityofCalgary - Traffic Volumes 3"
            self.temp = reader_obj.traffic_volumes(collection_name)
            self.tree_insert(self.temp)

    ## TODO Figure out how to pass the self.temp objects created and held in the data_types read function
    ## , might need to also make the object instance accessible between functions as well
    # This function will take the dataframe object currently read and sort it based on descending order
    # from Incident Count or Traffic Volume
    def data_sort(self):
        reader_obj = rfd.DBReader() # Object used to do things
        # Each statement accounts for a scenario based on the users choice in the combo-boxes
        # and returns the corresponding dataframe displayed in the GUI.
        #### TODO: THE DATA MUST BE READ BEFORE IT CAN BE SORTED. NEED TO THROW AN ERROR IN THE STATUS
        #### STATUS WINDOW IF IT IS NOT
        if type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
            collection_name = "CityofCalgary - Traffic Incidents"
            column_name = "Count"
            self.temp1 = reader_obj.group_by_count(self.temp,column_name)
            self.tempSorted = reader_obj.sort(self.temp1,column_name)
            self.tree_insert(self.tempSorted)
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
            collection_name = "CityofCalgary - Traffic Incidents 2"
            column_name = "Count"
            self.temp1 = reader_obj.group_by_count(self.temp,column_name)
            self.tempSorted = reader_obj.sort(self.temp1,column_name)
            self.tree_insert(self.tempSorted)
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
            collection_name = "CityofCalgary - Traffic Incidents 3"
            column_name = "Count"
            self.temp1 = reader_obj.group_by_count(self.temp,column_name)
            self.tempSorted = reader_obj.sort(self.temp1,column_name)
            self.tree_insert(self.tempSorted)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
            collection_name = "CityofCalgary - Traffic Volumes"
            column_name = "volume"
            self.tempSorted = reader_obj.sort(self.temp,column_name)
            self.tree_insert(self.tempSorted)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
            collection_name = "CityofCalgary - Traffic Volumes 2"
            column_name = "volume"
            self.tempSorted = reader_obj.sort(self.temp,column_name)
            self.tree_insert(self.tempSorted)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
            collection_name = "CityofCalgary - Traffic Volumes 3"
            column_name = "VOLUME"
            self.tempSorted = reader_obj.sort(self.temp,column_name)
            self.tree_insert(self.tempSorted)

    #TODO Fix extra column (blank) at end of method that is added on sorting
    # Specifies column layout and headers depending on the combobox selections and physically builds
    # the chart display from the dataframe data to the GUI.
    def tree_insert(self,df): #df is the data frame object
        df_col = df.columns.values
        tree["show"] = "headings"
        tree["columns"] = df_col
        counter = len(df)

        rowLabels = df.index.tolist()
        for x in range(len(df_col)):

            tree.column(x, width=80, minwidth=80)
            tree.heading(x, text=df_col[x])
            print(x)
            for i in range(counter):
                tree.insert('', i, text=rowLabels[i], values=df.iloc[i,:].tolist())
        tree.grid(row=0, column=1, sticky = "nsew")
        
    #TODO: Check and see if Traffic Incidents maps work, waiting for left pane disappearing bug
    #to be fixed
    #############################################################################################
    # This function will get the max values for either traffic volume or traffic incidents, based
    # on year selected by user, and the corresponding coordinates, and write a marker to a folium
    # map object showing where this occurs.
    def draw_map(self):
        reader_obj = rfd.DBReader()
        if type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
            column_name = "volume"
            max_count = reader_obj.get_max_count(self.temp,column_name)
            holding = reader_obj.get_max_coords(self.temp,max_count,column_name)
            coords = re.findall("\d+\.\d+", holding)
            coordinate1 = float(coords[1])
            coordinate2 = float(coords[0])
            coordinate2 = (-1)*coordinate2
            latlon = [coordinate1, coordinate2]
            m = folium.Map(location=latlon, zoom_start=12)
            tooltip = '2016 - Highest Traffic Volume Location'
            folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
            m.save('2016TrafficVolumeMap.html')
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
            column_name = "volume"
            max_count = reader_obj.get_max_count(self.temp,column_name)
            holding = reader_obj.get_max_coords(self.temp,max_count,column_name)
            coords = re.findall("\d+\.\d+", holding)
            coordinate1 = float(coords[1])
            coordinate2 = float(coords[0])
            coordinate2 = (-1)*coordinate2
            latlon = [coordinate1, coordinate2]
            m = folium.Map(location=latlon, zoom_start=12)
            tooltip = '2017 - Highest Traffic Volume Location'
            folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
            m.save('2017TrafficVolumeMap.html')
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
            column_name = "VOLUME"
            max_count = reader_obj.get_max_count(self.temp,column_name)
            holding = reader_obj.get_max_coords(self.temp,max_count,column_name)
            coords = re.findall("\d+\.\d+", holding)
            coordinate1 = float(coords[1])
            coordinate2 = float(coords[0])
            coordinate2 = (-1)*coordinate2
            latlon = [coordinate1, coordinate2]
            m = folium.Map(location=latlon, zoom_start=12)
            tooltip = '2018 - Highest Traffic Volume Location'
            folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
            m.save('2018TrafficVolumeMap.html')
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
            column_name = "Count"
            max_count = reader_obj.get_max_count(self.temp,column_name)
            holding = reader_obj.get_max_coords(self.temp,max_count,column_name)
            coords = re.findall("\d+\.\d+", holding)
            coordinate1 = float(coords[1])
            coordinate2 = float(coords[0])
            coordinate2 = (-1)*coordinate2
            latlon = [coordinate1, coordinate2]
            m = folium.Map(location=latlon, zoom_start=12)
            tooltip = '2016 - Highest Traffic Incidents Location'
            folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
            m.save('2016TrafficIncidentsMap.html')
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
            column_name = "Count"
            max_count = reader_obj.get_max_count(self.temp,column_name)
            holding = reader_obj.get_max_coords(self.temp,max_count,column_name)
            coords = re.findall("\d+\.\d+", holding)
            coordinate1 = float(coords[1])
            coordinate2 = float(coords[0])
            coordinate2 = (-1)*coordinate2
            latlon = [coordinate1, coordinate2]
            m = folium.Map(location=latlon, zoom_start=12)
            tooltip = '2017 - Highest Traffic Incidents Location'
            folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
            m.save('2017TrafficIncidentsMap.html')
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
            column_name = "Count"
            max_count = reader_obj.get_max_count(self.temp,column_name)
            holding = reader_obj.get_max_coords(self.temp,max_count,column_name)
            coords = re.findall("\d+\.\d+", holding)
            coordinate1 = float(coords[1])
            coordinate2 = float(coords[0])
            coordinate2 = (-1)*coordinate2
            latlon = [coordinate1, coordinate2]
            m = folium.Map(location=latlon, zoom_start=12)
            tooltip = '2018 - Highest Traffic Incidents Location'
            folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
            m.save('2018TrafficIncidentsMap.html')


# Function to insert an embedded histogram into the window
# TODO: Can we make the plot go away if we try to read new data? Also see if we can set the Y axis
    def insert_hist(self):

        analyzer_object = rfd.Analyzer()
        list_x = ["2016", "2017", "2018"]
        if type_combo.get() == "Traffic Incidents":
            data = {"Years": list_x, "Traffic Incidents": analyzer_object.read_all_traffic_incidents()}
            df = DataFrame(data, columns=["Years", "Traffic Incidents"])
            figure = plt.Figure(figsize=(1, 1), dpi=100)
            ax1 = figure.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure, master=window)
            bar1.get_tk_widget().grid(row=0, column=1, sticky="nsew")
            df = df[['Years', 'Traffic Incidents']].groupby('Years').sum()
            df.plot(kind='bar', legend=True, ax=ax1)
            ax1.set_title('Year vs Traffic Incidents')

        elif type_combo.get() == "Traffic Volume":
            data = {"Years": list_x, "Traffic Volume": analyzer_object.read_all_traffic_volumes()}
            df = DataFrame(data, columns=["Years", "Traffic Volume"])
            figure = plt.Figure(figsize=(1, 1), dpi=100)
            ax1 = figure.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure, master=window)
            bar1.get_tk_widget().grid(row=0, column=1, sticky="nsew")
            df = df[['Years', 'Traffic Volume']].groupby('Years').sum()
            df.plot(kind='bar', legend=True, ax=ax1)
            ax1.set_title('Year vs Traffic Volumes')


if __name__ == "__main__":

    # Instantiate the GUI class
    app = GUI()

    window = tk.Tk()
    window.title("Traffic Analysis")
    window.columnconfigure([0, 1], weight=1)
    window.rowconfigure(0, weight=1)
    window.geometry("1300x500")
    window.propagate(False)
    # window.maxsize(width=1200,height=400)

    frame_left = tk.Frame(master=window, width=100, height=400,
                          bg="gray55")  # build the left frame that will hold all the buttons
    frame_left.columnconfigure(0, weight=1, minsize=200)
    frame_left.rowconfigure([0, 7], weight=1, minsize=100)
    frame_left.grid(column=0, sticky="nsew")
    frame_left.grid_propagate(False)


    frame_right = tk.Frame(master=window, width=1000, height=400)  # build the right frame that will hold all the data
    frame_right.columnconfigure(1, weight=1)
    frame_right.rowconfigure(0, weight=1)
    frame_right.grid(row=0, column=1, sticky="nsew")
    frame_right.grid_propagate(False)

    # Instantiate the tree object
    tree = ttk.Treeview(frame_right)


    type_combo = ttk.Combobox(
        values=["Traffic Volume", "Traffic Incidents"],  # Data type combobox
        justify="center",
        master=frame_left,
        width=16
    )
    type_combo.grid(row=0, column=0, padx=5, pady=5, sticky='s')

    year_combo = ttk.Combobox(  # Year combobox
        values=["2016", "2017", "2018"],
        justify="center",
        master=frame_left,
        width=16
    )
    year_combo.grid(row=1, column=0, padx=5, pady=5)

    read_btn = tk.Button(  # Build Read button
        relief="solid",
        master=frame_left,
        text="Read",
        width=16,
        activebackground="tomato",
        command=app.data_types
    )
    read_btn.grid(row=2, column=0, padx=5, pady=5)

    sort_btn = tk.Button(  # Build Sort button
        relief="solid",
        master=frame_left,
        text="Sort",
        activebackground="tomato",
        width=16,
        command = app.data_sort
    )
    sort_btn.grid(row=3, column=0, padx=5, pady=5)

    analysis_btn = tk.Button(  # Build Analysis button
        relief="solid",
        master=frame_left,
        text="Analysis",
        activebackground="tomato",
        width=16,
        command=app.insert_hist
    )
    analysis_btn.grid(row=4, column=0, padx=5, pady=5)

    map_btn = tk.Button(  # Build Map button
        relief="solid",
        master=frame_left,
        text="Map",
        activebackground="tomato",
        width=16,
        command = app.draw_map
    )
    map_btn.grid(row=5, column=0, padx=5, pady=5)

    status_label = tk.Label(  # Build status label
        master=frame_left,
        text="Status:",
        bg="gray55"
    )
    status_label.grid(row=6, column=0, padx=5, sticky="w")

    status_box = tk.Label(  # Build the status message box
        master=frame_left,
        height=3,
        width=16,
        wraplength=85,
        relief="solid",
        text="Successfully read from DB",
        bg="green2"
    )
    status_box.grid(row=7, column=0, padx=5, pady=5, sticky="n")

    window.mainloop()
