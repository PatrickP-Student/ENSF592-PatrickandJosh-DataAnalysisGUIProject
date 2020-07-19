"""
The purpose of this program is to build the GUI that will read, sort, and analyze the provided traffic data.
"""

import tkinter as tk
from tkinter import ttk
import read_from_db as rfd
import pymongo
from pymongo import MongoClient

class GUI:

    # Returns collection_name string for read_from_db's method parameters based on the selection of the comboboxes
    def data_types(self):
        reader_obj = rfd.DBReader() # Object used to do things
        if type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
            collection_name = "CityofCalgary - Traffic Incidents"
            temp = reader_obj.traffic_incidents(collection_name)
            self.tree_insert(temp)
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
            collection_name = "CityofCalgary - Traffic Incidents 2"
            temp = reader_obj.traffic_incidents(collection_name)
            self.tree_insert(temp)
        elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
            collection_name = "CityofCalgary - Traffic Incidents 3"
            temp = reader_obj.traffic_incidents(collection_name)
            self.tree_insert(temp)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
            collection_name = "CityofCalgary - Traffic Volumes"
            temp = reader_obj.traffic_volumes(collection_name)
            self.tree_insert(temp)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
            collection_name = "CityofCalgary - Traffic Volumes 2"
            temp = reader_obj.traffic_volumes(collection_name)
            self.tree_insert(temp)
        elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
            collection_name = "CityofCalgary - Traffic Volumes 3"
            temp = reader_obj.traffic_volumes(collection_name)
            self.tree_insert(temp)


    # Specifies column layout and headers depending on the combobox selections
    def tree_insert(self,df): #df is the data frame object
        # if type_combo.get() == "Traffic Volume":
        #     tree1.grid(row=0, column=1, sticky="nwes")
        #     tree1.insert("", 0, text="First Row", values=["B1", "C1", "D1", "E1"])



        df_col = df.columns.values
        tree["columns"] = df_col
        print(df_col)
        counter = len(df) 

        rowLabels = df.index.tolist()
        for x in range(len(df_col)):
            tree.column(x, width=100)
            tree.heading(x, text=df_col[x])
            for i in range(counter):
                tree.insert('', i, text=rowLabels[i], values=df.iloc[i,:].tolist())
        
        tree.grid(row=0, column=1, sticky = "nsew")

        # elif type_combo.get() == "Traffic Incidents" and (year_combo.get() == "2016" or year_combo.get == "2017"):
        #     tree2.grid(row=0, column=1, sticky="nwes")
            
        # elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
        #     tree3.grid(row=0, column=1, sticky="nwes")
        


