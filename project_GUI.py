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
        reader_obj = rfd.DBReader()  # Object used to do things
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
    def tree_insert(self, df):  # df is the data frame object

        df_col = df.columns.values
        tree["columns"] = df_col
        counter = len(df)

        rowLabels = df.index.tolist()
        for x in range(0, len(df_col)):
            tree.column(x, width=80)
            tree.heading(x, text=df_col[x])
            for i in range(counter):
                tree.insert('', i, text=rowLabels[i], values=df.iloc[i, :].tolist())

        tree.grid(row=0, column=1, sticky="nsew")

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

    frame_left = tk.Frame(master=window, width=250, height=400,
                          bg="gray55")  # build the left frame that will hold all the buttons
    frame_left.columnconfigure(0, weight=1)
    frame_left.rowconfigure([0, 7], weight=1)
    frame_left.grid(column=0, sticky="nsew")

    frame_right = tk.Frame(master=window, width=1000)  # build the right frame that will hold all the data
    frame_right.columnconfigure(1, weight=1)
    frame_right.rowconfigure(0, weight=1)
    frame_right.grid(column=1, sticky="nsew")

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

    read_btn = tk.Button(  # Build Read button
        relief="solid",
        master=frame_left,
        text="Read",
        width=16,
        activebackground="tomato",
        command=app.data_types
    )
    read_btn.grid(row=2, column=0, padx=5, pady=5)

    # Instantiate the tree object
    tree = ttk.Treeview(window)

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
