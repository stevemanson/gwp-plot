import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import numpy as np
import math

excel_path = r"\\GS-STORAGE\Engineer\Sustainability Committee\GWP Tools\Concrete Spreadsheets\20231121_Master GWP File_rgh.xlsx"
conc_sheet_name = "Concrete"
steel_sheet_name = "Steel"

def element_changed(temp):
    print("element changed")
    element = element_combo.get()
    widgets = window.grid_slaves(row = 1, column=0)

    for widget in widgets:
        widget.grid_forget()

    if element =="Column":
        column_frame.grid(row=1,column=0,sticky='NSEW', padx=5, pady=5)
    elif element =="Beam":
        beam_frame.grid(row=1,column=0,sticky='NSEW', padx=5, pady=5)
    elif element =="Wall":
        wall_frame.grid(row=1,column=0,sticky='NSEW', padx=5, pady=5)
    elif element =="Slab":
        slab_frame.grid(row=1,column=0,sticky='NSEW', padx=5, pady=5)
    elif element =="Footing":
        footing_frame.grid(row=1,column=0,sticky='NSEW', padx=5, pady=5)

    update_conc_gwp()

def units_changed(temp):
    print("units changed")
    units = units_combo.get()
    if units == "Imperial":
        
        dim_unit_label_list = [col_unit3,col_unit4,col_unit5,col_unit6,col_unit7,col_unit8,
                           beam_unit3,beam_unit4,beam_unit5,beam_unit6,beam_unit7,beam_unit8,
                           wall_unit3,wall_unit4,wall_unit5,wall_unit6,wall_unit7,wall_unit8,
                           slab_unit3,slab_unit4,slab_unit5,slab_unit6,slab_unit7,slab_unit8,
                           footing_unit3,footing_unit4,footing_unit5,footing_unit6,footing_unit7,footing_unit8]
        
        for label in dim_unit_label_list:
            label["text"]="ft"
        
    elif units =="Metric":
        
        dim_unit_label_list = [col_unit3,col_unit4,col_unit5,col_unit6,col_unit7,col_unit8,
                           beam_unit3,beam_unit4,beam_unit5,beam_unit6,beam_unit7,beam_unit8,
                           wall_unit3,wall_unit4,wall_unit5,wall_unit6,wall_unit7,wall_unit8,
                           slab_unit3,slab_unit4,slab_unit5,slab_unit6,slab_unit7,slab_unit8,
                           footing_unit3,footing_unit4,footing_unit5,footing_unit6,footing_unit7,footing_unit8]
       
        for label in dim_unit_label_list:
            label["text"]="m"

def region_changed(temp):
    print("Region changed")
    region = region_combo.get()
    conc_grades = get_conc_grades(region)
    locations = get_locations(region)

    if region == "CANADA":
        location_combo["values"] = locations
        location_combo.current(0)

        col_conc_combo1["values"] = conc_grades
        col_conc_combo2["values"] = conc_grades
        beam_conc_combo1["values"] = conc_grades
        beam_conc_combo2["values"] = conc_grades
        slab_conc_combo1["values"] = conc_grades
        slab_conc_combo2["values"] = conc_grades
        wall_conc_combo1["values"] = conc_grades
        wall_conc_combo2["values"] = conc_grades
        footing_conc_combo1["values"] = conc_grades
        footing_conc_combo2["values"] = conc_grades

        col_conc_combo1.current(3)
        col_conc_combo2.current(3)
        beam_conc_combo1.current(3)
        beam_conc_combo2.current(3)
        slab_conc_combo1.current(3)
        slab_conc_combo2.current(3)
        wall_conc_combo1.current(3)
        wall_conc_combo2.current(3)
        footing_conc_combo1.current(3)
        footing_conc_combo2.current(3)
        
        fc_unit_label_list = [col_unit1,col_unit2,
                           beam_unit1,beam_unit2,
                           wall_unit1,wall_unit2,
                           slab_unit1,slab_unit2,
                           footing_unit1,footing_unit2]
        
        for label in fc_unit_label_list:
            label["text"]="MPa"

    else:
        location_combo["values"] = locations
        location_combo.current(0)

        col_conc_combo1["values"] = conc_grades
        col_conc_combo2["values"] = conc_grades
        beam_conc_combo1["values"] = conc_grades
        beam_conc_combo2["values"] = conc_grades
        slab_conc_combo1["values"] = conc_grades
        slab_conc_combo2["values"] = conc_grades
        wall_conc_combo1["values"] = conc_grades
        wall_conc_combo2["values"] = conc_grades
        footing_conc_combo1["values"] = conc_grades
        footing_conc_combo2["values"] = conc_grades

        col_conc_combo1.current(3)
        col_conc_combo2.current(3)
        beam_conc_combo1.current(3)
        beam_conc_combo2.current(3)
        slab_conc_combo1.current(3)
        slab_conc_combo2.current(3)
        wall_conc_combo1.current(3)
        wall_conc_combo2.current(3)
        footing_conc_combo1.current(3)
        footing_conc_combo2.current(3)
        
        fc_unit_label_list = [col_unit1,col_unit2,
                           beam_unit1,beam_unit2,
                           wall_unit1,wall_unit2,
                           slab_unit1,slab_unit2,
                           footing_unit1,footing_unit2]
        
        for label in fc_unit_label_list:
            label["text"]="psi"

    update_conc_gwp()

def location_changed(temp):
    print("Location changed")
    update_conc_gwp()

def grade_changed(temp):
    print("Concrete Grade changed")
    update_conc_gwp()

def get_volume(l,b,h):
    vol = l*b*h
    return vol

def get_conc_grades(region):
    global excel_path
    global conc_sheet_name
    if region == "CANADA":
        df = pd.read_excel(excel_path, sheet_name= conc_sheet_name)
        conc_grades = df.iloc[5:16,1].tolist()
        
    else:
        df = pd.read_excel(excel_path, sheet_name= conc_sheet_name)
        conc_grades = df.iloc[23:34,1].tolist()

    conc_grades = [value for value in conc_grades if not pd.isna(value)]
    return conc_grades

def get_locations(region):
    global excel_path
    global conc_sheet_name
    if region == "CANADA":
        df = pd.read_excel(excel_path, sheet_name= conc_sheet_name)
        locations = df.iloc[2,2:16].tolist()
    else:
        df = pd.read_excel(excel_path, sheet_name= conc_sheet_name)
        locations = df.iloc[20,2:20].tolist()

    locations = [value for value in locations if not pd.isna(value)]
    locations.append("Custom")
    return locations

