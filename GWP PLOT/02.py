import openpyxl
from openpyxl import Workbook, load_workbook
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk


path = r"U:\Steve\LCA\data collection\GWP data - Residentail.xlsx"

wb = load_workbook(path)

sheet = wb["Sheet1"]


#message box of inputing project status
win = tk.Tk()

#textbox entry widget
ttk.Label(win, text="GWP (kgCO2eq/m2)").place(x=190, y=5)

ttk.Label(win, text="Design Development").place(x=50, y=30)
name1 = tk.StringVar()
name_entered1 = ttk.Entry(win, width=12, textvariable=name1).place(x=200, y=30)
var1 = tk.IntVar()
checkbox1 = ttk.Checkbutton(win,variable=var1,onvalue=1, offvalue=0).place(x=15, y=30)

ttk.Label(win, text="Building Permit").place(x=50, y=70)
name2 = tk.StringVar()
name_entered2 = ttk.Entry(win, width=12, textvariable=name2).place(x=200, y=70)
var2 = tk.IntVar()
checkbox2 = ttk.Checkbutton(win,variable=var2,onvalue=1, offvalue=0).place(x=15, y=70)

ttk.Label(win, text="Tender").place(x=50, y=110)
name3 = tk.StringVar()
name_entered3 = ttk.Entry(win, width=12, textvariable=name3).place(x=200, y=110)
var3 = tk.IntVar()
checkbox3 = ttk.Checkbutton(win,variable=var3,onvalue=1, offvalue=0).place(x=15, y=110)

ttk.Label(win, text="IFC").place(x=50, y=150)
name4 = tk.StringVar()
name_entered4 = ttk.Entry(win, width=12, textvariable=name4).place(x=200, y=150)
var4 = tk.IntVar()
checkbox4 = ttk.Checkbutton(win,variable=var4,onvalue=1, offvalue=0).place(x=15, y=150)


#add button
action = ttk.Button(win, text='Confirm', command= win.destroy).place(x= 200, y=190)


# #dropdown
# ttk.Label(win, text="status").grid(column=1, row=0)
# var = tk.StringVar()
# project_status = ttk.Combobox(win, width = 12, textvariable = var)
# project_status['values'] = (' SD/DD', ' BP', ' TENDER', ' IFC',)
# project_status.grid(column=1, row=1)
# project_status.current(0)

win.geometry('400x250')
win.title("Project Status")
win.mainloop()

X1 = [16870]
Y_temp = [550]



SD_DD = name1.get()
if SD_DD == "":
    if var1.get() == 1:
        SD_y = Y_temp
        plt.scatter(X1, SD_y, s=100, color="red")
    else:
        pass
elif SD_DD.isnumeric() is False:
    tkinter.messagebox.showinfo("error", "data entered is not numeric")
else:
    SD_y = float(SD_DD)
    plt.scatter(X1, SD_y, s=100, color="red")



BP = name2.get()
if BP == "":
    if var2.get() == 1:
        BP_y = Y_temp
        plt.scatter(X1, BP_y, s=100, color="black")
    else:
        pass
elif BP.isnumeric() is False:
    tkinter.messagebox.showinfo("error", "data entered is not numeric")
else:
    BP_y = float(BP)
    plt.scatter(X1, BP_y, s=100, color="black")

TENDER = name3.get()
if TENDER == "":
    if var3.get() == 1:
        TENDER_y = Y_temp
        plt.scatter(X1, TENDER_y, s=100, color="blue")
    else:
        pass
elif TENDER.isnumeric() is False:
    tkinter.messagebox.showinfo("error", "data entered is not numeric")
else:
    TENDER_y = float(TENDER)
    plt.scatter(X1, TENDER_y, s=100, color="blue")

IFC = name4.get()
if IFC == "":
    if var4.get() == 1:
        IFC_y = Y_temp
        plt.scatter(X1, IFC_y, s=100, color="green")
    else:
        pass
elif IFC.isnumeric() is False:
    tkinter.messagebox.showinfo("error", "data entered is not numeric")
else:
    IFC_y = float(IFC)
    plt.scatter(X1, IFC_y, s=100, color="green")



#AREA TO LIST
listx = []
for cell in sheet['C']:
    listx.append(cell.value)

#GWP TO LIST
listy =[]
for string in sheet['I']:
    listy.append(string.value)

listx.pop(0)
listy.pop(0)

plt.ylabel("EMBODIED CARBON INTENSITY (KgCO2/m^2)", font= 'Arial')
plt.xlabel("BUILDING AREA (m^2)", font= 'Arial')

#print(listx)
#print(listy)

orig_map=plt.cm.get_cmap('viridis')
reversed_map = orig_map.reversed()



sc=plt.scatter(listx, listy, c=listy, alpha = 0.3, cmap=reversed_map)


X = [0, 0]
Y = [200, 600]

sc2 = plt.scatter(X, Y, c=Y, s=0.1, cmap=reversed_map)




plt.grid()
plt.show()