if __name__ == "__main__":
    # # connects to the cluster hosted on MongoDB Atlas (cloud database created for this project)
    # cluster = pymongo.MongoClient("mongodb+srv://User_1:1234@cluster-project.mmhhg.mongodb.net/ENSF592-DataCity?retryWrites=true&w=majority")
    # # clarifies database that will be used for this application
    # db = cluster["ENSF592-DataCity"]

    # Instantiate the GUI class
    app = GUI()

    window = tk.Tk()
    window.title("Traffic Analysis")
    window.columnconfigure([0, 1], weight=1)
    window.rowconfigure(0, weight=1)

    frame_left = tk.Frame(master=window, width=250, height=400, bg="gray55")  # build the left frame that will hold all the buttons
    frame_left.columnconfigure(0, weight=1)
    frame_left.rowconfigure([0, 7], weight=1)
    frame_left.grid(column=0, sticky="nsew")

    frame_right = tk.Frame(master=window, width=1000)  # build the right frame that will hold all the data
    frame_right.columnconfigure(1, weight=1)
    frame_right.rowconfigure(0, weight=1)
    frame_right.grid(column=1)

    type_combo = ttk.Combobox(
        values=["Traffic Volume", "Traffic Incidents"],  # Data type combobox
        justify="center",
        master=frame_left,
        width=16
    )
    type_combo.grid(row=0, column=0, padx=5, pady=5)

    year_combo = ttk.Combobox(  # Year combobox
        values=["2016", "2017", "2018"],
        justify="center",
        master=frame_left,
        width=16
    )
    year_combo.grid(row=1, column=0, padx=5, pady=5)
    # print(db_Reader.traffic_volumes(data_types()))

    read_btn = tk.Button(  # Build Read button
        relief="solid",
        master=frame_left,
        text="Read",
        width=16,
        activebackground="tomato",
        command= app.data_types
    )
    read_btn.grid(row=2, column=0, padx=5, pady=5)


    tree = ttk.Treeview(window)
    ### TREE1 IS FOR TRAFFIC VOLUME
    # Getting Treeview list for Traffic Volume
    tree1 = ttk.Treeview(window)

    # Creating Columns
    tree1["columns"] = ("the_geom", "year_vol", "shape_leng", "volume")

    # Formatting Columns
    tree1.column("#0", width=80, minwidth=50)
    tree1.column("the_geom", width=80, minwidth=50)
    tree1.column("year_vol", width=80, minwidth=50)
    tree1.column("shape_leng", width=80, minwidth=50)
    tree1.column("volume", width=80, minwidth=50)

    tree1.heading("#0", text="secname", anchor=tk.W)
    tree1.heading("the_geom", text="the_geom", anchor=tk.W)
    tree1.heading("year_vol", text="year_vol", anchor=tk.W)
    tree1.heading("shape_leng", text="shape_leng", anchor=tk.W)
    tree1.heading("volume", text="volume", anchor=tk.W)

    ### TREE2 IS FOR TRAFFIC INCIDENTS 2016 and 2017
    # Getting Treeview list For Traffic Incidents
    tree2 = ttk.Treeview(window)

    # Creating Columns
    tree2["columns"] = (
        "DESCRIPTION", "START_DT", "MODIFIED_DT", "QUADRANT", "Longitude", "Latitude", "location", "Count")

    # Formatting Columns
    tree2.column("#0", width=80, minwidth=50)
    tree2.column("DESCRIPTION", width=80, minwidth=50)
    tree2.column("START_DT", width=80, minwidth=50)
    tree2.column("MODIFIED_DT", width=80, minwidth=50)
    tree2.column("QUADRANT", width=80, minwidth=50)
    tree2.column("Longitude", width=80, minwidth=50)
    tree2.column("Latitude", width=80, minwidth=50)
    tree2.column("location", width=80, minwidth=50)
    tree2.column("Count", width=80, minwidth=50)

    tree2.heading("#0", text="INCIDENT INFO", anchor=tk.W)
    tree2.heading("DESCRIPTION", text="DESCRIPTION", anchor=tk.W)
    tree2.heading("START_DT", text="START_DT", anchor=tk.W)
    tree2.heading("MODIFIED_DT", text="MODIFIED_DT", anchor=tk.W)
    tree2.heading("QUADRANT", text="QUADRANT", anchor=tk.W)
    tree2.heading("Longitude", text="Longitude", anchor=tk.W)
    tree2.heading("Latitude", text="Latitude", anchor=tk.W)
    tree2.heading("location", text="location", anchor=tk.W)
    tree2.heading("Count", text="Count", anchor=tk.W)

    ### TREE3 IS FOR TRAFFIC INCIDENTS 2018
    # Getting Treeview list For Traffic Incidents
    tree3 = ttk.Treeview(window)

    # Creating Columns
    tree3["columns"] = (
        "DESCRIPTION", "START_DT", "MODIFIED_DT", "QUADRANT", "Longitude", "Latitude", "location", "Count", "id")

    # Formatting Columns
    tree3.column("#0", width=80, minwidth=50)
    tree3.column("DESCRIPTION", width=80, minwidth=50)
    tree3.column("START_DT", width=80, minwidth=50)
    tree3.column("MODIFIED_DT", width=80, minwidth=50)
    tree3.column("QUADRANT", width=80, minwidth=50)
    tree3.column("Longitude", width=80, minwidth=50)
    tree3.column("Latitude", width=80, minwidth=50)
    tree3.column("location", width=80, minwidth=50)
    tree3.column("Count", width=80, minwidth=50)
    tree3.column("id", width=80, minwidth=50)

    tree3.heading("#0", text="INCIDENT INFO", anchor=tk.W)
    tree3.heading("DESCRIPTION", text="DESCRIPTION", anchor=tk.W)
    tree3.heading("START_DT", text="START_DT", anchor=tk.W)
    tree3.heading("MODIFIED_DT", text="MODIFIED_DT", anchor=tk.W)
    tree3.heading("QUADRANT", text="QUADRANT", anchor=tk.W)
    tree3.heading("Longitude", text="Longitude", anchor=tk.W)
    tree3.heading("Latitude", text="Latitude", anchor=tk.W)
    tree3.heading("location", text="location", anchor=tk.W)
    tree3.heading("Count", text="Count", anchor=tk.W)
    tree3.heading("id", text="id", anchor=tk.W)

    sort_btn = tk.Button(  # Build Sort button
        relief="solid",
        master=frame_left,
        text="Sort",
        activebackground="tomato",
        width=16
    )
    sort_btn.grid(row=3, column=0, padx=5, pady=5)

    analysis_btn = tk.Button(  # Build Analysis button
        relief="solid",
        master=frame_left,
        text="Analysis",
        activebackground="tomato",
        width=16
    )
    analysis_btn.grid(row=4, column=0, padx=5, pady=5)

    map_btn = tk.Button(  # Build Map button
        relief="solid",
        master=frame_left,
        text="Map",
        activebackground="tomato",
        width=16
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
    status_box.grid(row=7, column=0, padx=5, pady=5)

    window.mainloop()