def update_conc_gwp():
    global excel_path
    global conc_sheet_name

    region = region_combo.get()
    location = location_combo.get()
    element = element_combo.get()

    if element =="Column":
        conc_grade_1 = col_conc_combo1.get()
        conc_grade_2 = col_conc_combo2.get()
    elif element =="Beam":
        conc_grade_1 = beam_conc_combo1.get()
        conc_grade_2 = beam_conc_combo2.get()
    elif element =="Wall":
        conc_grade_1 = wall_conc_combo1.get()
        conc_grade_2 = wall_conc_combo2.get()
    elif element =="Slab":
        conc_grade_1 = slab_conc_combo1.get()
        conc_grade_2 = slab_conc_combo2.get()
    elif element =="Footing":
        conc_grade_1 = footing_conc_combo1.get()
        conc_grade_2 = footing_conc_combo2.get()

    global excel_path
    global conc_sheet_name
  
    df = pd.read_excel(excel_path, sheet_name= conc_sheet_name).astype(str)

    # Find row of grade
    column_index = 1
    rows, cols = np.where(df.isin([conc_grade_1]))
    unique_rows = list(np.unique(rows))

    if unique_rows == []:
        opt_1_row = "Not found"
    else:
        opt_1_row = unique_rows[0]

    rows,cols = np.where(df.isin([conc_grade_2]))
    unique_rows = list(np.unique(rows))
    
    if unique_rows == []:
        opt_2_row = "Not found"
    else:
        opt_2_row = unique_rows[0]
    
    # Find col of location
    rows, cols = np.where(df.isin([str(location)]))
    unique_rows = list(np.unique(rows))
    unique_cols = list(np.unique(cols))

    if unique_cols == []:
        opt_1_col = "Not found"
        opt_2_col = "Not found"
    else:
        opt_1_col = unique_cols[0]
        opt_2_col = unique_cols[0]

    if opt_1_row == "Not found" or opt_1_col == "Not found":
        if element =="Column":
            col_gwp_conc_entry1.delete(0,tk.END)
            col_gwp_conc_entry1.insert(0,"")
        elif element =="Beam":
            beam_gwp_conc_entry1.delete(0,tk.END)
            beam_gwp_conc_entry1.insert(0,"")
        elif element =="Wall":
            wall_gwp_conc_entry1.delete(0,tk.END)
            wall_gwp_conc_entry1.insert(0,"")
        elif element =="Slab":
            slab_gwp_conc_entry1.delete(0,tk.END)
            slab_gwp_conc_entry1.insert(0,"")
        elif element =="Footing":
            footing_gwp_conc_entry1.delete(0,tk.END)
            footing_gwp_conc_entry1.insert(0,"")

    if opt_2_row == "Not found" or opt_2_col == "Not found":
        if element =="Column":
            col_gwp_conc_entry2.delete(0,tk.END)
            col_gwp_conc_entry2.insert(0,"")
        elif element =="Beam":
            beam_gwp_conc_entry2.delete(0,tk.END)
            beam_gwp_conc_entry2.insert(0,"")
        elif element =="Wall":
            wall_gwp_conc_entry2.delete(0,tk.END)
            wall_gwp_conc_entry2.insert(0,"")
        elif element =="Slab":
            slab_gwp_conc_entry2.delete(0,tk.END)
            slab_gwp_conc_entry2.insert(0,"")
        elif element =="Footing":
            footing_gwp_conc_entry2.delete(0,tk.END)
            footing_gwp_conc_entry2.insert(0,"")

    if opt_1_row != "Not found" and opt_1_col != "Not found":
        result = df.iloc[opt_1_row,opt_1_col]
        if element =="Column":
            col_gwp_conc_entry1.delete(0,tk.END)
            col_gwp_conc_entry1.insert(0,result)
        elif element =="Beam":
            beam_gwp_conc_entry1.delete(0,tk.END)
            beam_gwp_conc_entry1.insert(0,result)
        elif element =="Wall":
            wall_gwp_conc_entry1.delete(0,tk.END)
            wall_gwp_conc_entry1.insert(0,result)
        elif element =="Slab":
            slab_gwp_conc_entry1.delete(0,tk.END)
            slab_gwp_conc_entry1.insert(0,result)
        elif element =="Footing":
            footing_gwp_conc_entry1.delete(0,tk.END)
            footing_gwp_conc_entry1.insert(0,result)
        
    if opt_2_row != "Not found" and opt_2_col != "Not found":
        result = df.iloc[opt_2_row,opt_2_col]
        if element =="Column":
            col_gwp_conc_entry2.delete(0,tk.END)
            col_gwp_conc_entry2.insert(0,result)
        elif element =="Beam":
            beam_gwp_conc_entry2.delete(0,tk.END)
            beam_gwp_conc_entry2.insert(0,result)
        elif element =="Wall":
            wall_gwp_conc_entry2.delete(0,tk.END)
            wall_gwp_conc_entry2.insert(0,result)
        elif element =="Slab":
            slab_gwp_conc_entry2.delete(0,tk.END)
            slab_gwp_conc_entry2.insert(0,result)
        elif element =="Footing":
            footing_gwp_conc_entry2.delete(0,tk.END)
            footing_gwp_conc_entry2.insert(0,result)


statements=["\"Your green choices are like ripples in a pond, spreading positive change.\"",
"\"You're helping to preserve the natural beauty of our planet.\"",
"\"With every sustainable decision, you're part of the solution.\"",
"\"You're a sustainability superstar!\"",
"\"Your environmental stewardship is making our world a better place.\"",
"\"Your eco-conscious actions are a beacon of hope for a brighter future.\"",
"\"You're paving the way for a more sustainable way of life.\"",
"\"Every day you choose sustainability is a win for the environment.\"",
"\"You're showing that every individual can make a meaningful impact.\"",
"\"Your planet-friendly choices are like seeds of positive change.\"",
"\"Your efforts are helping to protect endangered species and habitats.\"",
"\"You're reducing your ecological footprint one step at a time.\"",
"\"You're turning challenges into opportunities for sustainability.\"",
"\"Thank you for being a guardian of our fragile ecosystems.\"",
"\"Your sustainable choices are a testament to your care for the Earth.\"",
"\"Your actions are a vital part of the global sustainability movement.\"",
"\"You're creating a legacy of responsible environmental stewardship.\"",
"\"Your commitment to sustainability is building a better tomorrow.\"",
"\"Your environmental awareness is an inspiration to those around you.\"",
"\"You're contributing to a more resilient and sustainable world.\"",
"\"You're making a real difference in the fight against climate change!\"",
"\"Your eco-conscious choices are helping to reduce emissions.\"",
"\"Every sustainable action you take counts toward a cleaner Earth.\"",
"\"Thank you for being a guardian of our planet.\"",
"\"Your environmental efforts are truly commendable.\"",
"\"With each eco-friendly decision, you're leading the way.\"",
"\"You're turning the tide for a greener future.\"",
"\"Your commitment to sustainability is inspiring.\"",
"\"Small changes add up to big improvements—keep it up!\"",
"\"You're setting a positive example for others to follow.\"",
"\"Your green choices are a breath of fresh air for our planet.\"",
"\"You're helping to protect biodiversity and ecosystems.\"",
"\"Every sustainable step you take brings us closer to a sustainable world.\"",
"\"Your actions are a beacon of hope for a cleaner Earth.\"",
"\"You're reducing your carbon footprint and making a positive impact.\"",
"\"Your eco-friendly choices are a gift to future generations.\"",
"\"By choosing sustainability, you're part of the solution.\"",
"\"You're fostering a culture of environmental responsibility.\"",
"\"Your dedication to the environment is truly inspiring.\"",
"\"You're contributing to a healthier, more sustainable world.\"",]

