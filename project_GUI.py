"""
The purpose of this program is to build the GUI that will read, sort, and analyze the provided traffic data.
"""

import tkinter as tk
from tkinter import ttk
import read_from_db as read


# Define data_types() function which gets the selections from the comboboxes and returns the collection name, to be passed
# to the read_from_db.py file

def data_types():
    if type_combo.get() == "Traffic Incidents" and year_combo.get() == "2016":
        return "CityofCalgary - Traffic Incidents"
    elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2017":
        return "CityofCalgary - Traffic Incidents 2"
    elif type_combo.get() == "Traffic Incidents" and year_combo.get() == "2018":
        return "CityofCalgary - Traffic Incidents 3"
    elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2016":
        return "CityofCalgary - Traffic Volumes"
    elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2017":
        return "CityofCalgary - Traffic Volumes 2"
    elif type_combo.get() == "Traffic Volume" and year_combo.get() == "2018":
        return "CityofCalgary - Traffic Volumes 3"


window = tk.Tk()
window.title("Traffic Analysis")
window.columnconfigure([0,1], weight = 1)
window.rowconfigure(0, weight = 1)

frame_left = tk.Frame(master = window, width = 250, height = 400, bg = "gray55")     # build the left frame that will hold all the buttons
frame_left.grid(column = 0, sticky = "nsew")

frame_right = tk.Frame(master = window, width = 750)       # build the right frame that will hold all the data
frame_right.grid(column = 1)


type_combo = ttk.Combobox(
    values = ["Traffic Volume", "Traffic Incidents"],      # Data type combobox
    justify = "center",
    master = frame_left,
    width = 16
)
type_combo.grid(row = 0, column = 0, padx = 5, pady = 5)


year_combo = ttk.Combobox(                      # Year combobox
    values = ["2016", "2017", "2018"],
    justify = "center",
    master = frame_left,
    width = 16
)
year_combo.grid(row = 1, column = 0, padx = 5, pady = 5)


read_btn = tk.Button(                         # Build Read button
    relief = "solid",
    master = frame_left,
    text = "Read",
    width = 16,
    command = data_types
)
read_btn.grid(row = 2, column = 0, padx = 5, pady = 5)


sort_btn = tk.Button(                         # Build Sort button
    relief = "solid",
    master = frame_left,
    text = "Sort",
    width = 16
)
sort_btn.grid(row = 3, column = 0, padx = 5, pady = 5)


analysis_btn = tk.Button(                      # Build Analysis button
    relief = "solid",
    master = frame_left,
    text = "Analysis",
    width = 16
)
analysis_btn.grid(row = 4, column = 0, padx = 5, pady = 5)


map_btn = tk.Button(                           # Build Map button
    relief = "solid",
    master = frame_left,
    text = "Map",
    width = 16
)
map_btn.grid(row = 5, column = 0, padx = 5, pady = 5)


status_label = tk.Label(                        # Build status label
    master = frame_left,
    text = "Status:",
    bg = "gray55"
)
status_label.grid(row = 6, column = 0, padx = 5, sticky = "w")


status_box = tk.Label(                           # Build the status message box
    master = frame_left,
    height = 2,
    width = 16,
    wraplength = 80,
    relief = "solid",
    text = "Successfully read from DB",
    bg = "green2"
)
status_box.grid(row = 7, column = 0, padx = 5, pady = 5)


window.mainloop()



