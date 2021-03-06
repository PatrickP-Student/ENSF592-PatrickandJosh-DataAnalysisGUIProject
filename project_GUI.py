'''
Filename: project_GUI.py
Author: Joshua Posyluzny, Patrick Pickard
Date: July 17, 2020 - Friday
Description: The purpose of this file is to build the GUI that will handle the inputs from the
user, and display the calculated and processed data in the desired format to the user via a GUI that
will be created.
'''

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import read_from_db as rfd
import pymongo
from pymongo import errors
import folium
import re
from pandas import DataFrame


class GUI:

    # gives objects we will need to use multiple times and in multiple locations
    # full class scope so we don't need to create new ones every time we need to do
    # something different
    def __init__(self):
        self.temp = None
        self.tempSorted = None
        self.hist_flag = None
        self.analyzer_object = rfd.Analyzer()
        self.reader_obj = rfd.DBReader() 

    # Returns collection_name string for read_from_db's method parameters based on the 
    # selection of the comboboxes
    def data_types(self):
        # Each statement accounts for a scenario based on the users choice in the combo-boxes
        # and returns the corresponding dataframe displayed in the GUI
        try:
            if type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
                collection_name = "CityofCalgary - Traffic Incidents"
                self.temp = self.reader_obj.traffic_incidents(collection_name)
                self.tree_insert(self.temp)
                app.status_box_generator("Successfully Read From DB", "green2")
            elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
                collection_name = "CityofCalgary - Traffic Incidents 2"
                self.temp = self.reader_obj.traffic_incidents(collection_name)
                self.tree_insert(self.temp)
                app.status_box_generator("Successfully Read From DB", "green2")
            elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
                collection_name = "CityofCalgary - Traffic Incidents 3"
                self.temp = self.reader_obj.traffic_incidents(collection_name)
                self.tree_insert(self.temp)
                app.status_box_generator("Successfully Read From DB", "green2")
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
                collection_name = "CityofCalgary - Traffic Volumes"
                self.temp = self.reader_obj.traffic_volumes(collection_name)
                self.tree_insert(self.temp)
                app.status_box_generator("Successfully Read From DB", "green2")
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
                collection_name = "CityofCalgary - Traffic Volumes 2"
                self.temp = self.reader_obj.traffic_volumes(collection_name)
                self.tree_insert(self.temp)
                app.status_box_generator("Successfully Read From DB", "green2")
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
                collection_name = "CityofCalgary - Traffic Volumes 3"
                self.temp = self.reader_obj.traffic_volumes(collection_name)
                self.tree_insert(self.temp)
                app.status_box_generator("Successfully Read From DB", "green2")
            elif type_combo.get() == "" or year_combo.get() == "":
                app.status_box_generator("Must select data in both dropdown boxes.", "firebrick1")
        except NameError:
            app.status_box_generator("Error with data in database.", "firebrick1")
        except pymongo.errors.ConfigurationError:
            app.status_box_generator("Cannot connect to database.", "firebrick1")
        except Exception as e:
            app.status_box_generator("Unsuccessful Read: " + str(repr(e)), "firebrick1")

    # This function will take the dataframe object currently read and sort it based on descending order
    # from Incident Count or Traffic Volume
    def data_sort(self):
        # Each statement accounts for a scenario based on the users choice in the combo-boxes
        # and returns the corresponding dataframe displayed in the GUI.
        try:
            if type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
                collection_name = "CityofCalgary - Traffic Incidents"
                column_name = "Count"
                self.temp1 = self.reader_obj.group_by_count(self.temp,column_name)
                self.tempSorted = self.reader_obj.sort(self.temp1,column_name)
                self.tree_insert(self.tempSorted)
                app.status_box_generator("Successfully Sorted","green2")
            elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
                collection_name = "CityofCalgary - Traffic Incidents 2"
                column_name = "Count"
                self.temp1 = self.reader_obj.group_by_count(self.temp,column_name)
                self.tempSorted = self.reader_obj.sort(self.temp1,column_name)
                self.tree_insert(self.tempSorted)
                app.status_box_generator("Successfully Sorted","green2")
            elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
                collection_name = "CityofCalgary - Traffic Incidents 3"
                column_name = "Count"
                self.temp1 = self.reader_obj.group_by_count(self.temp,column_name)
                self.tempSorted = self.reader_obj.sort(self.temp1,column_name)
                self.tree_insert(self.tempSorted)
                app.status_box_generator("Successfully Sorted","green2")
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
                collection_name = "CityofCalgary - Traffic Volumes"
                column_name = "volume"
                self.tempSorted = self.reader_obj.sort(self.temp,column_name)
                self.tree_insert(self.tempSorted)
                app.status_box_generator("Successfully Sorted","green2")
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
                collection_name = "CityofCalgary - Traffic Volumes 2"
                column_name = "volume"
                self.tempSorted = self.reader_obj.sort(self.temp,column_name)
                self.tree_insert(self.tempSorted)
                app.status_box_generator("Successfully Sorted","green2")
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
                collection_name = "CityofCalgary - Traffic Volumes 3"
                column_name = "VOLUME"
                self.tempSorted = self.reader_obj.sort(self.temp,column_name)
                self.tree_insert(self.tempSorted)
                app.status_box_generator("Successfully Sorted","green2")
            elif type_combo.get() == "" or year_combo.get() == "":
                app.status_box_generator("Must select data in both dropdown boxes.", "firebrick1")
        except KeyError:
            app.status_box_generator("Must sort the same file that has been read.", "firebrick1")
        except AttributeError:
            app.status_box_generator("Must read the data before trying to sort.", "firebrick1")
        except Exception as e:
            app.status_box_generator("Unsuccessful Sort" + str(repr(e)), "firebrick1")

    # This function specifies column layout and headers depending on the combobox selections and physically builds
    # the chart display from the dataframe data onto the GUI.
    def tree_insert(self,df):           # df is the data frame object
        if self.hist_flag:              # if statement that says if the self.hist_flag is True:
            self.clear()                # run the self.clear() function to destroy the plot widget
        df_col = df.columns.values                  # df_col becomes a numpy array with the column header names inside
        tree["show"] = "headings"                   # this line eliminates the index column from the data
        tree["columns"] = df_col                    # specifies that the column headers will be the df_col values
        rowLabels = df.index.tolist()               # specifies that the rowLabels will be a list of the row indices
        for x in range(len(df_col)):                # starts a for loop for each column that says:
            tree.column(x, width=int(1100 / len(df_col)))  # each column in the tree will have a constant width
            tree.heading(x, text=df_col[x],
                         anchor=tk.NW)              # each heading will be assigned their respective value from df_col
            for i in range(len(df)):                # start a for loop for each row that says:
                tree.insert('', i, text=rowLabels[i],values=df.iloc[i, :].tolist())  # each row will contain the values of the dataframe rows
        tree.grid(row=0, column=1, sticky="nsew")


    # This function will get the max values for either traffic volume or traffic incidents, based
    # on year selected by user, and the corresponding coordinates, and write a marker to a folium
    # map object showing where this occurs. **Only the first block of code has been commented thoroughly
    # so as to explain the methodology behind this function, but the same exact process applies
    # to all of the if/elif code blocks in this function.
    def draw_map(self):
        try:
            # for Traffic Volumes - 2016 file
            if type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
                # specifies the column name we are searching for the max value in
                column_name = "volume"
                # calls the get_max_count function
                max_count = self.reader_obj.get_max_count(self.tempSorted,column_name)
                # calls the get_max_coords function
                holding = self.reader_obj.get_max_coords(self.tempSorted,max_count,column_name)
                # parses the coordinates multilinestring to return the only numbers
                coords = re.findall("\d+\.\d+", holding)
                # this will fetch the first 2 numbers from the above string (which will be the x and
                # y coordinates). This will be for the highest volume location as this list as been 
                # sorted already based on that criteria
                coordinate1 = float(coords[1])
                coordinate2 = float(coords[0])
                # flips the hemisphere to northern hemisphere
                coordinate2 = (-1)*coordinate2
                # creates a list of these coordinates
                latlon = [coordinate1, coordinate2]
                # builds the folium map
                m = folium.Map(location=latlon, zoom_start=12)
                # specifies the string to be displayed when mouse is hovered over the marker on map
                tooltip = '2016 - Highest Traffic Volume Location'
                # set the marker on the map based on the above coordinates
                folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
                # saves the created .html file locally
                m.save('2016TrafficVolumeMap.html')
                # updates the status box to display a successful map generation
                app.status_box_generator("Map HTML Successfully Generated", "green2")
            # for Traffic Volumes - 2017 file
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
                column_name = "volume"
                max_count = self.reader_obj.get_max_count(self.tempSorted,column_name)
                holding = self.reader_obj.get_max_coords(self.tempSorted,max_count,column_name)
                coords = re.findall("\d+\.\d+", holding)
                coordinate1 = float(coords[1])
                coordinate2 = float(coords[0])
                coordinate2 = (-1)*coordinate2
                latlon = [coordinate1, coordinate2]
                m = folium.Map(location=latlon, zoom_start=12)
                tooltip = '2017 - Highest Traffic Volume Location'
                folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
                m.save('2017TrafficVolumeMap.html')
                app.status_box_generator("Map HTML Successfully Generated", "green2")
            # for Traffic Volumes - 2018 file
            elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
                column_name = "VOLUME"
                max_count = self.reader_obj.get_max_count(self.tempSorted,column_name)
                holding = self.reader_obj.get_max_coords(self.tempSorted,max_count,column_name)
                coords = re.findall("\d+\.\d+", holding)
                coordinate1 = float(coords[1])
                coordinate2 = float(coords[0])
                coordinate2 = (-1)*coordinate2
                latlon = [coordinate1, coordinate2]
                m = folium.Map(location=latlon, zoom_start=12)
                tooltip = '2018 - Highest Traffic Volume Location'
                folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
                m.save('2018TrafficVolumeMap.html')
                app.status_box_generator("Map HTML Successfully Generated", "green2")
            # for Traffic Incidents - 2016 file
            elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
                column_name = "Count"
                max_count = self.reader_obj.get_max_count(self.tempSorted,column_name)
                holding = self.reader_obj.get_max_coords(self.tempSorted,max_count,column_name)
                coords = re.findall("\d+\.\d+", holding)
                coordinate1 = float(coords[0])
                coordinate2 = float(coords[1])
                coordinate2 = (-1)*coordinate2
                latlon = [coordinate1, coordinate2]
                m = folium.Map(location=latlon, zoom_start=12)
                tooltip = '2016 - Highest Traffic Incidents Location'
                folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
                m.save('2016TrafficIncidentsMap.html')
                app.status_box_generator("Map HTML Successfully Generated", "green2")
            # for Traffic Incidents - 2017 file
            elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
                column_name = "Count"
                max_count = self.reader_obj.get_max_count(self.tempSorted,column_name)
                holding = self.reader_obj.get_max_coords(self.tempSorted,max_count,column_name)
                coords = re.findall("\d+\.\d+", holding)
                coordinate1 = float(coords[0])
                coordinate2 = float(coords[1])
                coordinate2 = (-1)*coordinate2
                latlon = [coordinate1, coordinate2]
                m = folium.Map(location=latlon, zoom_start=12)
                tooltip = '2017 - Highest Traffic Incidents Location'
                folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
                m.save('2017TrafficIncidentsMap.html')
                app.status_box_generator("Map HTML Successfully Generated", "green2")
            # for Traffic Incidents - 2018 file
            elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
                column_name = "Count"
                max_count = self.reader_obj.get_max_count(self.tempSorted,column_name)
                holding = self.reader_obj.get_max_coords(self.tempSorted,max_count,column_name)
                coords = re.findall("\d+\.\d+", holding)
                coordinate1 = float(coords[0])
                coordinate2 = float(coords[1])
                coordinate2 = (-1)*coordinate2
                latlon = [coordinate1, coordinate2]
                m = folium.Map(location=latlon, zoom_start=12)
                tooltip = '2018 - Highest Traffic Incidents Location'
                folium.Marker(location=latlon, popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
                m.save('2018TrafficIncidentsMap.html')
                app.status_box_generator("Map HTML Successfully Generated", "green2")
            # Lets the user know they need to select options from the combo boxes to create a map
            elif self.temp == None:
                app.status_box_generator("Must select data in both dropdown boxes.", "firebrick1")
        # error handling and displaying sections
        except TypeError:
            app.status_box_generator("Must read and sort data before generating map.", "firebrick1")
        except KeyError:
            app.status_box_generator("Please sort data before writing to map.", "firebrick1")
        except Exception as e:
            app.status_box_generator("Unsuccessful Map Generation:" + str(repr(e)), "firebrick1")

    # Function to insert an embedded histogram into the window. This function uses list_x as labels for the x-axis, which
    # never changes. The if statements depend on the values that is picked from the first combobox. The data that will be
    # used for the plot is put into a dictionary called data. The class object self.bar1 is created and made into a widget,
    # and the plot is displayed inside the right frame.
    def insert_hist(self):
        if self.hist_flag:              # if statement that says if the self.hist_flag is True:
            self.clear()                # run the self.clear() function to destroy the plot widget
        try:
            list_x = ["2016", "2017", "2018"]
            if type_combo.get() == "Traffic Incidents":
                data = {"Years": list_x, "Traffic Incidents": self.analyzer_object.read_all_traffic_incidents()}
                df = DataFrame(data, columns=["Years", "Traffic Incidents"])
                figure = plt.Figure(figsize=(1, 1), dpi=80)
                ax1 = figure.add_subplot(111)
                ax1.set_ylabel("Maximum Incidents")
                self.bar1 = FigureCanvasTkAgg(figure, master=frame_right)
                self.bar1.get_tk_widget().grid(row=0, column=1, sticky="nsew")
                df = df[['Years', 'Traffic Incidents']].groupby('Years').sum()
                df.plot(kind='bar', legend=True, ax=ax1)
                ax1.set_title('Year vs Maximum Traffic Incidents')
                app.status_box_generator("Analysis Successfully Generated","green2")
                self.hist_flag = True
            elif type_combo.get() == "Traffic Volume":
                data = {"Years": list_x, "Traffic Volume": self.analyzer_object.read_all_traffic_volumes()}
                df = DataFrame(data, columns=["Years", "Traffic Volume"])
                figure = plt.Figure(figsize=(1, 1), dpi=80)
                ax1 = figure.add_subplot(111)
                ax1.set_ylabel("Maximum Volume")
                self.bar1 = FigureCanvasTkAgg(figure, master=frame_right)
                self.bar1.get_tk_widget().grid(row=0, column=1, sticky="nsew")
                df = df[['Years', 'Traffic Volume']].groupby('Years').sum()
                df.plot(kind='bar', legend=True, ax=ax1)
                ax1.set_title('Year vs Maximum Traffic Volumes')
                app.status_box_generator("Analysis Successfully Generated","green2")
                self.hist_flag = True
            elif type_combo.get() == "":
                app.status_box_generator("Must select data in both dropdown boxes.", "firebrick1")
        # Error handling statements
        except NameError:
            app.status_box_generator("Error with data in database.", "firebrick1")
        except KeyError:
            app.status_box_generator("ERROR.", "firebrick1")
        except pymongo.errors.ConfigurationError:
            app.status_box_generator("Cannot connect to database.", "firebrick1")
        except Exception as e:
            app.status_box_generator("Unsuccessful Analysis: " + str(repr(e)),"firebrick1")

    # This function builds the status box in the bottom left corner of the GUI. It takes a message and a color as parameters.
    # It is implemented in every function to indicate successes or failures.
    def status_box_generator(self, message, color):
        status_box = tk.Label(
            master=frame_left,
            height=5,
            width=25,
            wraplength=120,
            relief="solid",
            text=message,
            bg=color
        )
        status_box.grid(row=8, column=0, padx=5, pady=5, sticky="n")
    
    # This function will clear the widget object created to display the bar plot when the read or sort buttons
    # are clicked.
    def clear(self):
        self.bar1.get_tk_widget().destroy()

if __name__ == "__main__":

    # Instantiate the GUI class
    app = GUI()

    # Build the main window
    window = tk.Tk()
    window.title("Traffic Analysis")
    window.columnconfigure([0, 1], weight=1)
    window.rowconfigure(0, weight=1)
    window.geometry("1300x500")
    window.propagate(False)

    # Build the left frame, which will hold all the buttons
    frame_left = tk.Frame(master=window, width=100, height=400,
                          bg="gray55")
    frame_left.columnconfigure(0, weight=1, minsize=200)
    frame_left.rowconfigure([0, 8], weight=1, minsize=100)
    frame_left.grid(column=0, sticky="nsew")
    frame_left.grid_propagate(False)

    # Build the right frame that will hold all the data
    frame_right = tk.Frame(master=window, width=1000, height=400)
    frame_right.columnconfigure(1, weight=1)
    frame_right.rowconfigure(0, weight=1)
    frame_right.grid(row=0, column=1, sticky="nsew")
    frame_right.grid_propagate(False)

    # Instantiate the tree object
    tree = ttk.Treeview(frame_right)

    # Build the comboboxes and buttons that will be held in the left frame
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
        activebackground="bisque",
        command= app.data_types
    )
    read_btn.grid(row=2, column=0, padx=5, pady=5)

    sort_btn = tk.Button(  # Build Sort button
        relief="solid",
        master=frame_left,
        text="Sort",
        activebackground="bisque",
        width=16,
        command = app.data_sort
    )
    sort_btn.grid(row=3, column=0, padx=5, pady=5)

    analysis_btn = tk.Button(  # Build Analysis button
        relief="solid",
        master=frame_left,
        text="Analysis",
        activebackground="bisque",
        width=16,
        command=app.insert_hist
    )
    analysis_btn.grid(row=4, column=0, padx=5, pady=5)

    map_btn = tk.Button(  # Build Map button
        relief="solid",
        master=frame_left,
        text="Map",
        activebackground="bisque",
        width=16,
        command = app.draw_map
    )
    map_btn.grid(row=5, column=0, padx=5, pady=5)

    status_label = tk.Label(  # Build status label
        master=frame_left,
        text="Status:",
        bg="gray55"
    )
    status_label.grid(row=7, column=0, padx=5, sticky="w")

    app.status_box_generator("","white")

    window.mainloop()