def calculate_gwp():
    try:
        element = element_combo.get()
        units = units_combo.get()
        region = region_combo.get()

        if units == "Imperial":
            unit_factor = 0.3048 #converting to m as GWP value is in /m3
        else:
            unit_factor = 1

        if element == "Column":
            l1 = float(col_height_entry1.get())*unit_factor
            l2 = float(col_height_entry2.get())*unit_factor

            b1 = float(col_width_entry1.get())*unit_factor
            b2 = float(col_width_entry2.get())*unit_factor

            h1 = float(col_depth_entry1.get())*unit_factor
            h2 = float(col_depth_entry2.get())*unit_factor

            rr1 = float(col_ratio_entry1.get())
            rr2 = float(col_ratio_entry2.get())

            vc1 = get_volume(l1,b1,h1)*(1-rr1/100)
            vc2 = get_volume(l2,b2,h2)*(1-rr2/100)
            vs1 = get_volume(l1,b1,h1)*rr1/100
            vs2 = get_volume(l2,b2,h2)*rr2/100

            gwp_per_m3_1 = float(col_gwp_conc_entry1.get())
            gwp_per_m3_2 = float(col_gwp_conc_entry2.get())
            gwp_per_mt = float(gwp_steel_entry.get())

            gwpc1 = vc1*gwp_per_m3_1
            gwpc2 = vc2*gwp_per_m3_2

            gwps1 = vs1*7.85*gwp_per_mt
            gwps2 = vs2*7.85*gwp_per_mt
            
            gwp1 = gwpc1 + gwps1
            gwp2 = gwpc2 + gwps2

        elif element == "Beam":
            l1 = float(beam_length_entry1.get())*unit_factor
            l2 = float(beam_length_entry2.get())*unit_factor

            b1 = float(beam_width_entry1.get())*unit_factor
            b2 = float(beam_width_entry2.get())*unit_factor

            h1 = float(beam_depth_entry1.get())*unit_factor
            h2 = float(beam_depth_entry2.get())*unit_factor

            rr1 = float(beam_ratio_entry1.get())
            rr2 = float(beam_ratio_entry2.get())

            vc1 = get_volume(l1,b1,h1)*(1-rr1/100)
            vc2 = get_volume(l2,b2,h2)*(1-rr2/100)
            vs1 = get_volume(l1,b1,h1)*rr1/100
            vs2 = get_volume(l2,b2,h2)*rr2/100

            gwp_per_m3_1 = float(beam_gwp_conc_entry1.get())
            gwp_per_m3_2 = float(beam_gwp_conc_entry2.get())
            gwp_per_mt = float(gwp_steel_entry.get())

            gwpc1 = vc1*gwp_per_m3_1
            gwpc2 = vc2*gwp_per_m3_2

            gwps1 = vs1*7.85*gwp_per_mt
            gwps2 = vs2*7.85*gwp_per_mt

            gwp1 = gwpc1 + gwps1
            gwp2 = gwpc2 + gwps2

        elif element == "Wall":
            l1 = float(wall_length_entry1.get())*unit_factor
            l2 = float(wall_length_entry2.get())*unit_factor

            b1 = float(wall_thick_entry1.get())*unit_factor
            b2 = float(wall_thick_entry2.get())*unit_factor

            h1 = float(wall_height_entry1.get())*unit_factor
            h2 = float(wall_height_entry2.get())*unit_factor

            rr1 = float(wall_ratio_entry1.get())
            rr2 = float(wall_ratio_entry2.get())

            vc1 = get_volume(l1,b1,h1)*(1-rr1/100)
            vc2 = get_volume(l2,b2,h2)*(1-rr2/100)
            vs1 = get_volume(l1,b1,h1)*rr1/100
            vs2 = get_volume(l2,b2,h2)*rr2/100

            gwp_per_m3_1 = float(wall_gwp_conc_entry1.get())
            gwp_per_m3_2 = float(wall_gwp_conc_entry2.get())
            gwp_per_mt = float(gwp_steel_entry.get())

            gwpc1 = vc1*gwp_per_m3_1
            gwpc2 = vc2*gwp_per_m3_2

            gwps1 = vs1*7.85*gwp_per_mt
            gwps2 = vs2*7.85*gwp_per_mt

            gwp1 = gwpc1 + gwps1
            gwp2 = gwpc2 + gwps2

        elif element == "Slab":
            l1 = float(slab_xlength_entry1.get())*unit_factor
            l2 = float(slab_xlength_entry2.get())*unit_factor

            b1 = float(slab_ylength_entry1.get())*unit_factor
            b2 = float(slab_ylength_entry2.get())*unit_factor

            h1 = float(slab_thick_entry1.get())*unit_factor
            h2 = float(slab_thick_entry2.get())*unit_factor

            rr1 = float(slab_ratio_entry1.get())
            rr2 = float(slab_ratio_entry2.get())

            vc1 = get_volume(l1,b1,h1)*(1-rr1/100)
            vc2 = get_volume(l2,b2,h2)*(1-rr2/100)
            vs1 = get_volume(l1,b1,h1)*rr1/100
            vs2 = get_volume(l2,b2,h2)*rr2/100

            gwp_per_m3_1 = float(slab_gwp_conc_entry1.get())
            gwp_per_m3_2 = float(slab_gwp_conc_entry2.get())
            gwp_per_mt = float(gwp_steel_entry.get())

            gwpc1 = vc1*gwp_per_m3_1
            gwpc2 = vc2*gwp_per_m3_2

            gwps1 = vs1*7.85*gwp_per_mt
            gwps2 = vs2*7.85*gwp_per_mt

            gwp1 = gwpc1 + gwps1
            gwp2 = gwpc2 + gwps2

        elif element == "Footing":
            l1 = float(footing_xlength_entry1.get())*unit_factor
            l2 = float(footing_xlength_entry2.get())*unit_factor

            b1 = float(footing_ylength_entry1.get())*unit_factor
            b2 = float(footing_ylength_entry2.get())*unit_factor

            h1 = float(footing_thick_entry1.get())*unit_factor
            h2 = float(footing_thick_entry2.get())*unit_factor

            rr1 = float(footing_ratio_entry1.get())
            rr2 = float(footing_ratio_entry2.get())

            vc1 = get_volume(l1,b1,h1)*(1-rr1/100)
            vc2 = get_volume(l2,b2,h2)*(1-rr2/100)
            vs1 = get_volume(l1,b1,h1)*rr1/100
            vs2 = get_volume(l2,b2,h2)*rr2/100

            gwp_per_m3_1 = float(footing_gwp_conc_entry1.get())
            gwp_per_m3_2 = float(footing_gwp_conc_entry2.get())
            gwp_per_mt = float(gwp_steel_entry.get())

            gwpc1 = vc1*gwp_per_m3_1
            gwpc2 = vc2*gwp_per_m3_2

            gwps1 = vs1*7.85*gwp_per_mt
            gwps2 = vs2*7.85*gwp_per_mt

            gwp1 = gwpc1 + gwps1
            gwp2 = gwpc2 + gwps2
        if units == "Imperial":
            vc1 = vc1*3.2808399**3
            vc2 = vc2*3.2808399**3
            vs1 = vs1*3.2808399**3
            vs2 = vs2*3.2808399**3

            if gwp1>gwp2:
                output_box["text"]=f"Option 1: GWP = {round(gwp1)}KgCO2e; Volume of concrete = {round(vc1,2)}ft³; Volume of steel = {round(vs1,2)}ft³\nOption 2: GWP = {round(gwp2)}KgCO2e; Volume of concrete = {round(vc2,2)}ft³; Volume of steel = {round(vs2,2)}ft³\n\nOption 2 is better than Option 1"
            elif gwp1<gwp2:
                output_box["text"]=f"Option 1: GWP = {round(gwp1)}KgCO2e; Volume of concrete = {round(vc1,2)}ft³; Volume of steel = {round(vs1,2)}ft³\nOption 2: GWP = {round(gwp2)}KgCO2e; Volume of concrete = {round(vc2,2)}ft³; Volume of steel = {round(vs2,2)}ft³\n\nOption 1 is better than Option 2"
            else:
                output_box["text"]=f"Option 1: GWP = {round(gwp1)}KgCO2e; Volume of concrete = {round(vc1,2)}ft³; Volume of steel = {round(vs1,2)}ft³\nOption 2: GWP = {round(gwp2)}KgCO2e; Volume of concrete = {round(vc2,2)}ft³; Volume of steel = {round(vs2,2)}ft³\n\nBoth have equal emissions"
            i = random.randint(0, 39)
            statement_box["text"]=statements[i]
        else:
            if gwp1>gwp2:
                output_box["text"]=f"Option 1: GWP = {round(gwp1)}KgCO2e; Volume of concrete = {round(vc1,2)}m³; Volume of steel = {round(vs1,2)}m³\nOption 2: GWP = {round(gwp2)}KgCO2e; Volume of concrete = {round(vc2,2)}m³; Volume of steel = {round(vs2,2)}m³\n\nOption 2 is better than Option 1"
            elif gwp1<gwp2:
                output_box["text"]=f"Option 1: GWP = {round(gwp1)}KgCO2e; Volume of concrete = {round(vc1,2)}m³; Volume of steel = {round(vs1,2)}m³\nOption 2: GWP = {round(gwp2)}KgCO2e; Volume of concrete = {round(vc2,2)}m³; Volume of steel = {round(vs2,2)}m³\n\nOption 1 is better than Option 2"
            else:
                output_box["text"]=f"Option 1: GWP = {round(gwp1)}KgCO2e; Volume of concrete = {round(vc1,2)}m³; Volume of steel = {round(vs1,2)}m³\nOption 2: GWP = {round(gwp2)}KgCO2e; Volume of concrete = {round(vc2,2)}m³; Volume of steel = {round(vs2,2)}m³\n\nBoth have equal emissions"
            i = random.randint(0, 39)
            statement_box["text"]=statements[i]
    except:
        print("Check inputs")
        output_box["text"]=output_box["text"]=f"Option 1: GWP = ; Volume of concrete = ; Volume of steel = \nOption 2: GWP = ; Volume of concrete = ; Volume of steel = \n\nCheck Inputs"
        i = random.randint(0, 39)
        statement_box["text"]=statements[i]

