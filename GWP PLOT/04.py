import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog
import customtkinter
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import openpyxl
from openpyxl import load_workbook, workbook
import warnings
import os
import PIL
from PIL import ImageTk, Image
import csv

import pandas as pd
import glob
import os

def load_data():
    global tally_xlsx_path
    warnings.simplefilter(action='ignore', category=UserWarning)
    filename = filedialog.askopenfilename(title='Please select a excel report from Tally')
    path = filename
    tally_xlsx_path = path.replace('\\', '/')
    return tally_xlsx_path


#convert to csv.
#tally_xlsx_path = r"U:\Steve\LCA\GWP baseline porjects\221109 - Highpoint\221109 - Highpoint - Tally Report - bp.xlsx"

all_sheets = pd.read_excel(load_data(), sheet_name=None)
sheets = all_sheets.keys()

x=0
temp_csv_path = r'U:\Steve\LCA\temp csv'
for sheet_name1 in sheets:
    x = x+1
    sheet = pd.read_excel(tally_xlsx_path, sheet_name = sheet_name1)
    sheet.to_csv(temp_csv_path + '\\' + str(x) + "-" + sheet_name1 + ".csv", index=False)
    sheet.to_csv_path(str(temp_csv_path + '\\' + str(x) + "-" + sheet_name1 + ".csv"))

df = pd.read_csv((r'U:\Steve\LCA\temp csv\1-Report Summary.csv'), header=0)
print(df.iat[7,1])




#delete csv

# csv_files = glob.glob(os.path.join(temp_csv_path,'*.csv'))
# for file in csv_files:
#     print("yes")
#     os.remove(file)


