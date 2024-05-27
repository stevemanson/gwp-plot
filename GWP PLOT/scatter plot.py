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


total_slab_area_m2 = 16000
total_gwp_per_area = 500

def benchmark_color_residential(y_value):
    if type(y_value) is list:
        y_value = sum(y_value)
    else:
        pass
    if y_value < 280:
       mycolor = "#4a9232"
    elif 280 < y_value < 360:
        mycolor = "#8acf30"
    elif 360 < y_value < 440:
        mycolor = "#b9ec5b"
    elif 440 < y_value < 520:
        mycolor = "#ecf10e"
    elif 520 < y_value < 600:
        mycolor = "#ffae88"
    elif 600 < y_value < 680:
        mycolor = "#ff8040"
    else:
        mycolor = "red"

    return mycolor



def button_of_dotchar():
    path1 = r"U:\Steve\LCA\data collection\GWP data - Residentail.xlsx"
    wb1 = load_workbook(path1)
    sheeta = wb1["Sheet1"]
    # message box of inputing project status
    win = tk.Tk()

    # textbox entry widget
    ttk.Label(win, text="GWP (kgCO2eq/m2)").place(x=190, y=5)

    ttk.Label(win, text="Design Development").place(x=50, y=30)
    name1 = tk.StringVar()
    name_entered1 = ttk.Entry(win, width=12, textvariable=name1).place(x=200, y=30)
    var1 = tk.IntVar()
    checkbox1 = ttk.Checkbutton(win, variable=var1, onvalue=1, offvalue=0).place(x=15, y=30)

    ttk.Label(win, text="Building Permit").place(x=50, y=70)
    name2 = tk.StringVar()
    name_entered2 = ttk.Entry(win, width=12, textvariable=name2).place(x=200, y=70)
    var2 = tk.IntVar()
    checkbox2 = ttk.Checkbutton(win, variable=var2, onvalue=1, offvalue=0).place(x=15, y=70)

    ttk.Label(win, text="Tender").place(x=50, y=110)
    name3 = tk.StringVar()
    name_entered3 = ttk.Entry(win, width=12, textvariable=name3).place(x=200, y=110)
    var3 = tk.IntVar()
    checkbox3 = ttk.Checkbutton(win, variable=var3, onvalue=1, offvalue=0).place(x=15, y=110)

    ttk.Label(win, text="IFC").place(x=50, y=150)
    name4 = tk.StringVar()
    name_entered4 = ttk.Entry(win, width=12, textvariable=name4).place(x=200, y=150)
    var4 = tk.IntVar()
    checkbox4 = ttk.Checkbutton(win, variable=var4, onvalue=1, offvalue=0).place(x=15, y=150)

    # add button
    action = ttk.Button(win, text='Confirm', command=win.destroy).place(x=200, y=190)

    win.geometry('400x250')
    win.title("Project Status")
    win.mainloop()

    X1 = [float(total_slab_area_m2)]
    Y_temp = [float(total_gwp_per_area)]

    listx = []
    r1 = 0
    for cell in sheeta['C']:
        r1 = r1 + 1
        if r1 == 1:
            pass
        else:
            listx.append(cell.value)

    # GWP TO LIST
    listy = []
    t1 = 0
    for string in sheeta['J']:
        t1 = t1 + 1
        if t1 == 1:
            pass
        else:
            listy.append(string.value)

    listx.pop(0)
    listy.pop(0)

    plt.ylabel("EMBODIED CARBON INTENSITY (KgCO2/m^2)", font='Arial')
    plt.xlabel("BUILDING AREA (m^2)", font='Arial')

    # print(listx)
    # print(listy)

    orig_map = plt.cm.get_cmap('viridis')
    reversed_map = orig_map.reversed()

    X = [0, 0]
    Y = [200, 800]

    plt.scatter(X, Y, c=Y, s=0.1, cmap=reversed_map)

    #plt.scatter(listx, listy, c=listy, alpha=0.3, cmap=reversed_map)
    plt.scatter(listx, listy, alpha=0.3, color='black')



    SD_DD = name1.get()
    if SD_DD == "":
        if var1.get() == 1:
            SD_y = Y_temp
            plt.scatter(X1, SD_y, marker= "^", s=100, color=benchmark_color_residential(SD_y))
        else:
            pass
    elif SD_DD.isnumeric() is False:
        try:
            if float(SD_DD):
                SD_y = float(SD_DD)
                plt.scatter(X1, SD_y, marker="^", alpha=0.3,s=50, color=benchmark_color_residential(SD_y))

        except ValueError:
            tkinter.messagebox.showinfo("error", "data entered is not numeric")
    else:
        SD_y = float(SD_DD)
        plt.scatter(X1, SD_y, marker= "^", alpha=0.3, s=50, color=benchmark_color_residential(SD_y))

    BP = name2.get()
    if BP == "":
        if var2.get() == 1:
            BP_y = Y_temp
            plt.scatter(X1, BP_y, marker= "D", s=100, color=benchmark_color_residential(BP_y))
        else:
            pass
    elif BP.isnumeric() is False:
        try:
            if float(BP):
                BP_y = float(BP)
                plt.scatter(X1, BP_y, marker="D", alpha=0.3,s=50, color=benchmark_color_residential(BP_y))

        except ValueError:
            tkinter.messagebox.showinfo("error", "data entered is not numeric")
    else:
        BP_y = float(BP)
        plt.scatter(X1, BP_y, marker= "D", alpha=0.3,s=50, color=benchmark_color_residential(BP_y))

    TENDER = name3.get()
    if TENDER == "":
        if var3.get() == 1:
            TENDER_y = Y_temp
            plt.scatter(X1, TENDER_y, marker= "s", s=100, color=benchmark_color_residential(TENDER_y))
        else:
            pass
    elif TENDER.isnumeric() is False:
        try:
            if float(TENDER):
                TENDER_y = float(TENDER)
                plt.scatter(X1, TENDER_y, marker="s", alpha=0.3,s=50, color=benchmark_color_residential(TENDER_y))

        except ValueError:
            tkinter.messagebox.showinfo("error", "data entered is not numeric")
    else:
        TENDER_y = float(TENDER)
        plt.scatter(X1, TENDER_y, marker= "s", alpha=0.3, s=50, color=benchmark_color_residential(TENDER_y))

    IFC = name4.get()
    if IFC == "":
        if var4.get() == 1:
            IFC_y = Y_temp
            plt.scatter(X1, IFC_y, marker= "X", s=100, color=benchmark_color_residential(IFC_y))
        else:
            pass
    elif IFC.isnumeric() is False:
        try:
            if float(IFC):
                IFC_y = float(IFC)
                plt.scatter(X1, IFC_y, marker="X", alpha=0.3,s=50, color=benchmark_color_residential(IFC_y))

        except ValueError:
            tkinter.messagebox.showinfo("error", "data entered is not numeric")
    else:
        IFC_y = float(IFC)
        plt.scatter(X1, IFC_y, marker= "X", alpha=0.3,s=50, color=benchmark_color_residential(IFC_y))



    plt.grid()
    plt.show()

button_of_dotchar()