window = tk.Tk()
window.title("GWP Calculator")
#window.geometry("600x600")

#Basic inputs
frame= tk.Frame(window)
frame.grid(row=0,column=0)

heading = tk.Label(frame, text="GWP Calculator", font=("Arial", 15, "bold underline"))
heading.grid(row=0, column =1, columnspan=3, sticky ="EW",padx=5,pady=5)

lable = tk.Label(frame, text="                ") 
lable.grid(row=1, column=0)

element_label = tk.Label(frame, text="Element :")
element_label.grid(row=1, column =1, sticky ="E",padx=5,pady=5)

element_combo = ttk.Combobox(frame, state="readonly", values=["Column","Beam","Wall","Slab","Footing"])
element_combo.grid(row=1, column =2, sticky ="W",padx=5,pady=5)
element_combo.current(0)
element_combo.bind("<<ComboboxSelected>>", element_changed)

units_label = tk.Label(frame, text="Units :")
units_label.grid(row=2, column =1, sticky ="E",padx=5,pady=5)

units_combo = ttk.Combobox(frame, state="readonly", values=["Imperial","Metric"])
units_combo.grid(row=2, column =2, sticky ="W",padx=5,pady=5)
units_combo.current(0)
units_combo.bind("<<ComboboxSelected>>", units_changed)

region_label = tk.Label(frame, text="Region :")
region_label.grid(row=3, column =1, sticky ="E",padx=5,pady=5)

region_combo = ttk.Combobox(frame, state="readonly", values=["CANADA","UNITED STATES"])
region_combo.grid(row=3, column =2, sticky ="W",padx=5,pady=5)
region_combo.current(0)
region_combo.bind("<<ComboboxSelected>>",region_changed)


location_label = tk.Label(frame, text="Location :")
location_label.grid(row=4, column =1, sticky ="E",padx=5,pady=5)

location_combo = ttk.Combobox(frame, state="readonly", values=[""])
location_combo.grid(row=4, column =2, sticky ="W",padx=5,pady=5)
location_combo.current(0)
location_combo.bind("<<ComboboxSelected>>",location_changed)

'''
gwp_conc_label = tk.Label(frame, text="GWP Value for Concrete :")
gwp_conc_label.grid(row=5, column =1, sticky ="E",padx=5,pady=5)

gwp_conc_entry = ttk.Entry(frame, width=5)
gwp_conc_entry.grid(row=5, column =2, sticky ="EW",padx=5,pady=5)
gwp_conc_entry.insert(0,258)

gwp_unit_label = tk.Label(frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=5, column =3, sticky ="W",padx=5,pady=5)
'''

gwp_steel_label = tk.Label(frame, text="GWP Value for Steel :")
gwp_steel_label.grid(row=6, column =1, sticky ="E",padx=5,pady=5)

gwp_steel_entry = ttk.Entry(frame, width=5)
gwp_steel_entry.grid(row=6, column =2, sticky ="EW",padx=5,pady=5)
gwp_steel_entry.insert(0,854)

gwp_unit_label = tk.Label(frame, text="KgCO2e/metric ton")
gwp_unit_label.grid(row=6, column =3, sticky ="W",padx=5,pady=5)

result_frame = tk.Frame(window)
result_frame.grid(row=2,column=0,sticky='NSEW', padx=5, pady=5)
string=" "
empty_label = tk.Label(result_frame, text= string*50)
empty_label.grid(row=0,column=0)
calculate_button = tk.Button(result_frame,text = " Calculate ", font=("Arial", 12, "roman"), command = calculate_gwp, width=10)
calculate_button.grid(row=0, column =1, sticky ="NSEW",padx=10,pady=10)
output_box = tk.Label(result_frame, width=70, height=4,font=("Arial", 10, "bold"), background="white",anchor="w", justify="left",borderwidth=2, relief="solid")
output_box.grid(row=1,column=0,columnspan=6,sticky ="W", padx=10,pady=10)
statement_box = tk.Label(result_frame, width=70, height=1,font=("Arial", 10, "bold"), fg="green",anchor="center", justify="center")
statement_box.grid(row=2,column=0,columnspan=6,sticky ="W", padx=10)

# Element specific input
############################################################################################################################# Column Frame
column_frame = tk.Frame(window)
column_frame.grid(row=1,column=0,sticky='NSEW', padx=5, pady=5)

option1_label = tk.Label(column_frame, text="Option 1", font=("Arial",10,"bold underline"))
option1_label.grid(row=0,column=1,columnspan=1,sticky="EW",padx=5,pady=5)
option2_label = tk.Label(column_frame, text="Option 2", font=("Arial",10,"bold underline"))
option2_label.grid(row=0,column=4,columnspan=1,sticky="EW",padx=5,pady=5)

# Concrete grade
col_label = tk.Label(column_frame, text="Concrete grade :")
col_label.grid(row=1,column=0,sticky="E",padx=5,pady=5)

col_conc_combo1 = ttk.Combobox(column_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
col_conc_combo1.grid(row=1, column =1, sticky ="W",padx=5,pady=5)
col_conc_combo1.current(0)
col_conc_combo1.bind("<<ComboboxSelected>>", grade_changed)
col_unit1 = tk.Label(column_frame,text="Mpa")
col_unit1.grid(row=1, column =2, sticky ="W",padx=5,pady=5)

col_label = tk.Label(column_frame, text="    ")
col_label.grid(row=1,column=3,sticky="E",padx=5,pady=5)
col_conc_combo2 = ttk.Combobox(column_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
col_conc_combo2.grid(row=1, column =4, sticky ="W",padx=5,pady=5)
col_conc_combo2.current(0)
col_conc_combo2.bind("<<ComboboxSelected>>", grade_changed)
col_unit2 = tk.Label(column_frame,text="Mpa")
col_unit2.grid(row=1, column =5, sticky ="W",padx=5,pady=5)

#Col_GWP
gwp_conc_label = tk.Label(column_frame, text="GWP Value:")
gwp_conc_label.grid(row=2,column=0,sticky="E",padx=5,pady=5)
col_gwp_conc_entry1 = ttk.Entry(column_frame)
col_gwp_conc_entry1.grid(row=2, column =1, sticky ="EW",padx=5,pady=5)
col_gwp_conc_entry1.insert(0,"")
gwp_unit_label = tk.Label(column_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =2, sticky ="W",padx=5,pady=5)

gwp_conc_label = tk.Label(column_frame, text="    ")
gwp_conc_label.grid(row=2,column=3,sticky="E",padx=5,pady=5)
col_gwp_conc_entry2 = ttk.Entry(column_frame)
col_gwp_conc_entry2.grid(row=2, column =4, sticky ="EW",padx=5,pady=5)
col_gwp_conc_entry2.insert(0,"")
gwp_unit_label = tk.Label(column_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =5, sticky ="W",padx=5,pady=5)

# height
col_label = tk.Label(column_frame, text="Height :")
col_label.grid(row=3,column=0,sticky="E",padx=5,pady=5)

col_height_entry1 = ttk.Entry(column_frame)
col_height_entry1.grid(row=3, column =1, sticky ="EW",padx=5,pady=5)
col_unit3 = tk.Label(column_frame,text="ft")
col_unit3.grid(row=3, column =2, sticky ="W",padx=5,pady=5)

col_label = tk.Label(column_frame, text="    ")
col_label.grid(row=3,column=3,sticky="E",padx=5,pady=5)
col_height_entry2 = ttk.Entry(column_frame)
col_height_entry2.grid(row=3, column =4, sticky ="EW",padx=5,pady=5)
col_unit4 = tk.Label(column_frame,text="ft")
col_unit4.grid(row=3, column =5, sticky ="W",padx=5,pady=5)

# width
col_label = tk.Label(column_frame, text="Width :")
col_label.grid(row=4,column=0,sticky="E",padx=5,pady=5)

col_width_entry1 = ttk.Entry(column_frame)
col_width_entry1.grid(row=4, column =1, sticky ="EW",padx=5,pady=5)
col_unit5 = tk.Label(column_frame,text="ft")
col_unit5.grid(row=4, column =2, sticky ="W",padx=5,pady=5)

col_label = tk.Label(column_frame, text="    ")
col_label.grid(row=4,column=3,sticky="E",padx=5,pady=5)
col_width_entry2 = ttk.Entry(column_frame)
col_width_entry2.grid(row=4, column =4, sticky ="EW",padx=5,pady=5)
col_unit6 = tk.Label(column_frame,text="ft")
col_unit6.grid(row=4, column =5, sticky ="W",padx=5,pady=5)

# depth
col_label = tk.Label(column_frame, text="Depth :")
col_label.grid(row=5,column=0,sticky="E",padx=5,pady=5)

col_depth_entry1 = ttk.Entry(column_frame)
col_depth_entry1.grid(row=5, column =1, sticky ="EW",padx=5,pady=5)
col_unit7 = tk.Label(column_frame,text="ft")
col_unit7.grid(row=5, column =2, sticky ="W",padx=5,pady=5)

col_label = tk.Label(column_frame, text="    ")
col_label.grid(row=5,column=3,sticky="E",padx=5,pady=5)
col_depth_entry2 = ttk.Entry(column_frame)
col_depth_entry2.grid(row=5, column =4, sticky ="EW",padx=5,pady=5)
col_unit8 = tk.Label(column_frame,text="ft")
col_unit8.grid(row=5, column =5, sticky ="W",padx=5,pady=5)

# rebar ratio
ratio_label = tk.Label(column_frame, text="Rebar ratio :")
ratio_label.grid(row=6, column=0,sticky="E",padx=5,pady=5)

col_ratio_entry1 = ttk.Entry(column_frame)
col_ratio_entry1.grid(row=6, column =1, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(column_frame,text="%")
ratio_unit.grid(row=6, column =2, sticky ="W",padx=5,pady=5)

ratio_label = tk.Label(column_frame, text="    ")
ratio_label.grid(row=6,column=3,sticky="E",padx=5,pady=5)
col_ratio_entry2 = ttk.Entry(column_frame)
col_ratio_entry2.grid(row=6, column =4, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(column_frame,text="%")
ratio_unit.grid(row=6, column =5, sticky ="W",padx=5,pady=5)

############################################################################################################################# Beam Frame
# Beam Frame
beam_frame = tk.Frame(window)
#beam_frame.grid(row=2,column=0,sticky='NSEW', padx=5, pady=5)

option1_label = tk.Label(beam_frame, text="Option 1", font=("Arial",10,"bold underline"))
option1_label.grid(row=0,column=1,columnspan=1,sticky="EW",padx=5,pady=5)
option2_label = tk.Label(beam_frame, text="Option 2", font=("Arial",10,"bold underline"))
option2_label.grid(row=0,column=4,columnspan=1,sticky="EW",padx=5,pady=5)

# Concrete grade
beam_label = tk.Label(beam_frame, text="Concrete grade :")
beam_label.grid(row=1,column=0,sticky="E",padx=5,pady=5)

beam_conc_combo1 = ttk.Combobox(beam_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
beam_conc_combo1.grid(row=1, column =1, sticky ="W",padx=5,pady=5)
beam_conc_combo1.current(0)
beam_conc_combo1.bind("<<ComboboxSelected>>", grade_changed)
beam_unit1 = tk.Label(beam_frame,text="Mpa")
beam_unit1.grid(row=1, column =2, sticky ="W",padx=5,pady=5)

beam_label = tk.Label(beam_frame, text="    ")
beam_label.grid(row=1,column=3,sticky="E",padx=5,pady=5)
beam_conc_combo2 = ttk.Combobox(beam_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
beam_conc_combo2.grid(row=1, column =4, sticky ="W",padx=5,pady=5)
beam_conc_combo2.current(0)
beam_conc_combo2.bind("<<ComboboxSelected>>", grade_changed)
beam_unit2 = tk.Label(beam_frame,text="Mpa")
beam_unit2.grid(row=1, column =5, sticky ="W",padx=5,pady=5)

#beam_GWP
gwp_conc_label = tk.Label(beam_frame, text="GWP Value:")
gwp_conc_label.grid(row=2,column=0,sticky="E",padx=5,pady=5)
beam_gwp_conc_entry1 = ttk.Entry(beam_frame)
beam_gwp_conc_entry1.grid(row=2, column =1, sticky ="EW",padx=5,pady=5)
beam_gwp_conc_entry1.insert(0,"")
gwp_unit_label = tk.Label(beam_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =2, sticky ="W",padx=5,pady=5)

gwp_conc_label = tk.Label(beam_frame, text="    ")
gwp_conc_label.grid(row=2,column=3,sticky="E",padx=5,pady=5)
beam_gwp_conc_entry2 = ttk.Entry(beam_frame)
beam_gwp_conc_entry2.grid(row=2, column =4, sticky ="EW",padx=5,pady=5)
beam_gwp_conc_entry2.insert(0,"")
gwp_unit_label = tk.Label(beam_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =5, sticky ="W",padx=5,pady=5)

# length
beam_label = tk.Label(beam_frame, text="Length :")
beam_label.grid(row=3,column=0,sticky="E",padx=5,pady=5)

beam_length_entry1 = ttk.Entry(beam_frame)
beam_length_entry1.grid(row=3, column =1, sticky ="EW",padx=5,pady=5)
beam_unit3 = tk.Label(beam_frame,text="ft")
beam_unit3.grid(row=3, column =2, sticky ="W",padx=5,pady=5)

beam_label = tk.Label(beam_frame, text="    ")
beam_label.grid(row=3,column=3,sticky="E",padx=5,pady=5)
beam_length_entry2 = ttk.Entry(beam_frame)
beam_length_entry2.grid(row=3, column =4, sticky ="EW",padx=5,pady=5)
beam_unit4 = tk.Label(beam_frame,text="ft")
beam_unit4.grid(row=3, column =5, sticky ="W",padx=5,pady=5)

# width
beam_label = tk.Label(beam_frame, text="Width :")
beam_label.grid(row=4,column=0,sticky="E",padx=5,pady=5)

beam_width_entry1 = ttk.Entry(beam_frame)
beam_width_entry1.grid(row=4, column =1, sticky ="EW",padx=5,pady=5)
beam_unit5 = tk.Label(beam_frame,text="ft")
beam_unit5.grid(row=4, column =2, sticky ="W",padx=5,pady=5)

beam_label = tk.Label(beam_frame, text="    ")
beam_label.grid(row=4,column=3,sticky="E",padx=5,pady=5)
beam_width_entry2 = ttk.Entry(beam_frame)
beam_width_entry2.grid(row=4, column =4, sticky ="EW",padx=5,pady=5)
beam_unit6 = tk.Label(beam_frame,text="ft")
beam_unit6.grid(row=4, column =5, sticky ="W",padx=5,pady=5)

# depth
beam_label = tk.Label(beam_frame, text="Depth :")
beam_label.grid(row=5,column=0,sticky="E",padx=5,pady=5)

beam_depth_entry1 = ttk.Entry(beam_frame)
beam_depth_entry1.grid(row=5, column =1, sticky ="EW",padx=5,pady=5)
beam_unit7 = tk.Label(beam_frame,text="ft")
beam_unit7.grid(row=5, column =2, sticky ="W",padx=5,pady=5)

beam_label = tk.Label(beam_frame, text="    ")
beam_label.grid(row=5,column=3,sticky="E",padx=5,pady=5)
beam_depth_entry2 = ttk.Entry(beam_frame)
beam_depth_entry2.grid(row=5, column =4, sticky ="EW",padx=5,pady=5)
beam_unit8 = tk.Label(beam_frame,text="ft")
beam_unit8.grid(row=5, column =5, sticky ="W",padx=5,pady=5)

# rebar ratio
ratio_label = tk.Label(beam_frame, text="Rebar ratio :")
ratio_label.grid(row=6,column=0,sticky="E",padx=5,pady=5)

beam_ratio_entry1 = ttk.Entry(beam_frame)
beam_ratio_entry1.grid(row=6, column =1, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(beam_frame,text="%")
ratio_unit.grid(row=6, column =2, sticky ="W",padx=5,pady=5)

ratio_label = tk.Label(beam_frame, text="    ")
ratio_label.grid(row=6,column=3,sticky="E",padx=5,pady=5)
beam_ratio_entry2 = ttk.Entry(beam_frame)
beam_ratio_entry2.grid(row=6, column =4, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(beam_frame,text="%")
ratio_unit.grid(row=6, column =5, sticky ="W",padx=5,pady=5)


############################################################################################################################# Wall Frame
# wall Frame
wall_frame = tk.Frame(window)
#wall_frame.grid(row=3,column=0,sticky='NSEW', padx=5, pady=5)

option1_label = tk.Label(wall_frame, text="Option 1", font=("Arial",10,"bold underline"))
option1_label.grid(row=0,column=1,columnspan=1,sticky="EW",padx=5,pady=5)
option2_label = tk.Label(wall_frame, text="Option 2", font=("Arial",10,"bold underline"))
option2_label.grid(row=0,column=4,columnspan=1,sticky="EW",padx=5,pady=5)

# Concrete grade
wall_label = tk.Label(wall_frame, text="Concrete grade :")
wall_label.grid(row=1,column=0,sticky="E",padx=5,pady=5)

wall_conc_combo1 = ttk.Combobox(wall_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
wall_conc_combo1.grid(row=1, column =1, sticky ="W",padx=5,pady=5)
wall_conc_combo1.current(0)
wall_conc_combo1.bind("<<ComboboxSelected>>", grade_changed)
wall_unit1 = tk.Label(wall_frame,text="Mpa")
wall_unit1.grid(row=1, column =2, sticky ="W",padx=5,pady=5)

wall_label = tk.Label(wall_frame, text="    ")
wall_label.grid(row=1,column=3,sticky="E",padx=5,pady=5)
wall_conc_combo2 = ttk.Combobox(wall_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
wall_conc_combo2.grid(row=1, column =4, sticky ="W",padx=5,pady=5)
wall_conc_combo2.current(0)
wall_conc_combo2.bind("<<ComboboxSelected>>", grade_changed)
wall_unit2 = tk.Label(wall_frame,text="Mpa")
wall_unit2.grid(row=1, column =5, sticky ="W",padx=5,pady=5)

#wall_GWP
gwp_conc_label = tk.Label(wall_frame, text="GWP Value:")
gwp_conc_label.grid(row=2,column=0,sticky="E",padx=5,pady=5)
wall_gwp_conc_entry1 = ttk.Entry(wall_frame)
wall_gwp_conc_entry1.grid(row=2, column =1, sticky ="EW",padx=5,pady=5)
wall_gwp_conc_entry1.insert(0,"")
gwp_unit_label = tk.Label(wall_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =2, sticky ="W",padx=5,pady=5)

gwp_conc_label = tk.Label(wall_frame, text="    ")
gwp_conc_label.grid(row=2,column=3,sticky="E",padx=5,pady=5)
wall_gwp_conc_entry2 = ttk.Entry(wall_frame)
wall_gwp_conc_entry2.grid(row=2, column =4, sticky ="EW",padx=5,pady=5)
wall_gwp_conc_entry2.insert(0,"")
gwp_unit_label = tk.Label(wall_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =5, sticky ="W",padx=5,pady=5)

# length
wall_label = tk.Label(wall_frame, text="Length :")
wall_label.grid(row=3,column=0,sticky="E",padx=5,pady=5)

wall_length_entry1 = ttk.Entry(wall_frame)
wall_length_entry1.grid(row=3, column =1, sticky ="EW",padx=5,pady=5)
wall_unit3 = tk.Label(wall_frame,text="ft")
wall_unit3.grid(row=3, column =2, sticky ="W",padx=5,pady=5)

wall_label = tk.Label(wall_frame, text="    ")
wall_label.grid(row=3,column=3,sticky="E",padx=5,pady=5)
wall_length_entry2 = ttk.Entry(wall_frame)
wall_length_entry2.grid(row=3, column =4, sticky ="EW",padx=5,pady=5)
wall_unit4 = tk.Label(wall_frame,text="ft")
wall_unit4.grid(row=3, column =5, sticky ="W",padx=5,pady=5)

# height
wall_label = tk.Label(wall_frame, text="Height :")
wall_label.grid(row=4,column=0,sticky="E",padx=5,pady=5)

wall_height_entry1 = ttk.Entry(wall_frame)
wall_height_entry1.grid(row=4, column =1, sticky ="EW",padx=5,pady=5)
wall_unit5 = tk.Label(wall_frame,text="ft")
wall_unit5.grid(row=4, column =2, sticky ="W",padx=5,pady=5)

wall_label = tk.Label(wall_frame, text="    ")
wall_label.grid(row=4,column=3,sticky="E",padx=5,pady=5)
wall_height_entry2 = ttk.Entry(wall_frame)
wall_height_entry2.grid(row=4, column =4, sticky ="EW",padx=5,pady=5)
wall_unit6 = tk.Label(wall_frame,text="ft")
wall_unit6.grid(row=4, column =5, sticky ="W",padx=5,pady=5)

# thick
wall_label = tk.Label(wall_frame, text="Thickness :")
wall_label.grid(row=5,column=0,sticky="E",padx=5,pady=5)

wall_thick_entry1 = ttk.Entry(wall_frame)
wall_thick_entry1.grid(row=5, column =1, sticky ="EW",padx=5,pady=5)
wall_unit7 = tk.Label(wall_frame,text="ft")
wall_unit7.grid(row=5, column =2, sticky ="W",padx=5,pady=5)

wall_label = tk.Label(wall_frame, text="    ")
wall_label.grid(row=5,column=3,sticky="E",padx=5,pady=5)
wall_thick_entry2 = ttk.Entry(wall_frame)
wall_thick_entry2.grid(row=5, column =4, sticky ="EW",padx=5,pady=5)
wall_unit8 = tk.Label(wall_frame,text="ft")
wall_unit8.grid(row=5, column =5, sticky ="W",padx=5,pady=5)

# rebar ratio
ratio_label = tk.Label(wall_frame, text="Rebar ratio :")
ratio_label.grid(row=6,column=0,sticky="E",padx=5,pady=5)

wall_ratio_entry1 = ttk.Entry(wall_frame)
wall_ratio_entry1.grid(row=6, column =1, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(wall_frame,text="%")
ratio_unit.grid(row=6, column =2, sticky ="W",padx=5,pady=5)

ratio_label = tk.Label(wall_frame, text="    ")
ratio_label.grid(row=6,column=3,sticky="E",padx=5,pady=5)
wall_ratio_entry2 = ttk.Entry(wall_frame)
wall_ratio_entry2.grid(row=6, column =4, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(wall_frame,text="%")
ratio_unit.grid(row=6, column =5, sticky ="W",padx=5,pady=5)

############################################################################################################################# Slab Frame
# slab Frame
slab_frame = tk.Frame(window)
#slab_frame.grid(row=1,column=1,sticky='NSEW', padx=5, pady=5)

option1_label = tk.Label(slab_frame, text="Option 1", font=("Arial",10,"bold underline"))
option1_label.grid(row=0,column=1,columnspan=1,sticky="EW",padx=5,pady=5)
option2_label = tk.Label(slab_frame, text="Option 2", font=("Arial",10,"bold underline"))
option2_label.grid(row=0,column=4,columnspan=1,sticky="EW",padx=5,pady=5)

# Concrete grade
slab_label = tk.Label(slab_frame, text="Concrete grade :")
slab_label.grid(row=1,column=0,sticky="E",padx=5,pady=5)

slab_conc_combo1 = ttk.Combobox(slab_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
slab_conc_combo1.grid(row=1, column =1, sticky ="W",padx=5,pady=5)
slab_conc_combo1.current(0)
slab_conc_combo1.bind("<<ComboboxSelected>>", grade_changed)
slab_unit1 = tk.Label(slab_frame,text="Mpa")
slab_unit1.grid(row=1, column =2, sticky ="W",padx=5,pady=5)

slab_label = tk.Label(slab_frame, text="    ")
slab_label.grid(row=1,column=3,sticky="E",padx=5,pady=5)
slab_conc_combo2 = ttk.Combobox(slab_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
slab_conc_combo2.grid(row=1, column =4, sticky ="W",padx=5,pady=5)
slab_conc_combo2.current(0)
slab_conc_combo2.bind("<<ComboboxSelected>>", grade_changed)
slab_unit2 = tk.Label(slab_frame,text="Mpa")
slab_unit2.grid(row=1, column =5, sticky ="W",padx=5,pady=5)

#Slab_GWP
gwp_conc_label = tk.Label(slab_frame, text="GWP Value:")
gwp_conc_label.grid(row=2,column=0,sticky="E",padx=5,pady=5)
slab_gwp_conc_entry1 = ttk.Entry(slab_frame)
slab_gwp_conc_entry1.grid(row=2, column =1, sticky ="EW",padx=5,pady=5)
slab_gwp_conc_entry1.insert(0,"")
gwp_unit_label = tk.Label(slab_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =2, sticky ="W",padx=5,pady=5)

gwp_conc_label = tk.Label(slab_frame, text="    ")
gwp_conc_label.grid(row=2,column=3,sticky="E",padx=5,pady=5)
slab_gwp_conc_entry2 = ttk.Entry(slab_frame)
slab_gwp_conc_entry2.grid(row=2, column =4, sticky ="EW",padx=5,pady=5)
slab_gwp_conc_entry2.insert(0,"")
gwp_unit_label = tk.Label(slab_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =5, sticky ="W",padx=5,pady=5)

# xlength
slab_label = tk.Label(slab_frame, text="Length-X :")
slab_label.grid(row=3,column=0,sticky="E",padx=5,pady=5)

slab_xlength_entry1 = ttk.Entry(slab_frame)
slab_xlength_entry1.grid(row=3, column =1, sticky ="EW",padx=5,pady=5)
slab_unit3 = tk.Label(slab_frame,text="ft")
slab_unit3.grid(row=3, column =2, sticky ="W",padx=5,pady=5)

slab_label = tk.Label(slab_frame, text="    ")
slab_label.grid(row=3,column=3,sticky="E",padx=5,pady=5)
slab_xlength_entry2 = ttk.Entry(slab_frame)
slab_xlength_entry2.grid(row=3, column =4, sticky ="EW",padx=5,pady=5)
slab_unit4 = tk.Label(slab_frame,text="ft")
slab_unit4.grid(row=3, column =5, sticky ="W",padx=5,pady=5)

# ylength
slab_label = tk.Label(slab_frame, text="Length-Y :")
slab_label.grid(row=4,column=0,sticky="E",padx=5,pady=5)

slab_ylength_entry1 = ttk.Entry(slab_frame)
slab_ylength_entry1.grid(row=4, column =1, sticky ="EW",padx=5,pady=5)
slab_unit5 = tk.Label(slab_frame,text="ft")
slab_unit5.grid(row=4, column =2, sticky ="W",padx=5,pady=5)

slab_label = tk.Label(slab_frame, text="    ")
slab_label.grid(row=4,column=3,sticky="E",padx=5,pady=5)
slab_ylength_entry2 = ttk.Entry(slab_frame)
slab_ylength_entry2.grid(row=4, column =4, sticky ="EW",padx=5,pady=5)
slab_unit6 = tk.Label(slab_frame,text="ft")
slab_unit6.grid(row=4, column =5, sticky ="W",padx=5,pady=5)

# thick
slab_label = tk.Label(slab_frame, text="Thickness :")
slab_label.grid(row=5,column=0,sticky="E",padx=5,pady=5)

slab_thick_entry1 = ttk.Entry(slab_frame)
slab_thick_entry1.grid(row=5, column =1, sticky ="EW",padx=5,pady=5)
slab_unit7 = tk.Label(slab_frame,text="ft")
slab_unit7.grid(row=5, column =2, sticky ="W",padx=5,pady=5)

slab_label = tk.Label(slab_frame, text="    ")
slab_label.grid(row=5,column=3,sticky="E",padx=5,pady=5)
slab_thick_entry2 = ttk.Entry(slab_frame)
slab_thick_entry2.grid(row=5, column =4, sticky ="EW",padx=5,pady=5)
slab_unit8 = tk.Label(slab_frame,text="ft")
slab_unit8.grid(row=5, column =5, sticky ="W",padx=5,pady=5)

# rebar ratio
ratio_label = tk.Label(slab_frame, text="Rebar ratio :")
ratio_label.grid(row=6,column=0,sticky="E",padx=5,pady=5)

slab_ratio_entry1 = ttk.Entry(slab_frame)
slab_ratio_entry1.grid(row=6, column =1, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(slab_frame,text="%")
ratio_unit.grid(row=6, column =2, sticky ="W",padx=5,pady=5)

ratio_label = tk.Label(slab_frame, text="    ")
ratio_label.grid(row=6,column=3,sticky="E",padx=5,pady=5)
slab_ratio_entry2 = ttk.Entry(slab_frame)
slab_ratio_entry2.grid(row=6, column =4, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(slab_frame,text="%")
ratio_unit.grid(row=6, column =5, sticky ="W",padx=5,pady=5)


############################################################################################################################# Footing Frame
# footing Frame
footing_frame = tk.Frame(window)
#footing_frame.grid(row=2,column=1,sticky='NSEW', padx=5, pady=5)

option1_label = tk.Label(footing_frame, text="Option 1", font=("Arial",10,"bold underline"))
option1_label.grid(row=0,column=1,columnspan=1,sticky="EW",padx=5,pady=5)
option2_label = tk.Label(footing_frame, text="Option 2", font=("Arial",10,"bold underline"))
option2_label.grid(row=0,column=4,columnspan=1,sticky="EW",padx=5,pady=5)

# Concrete grade
footing_label = tk.Label(footing_frame, text="Concrete grade :")
footing_label.grid(row=1,column=0,sticky="E",padx=5,pady=5)

footing_conc_combo1 = ttk.Combobox(footing_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
footing_conc_combo1.grid(row=1, column =1, sticky ="W",padx=5,pady=5)
footing_conc_combo1.current(0)
footing_conc_combo1.bind("<<ComboboxSelected>>", grade_changed)
footing_unit1 = tk.Label(footing_frame,text="Mpa")
footing_unit1.grid(row=1, column =2, sticky ="W",padx=5,pady=5)

footing_label = tk.Label(footing_frame, text="    ")
footing_label.grid(row=1,column=3,sticky="E",padx=5,pady=5)
footing_conc_combo2 = ttk.Combobox(footing_frame, state="readonly", values=list(fc for fc in range(20,61,5)))
footing_conc_combo2.grid(row=1, column =4, sticky ="W",padx=5,pady=5)
footing_conc_combo2.current(0)
footing_conc_combo2.bind("<<ComboboxSelected>>", grade_changed)
footing_unit2 = tk.Label(footing_frame,text="Mpa")
footing_unit2.grid(row=1, column =5, sticky ="W",padx=5,pady=5)

#footing_GWP
gwp_conc_label = tk.Label(footing_frame, text="GWP Value:")
gwp_conc_label.grid(row=2,column=0,sticky="E",padx=5,pady=5)
footing_gwp_conc_entry1 = ttk.Entry(footing_frame)
footing_gwp_conc_entry1.grid(row=2, column =1, sticky ="EW",padx=5,pady=5)
footing_gwp_conc_entry1.insert(0,"")
gwp_unit_label = tk.Label(footing_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =2, sticky ="W",padx=5,pady=5)

gwp_conc_label = tk.Label(footing_frame, text="    ")
gwp_conc_label.grid(row=2,column=3,sticky="E",padx=5,pady=5)
footing_gwp_conc_entry2 = ttk.Entry(footing_frame)
footing_gwp_conc_entry2.grid(row=2, column =4, sticky ="EW",padx=5,pady=5)
footing_gwp_conc_entry2.insert(0,"")
gwp_unit_label = tk.Label(footing_frame, text="KgCO2e/m³")
gwp_unit_label.grid(row=2, column =5, sticky ="W",padx=5,pady=5)

# xlength
footing_label = tk.Label(footing_frame, text="Length-X :")
footing_label.grid(row=3,column=0,sticky="E",padx=5,pady=5)

footing_xlength_entry1 = ttk.Entry(footing_frame)
footing_xlength_entry1.grid(row=3, column =1, sticky ="EW",padx=5,pady=5)
footing_unit3 = tk.Label(footing_frame,text="ft")
footing_unit3.grid(row=3, column =2, sticky ="W",padx=5,pady=5)

footing_label = tk.Label(footing_frame, text="    ")
footing_label.grid(row=3,column=3,sticky="E",padx=5,pady=5)
footing_xlength_entry2 = ttk.Entry(footing_frame)
footing_xlength_entry2.grid(row=3, column =4, sticky ="EW",padx=5,pady=5)
footing_unit4 = tk.Label(footing_frame,text="ft")
footing_unit4.grid(row=3, column =5, sticky ="W",padx=5,pady=5)

# ylength
footing_label = tk.Label(footing_frame, text="Length-Y :")
footing_label.grid(row=4,column=0,sticky="E",padx=5,pady=5)

footing_ylength_entry1 = ttk.Entry(footing_frame)
footing_ylength_entry1.grid(row=4, column =1, sticky ="EW",padx=5,pady=5)
footing_unit5 = tk.Label(footing_frame,text="ft")
footing_unit5.grid(row=4, column =2, sticky ="W",padx=5,pady=5)

footing_label = tk.Label(footing_frame, text="    ")
footing_label.grid(row=4,column=3,sticky="E",padx=5,pady=5)
footing_ylength_entry2 = ttk.Entry(footing_frame)
footing_ylength_entry2.grid(row=4, column =4, sticky ="EW",padx=5,pady=5)
footing_unit6 = tk.Label(footing_frame,text="ft")
footing_unit6.grid(row=4, column =5, sticky ="W",padx=5,pady=5)

# thick
footing_label = tk.Label(footing_frame, text="Thickness :")
footing_label.grid(row=5,column=0,sticky="E",padx=5,pady=5)

footing_thick_entry1 = ttk.Entry(footing_frame)
footing_thick_entry1.grid(row=5, column =1, sticky ="EW",padx=5,pady=5)
footing_unit7 = tk.Label(footing_frame,text="ft")
footing_unit7.grid(row=5, column =2, sticky ="W",padx=5,pady=5)

footing_label = tk.Label(footing_frame, text="    ")
footing_label.grid(row=5,column=3,sticky="E",padx=5,pady=5)
footing_thick_entry2 = ttk.Entry(footing_frame)
footing_thick_entry2.grid(row=5, column =4, sticky ="EW",padx=5,pady=5)
footing_unit8 = tk.Label(footing_frame,text="ft")
footing_unit8.grid(row=5, column =5, sticky ="W",padx=5,pady=5)

# rebar ratio
ratio_label = tk.Label(footing_frame, text="Rebar ratio :")
ratio_label.grid(row=6,column=0,sticky="E",padx=5,pady=5)

footing_ratio_entry1 = ttk.Entry(footing_frame)
footing_ratio_entry1.grid(row=6, column =1, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(footing_frame,text="%")
ratio_unit.grid(row=6, column =2, sticky ="W",padx=5,pady=5)

ratio_label = tk.Label(footing_frame, text="    ")
ratio_label.grid(row=6,column=3,sticky="E",padx=5,pady=5)
footing_ratio_entry2 = ttk.Entry(footing_frame)
footing_ratio_entry2.grid(row=6, column =4, sticky ="EW",padx=5,pady=5)
ratio_unit = tk.Label(footing_frame,text="%")
ratio_unit.grid(row=6, column =5, sticky ="W",padx=5,pady=5)


region_changed(0)

frame.mainloop()