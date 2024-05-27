import xlrd
import xlsxwriter
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Viewport
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import Application, Button, Form, Label, TextBox, CheckBox, FolderBrowserDialog, OpenFileDialog, DialogResult, ComboBox, FormBorderStyle

from rpw.ui.forms import SelectFromList
value = SelectFromList('Select Project Status', ['#1 - SD/CD','#2 - Building Permit','#3 - Tender', '#4 - IFC'])

sheetsize = SelectFromList('Select Sheet Size', ['#1 - 24x36','#2 - 30x42','#3 - 36x48'])
#print(value)



doc = __revit__.ActiveUIDocument.Document

sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
drafting_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).ToElements()
level_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType()
slab_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType()
wall_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType()
column_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType()
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules).OfClass(ViewSchedule).ToElements()
family_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericAnnotation).WhereElementIsNotElementType().ToElements()
ftg_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType()
framing_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType()

######open excel
# mpath = ""
#
# dialog = FolderBrowserDialog()
#
# dialog = OpenFileDialog()
#
# if(dialog.ShowDialog() == DialogResult.OK):
#     mpath = dialog.FileName
#
# rpath = mpath.replace('\\', '/')
#
# path = rpath


#wb = xlrd.open_workbook(path)


##revit model sheet tab
#worksheet2 = wb.sheet_by_index(1)


##Stage-Division sheet tab
#worksheet4 = wb.sheet_by_index(3)


##Category-Familysheet tab
#worksheet10 = wb.sheet_by_index(9)



#####density  & factor
##concrete:
psi_4000_density = {"0% fly ash": (2259.7141245, 0.231), "20% fly ash":(2217.77692725, 0.214), "30% fly ash":(2195.844255125, 0.2042),
                    "40% fly ash":(2172.484012625,0.1939), "30% slag":(2251.59365925, 0.1822), "40% slag":(2248.99807675,0.166),
                    "50% slag":(2247.4036475,0.1497), "20% fly ash and 30% slag":(2210.0272595, 0.1615)}

psi_5000_density = {"0% fly ash": (2279.66303, 0.27128), "20% fly ash":(2228.4188155, 0.2506), "30% fly ash":(2200.145506125, 0.2389),
                    "40% fly ash":(2171.260380875,0.2263), "30% slag":(2269.54025825, 0.2105), "40% slag":(2267.352553,0.1904),
                    "50% slag":(2264.386173,0.1697), "20% fly ash and 30% slag":(2218.110645, 0.1848)}

psi_6000_density = {"0% fly ash": (2340.73337825, 0.2771), "20% fly ash":(2287.11605975, 0.25592), "30% fly ash":(2257.0443825, 0.2441),
                    "40% fly ash":(2225.78615325,0.2311), "30% slag":(2330.6106065, 0.2149), "40% slag":(2327.82962525,0.194),
                    "50% slag":(2325.048644,0.173), "20% fly ash and 30% slag":(2276.400012, 0.18864)}

psi_8000_density = {"0% fly ash": (2356.15855425, 0.3123), "20% fly ash":(2291.26899175, 0.2883), "30% fly ash":(2257.6376585, 0.2748),
                    "40% fly ash":(2220.8545465,0.2597), "30% slag":(2344.8492305, 0.2395), "40% slag":(2340.1030225,0.2147),
                    "50% slag":(2337.32204125,0.1902), "20% fly ash and 30% slag":(2279.77426925, 0.209)}
##steel:

stee_beam_post_density = (7850, 1.094)
steel_rebar_density = (7850, 1.42)

##wood
wood_density = {"wood framing":(433.57, 0.5367), "plywood":(491.17, 0.6374), "heavy timber":(529, 0.5588), "CLT":(490, 0.7224),
                "glulam":(533.97, 0.7224), "LSL/OSL":(545.87, 0.7434), "LVL":(545.87, 0.7214), "PSL":(630,0.7214), "Concrete Topping":(2217.77692725, 0.214),}
total_misc = []

##########slab gwp
slab_not_found = []
total_allslab_volume = 0
total_woodflooring_volume = 0
total_woodsheathing_volume = 0
total_deck_volume = 0
total_groundfloor_volume = 0
total_parking_volume = 0
total_ptslab_volume = 0
total_roofslab_volume = 0
total_sog_volume = 0
total_tower_volume = 0
total_slabband_volume = 0
total_topping_volume = 0
for floor in slab_collector:
    floor_name = floor.LookupParameter("Type").AsValueString()
    floor_vol_ft3 = floor.LookupParameter("Volume").AsDouble()
    floor_vol_m3 = floor_vol_ft3 * 0.0283168466
    #total_allslab_volume += floor_vol_m3
    if "Wood" in floor_name:
        wood_floor_type = doc.GetElement(floor.GetTypeId())
        compound_structure = wood_floor_type.GetCompoundStructure()
        floor_area_ft2 = floor.LookupParameter("Area").AsDouble()
        floor_area_m2 = floor_area_ft2 * 0.09290304
        layers = compound_structure.GetLayers()
        for layer in layers:
            layer_name = doc.GetElement(layer.MaterialId).Name
            layer_thickness_m = layer.Width * 0.3048
            layer_volume_m3 = floor_area_m2 * layer_thickness_m
            if "Wood" in layer_name:
                if "Flooring" in layer_name:
                    total_woodflooring_volume += layer_volume_m3
                elif "Sheathing" in layer_name:
                    total_woodsheathing_volume += layer_volume_m3
            elif "Concrete" in layer_name:
                total_topping_volume += layer_volume_m3
            else:
                total_woodflooring_volume += layer_volume_m3
    elif "Deck" in floor_name:
        total_deck_volume += floor_vol_m3
    else:
        #total_all_volume += floor_vol_ft3
        if "GS Slab_Ground Floor" in floor_name:
            total_groundfloor_volume += floor_vol_m3

        elif "GS Slab_Parking" in floor_name:
            total_parking_volume += floor_vol_m3
        elif "GS Slab_PT" in floor_name:
            total_ptslab_volume += floor_vol_m3
        elif "GS Slab_Roof" in floor_name:
            total_roofslab_volume += floor_vol_m3
        elif "GS Slab_SOG" in floor_name:
            total_sog_volume += floor_vol_m3
        elif "GS Slab_Tower" in floor_name:
            total_tower_volume += floor_vol_m3
        elif "GS Slabband" in floor_name:
            total_slabband_volume += floor_vol_m3
        else:
            slab_not_found.append(floor_name)


if len(slab_not_found) > 0:
    print("below list are the names of slab type not found, please change slab name per standard:")
    print(slab_not_found)
else:
    pass

#ground floor gwp - 2.3% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_groundfloor_volume * v[0]
        total_rebar_weight_kg = total_groundfloor_volume * 0.023 * steel_rebar_density[0]
        total_gwp_groundfloor = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#parking floor gwp - 1.3% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_parking_volume * v[0]
        total_rebar_weight_kg = total_parking_volume * 0.013 * steel_rebar_density[0]
        total_gwp_parking = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#pt slab gwp - 1.2% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_ptslab_volume * v[0]
        total_rebar_weight_kg = total_ptslab_volume * 0.012 * steel_rebar_density[0]
        total_gwp_pt = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#roof slab gwp - 1.5% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_roofslab_volume * v[0]
        total_rebar_weight_kg = total_roofslab_volume * 0.015 * steel_rebar_density[0]
        total_gwp_roof = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#sog gwp - 1.0% rebar
for k, v in psi_4000_density.items():
    if k == "30% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_sog_volume * v[0]
        total_rebar_weight_kg = total_sog_volume * 0.01 * steel_rebar_density[0]
        total_gwp_sog = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#tower gwp - 1.4% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_tower_volume * v[0]
        total_rebar_weight_kg = total_tower_volume * 0.014 * steel_rebar_density[0]
        total_gwp_tower = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#slabband gwp - 2.3% rebar
for k, v in psi_6000_density.items():
    if k == "20% fly ash and 30% slag":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_slabband_volume * v[0]
        total_rebar_weight_kg = total_slabband_volume * 0.023 * steel_rebar_density[0]
        total_gwp_slabband = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

###topping - 0% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_topping_volume * v[0]
        total_gwp_topping = (total_concrete_weight_kg * v[1])

#wood flooring gwp
for k, v in wood_density.items():
    if k == "wood framing":
        # print(v[0], v[1])
        total_gwp_woodflooring = total_woodflooring_volume * v[0] * v[1]

#wood sheathing gwp
for k, v in wood_density.items():
    if k == "plywood":
        # print(v[0], v[1])
        total_gwp_woodsheathing = total_woodsheathing_volume * v[0] * v[1]

total_gwp_allfloor = total_gwp_groundfloor + total_gwp_parking + total_gwp_pt + total_gwp_roof + total_gwp_sog + total_gwp_tower + total_gwp_slabband + total_gwp_topping + total_gwp_woodflooring + total_gwp_woodsheathing
#print(total_gwp_allfloor)



######wall gwp
wall_not_found = []
total_allwall_volume = 0
total_woodwall_framing_volume = 0
total_woodwall_sheathing_volume = 0
total_basementwall_volume = 0
total_shearwall_volume = 0
total_otherwall_volume = 0
for wall in wall_collector:
    wall_name = wall.LookupParameter("Type").AsValueString()
    wall_vol_ft3 = wall.LookupParameter("Volume").AsDouble()
    wall_vol_m3 = wall_vol_ft3 * 0.0283168466
    if "GS Wall_Wood" in wall_name:
        wood_wall_type = doc.GetElement(wall.GetTypeId())
        wall_width_ft = wood_wall_type.Width
        wall_width_m = wall_width_ft * 0.3048
        compound_structure = wood_wall_type.GetCompoundStructure()
        layers = compound_structure.GetLayers()
        for layer in layers:
            layer_name = doc.GetElement(layer.MaterialId).Name
            layer_thickness_m = layer.Width * 0.3048
            layer_thickness_percentage = layer_thickness_m/wall_width_m
            layer_volume_m3 = wall_vol_m3 * layer_thickness_percentage
            if "Sheathing" in layer_name:
                total_woodwall_sheathing_volume += layer_volume_m3
            else:
                total_woodwall_framing_volume += layer_volume_m3
    elif "GS Wall_Arch" in wall_name:
        pass
    else:
        if "GS Wall_Basement" in wall_name:
            total_basementwall_volume += wall_vol_m3
        elif "GS Wall_Header" in wall_name:
            total_shearwall_volume += wall_vol_m3
        elif "GS Wall_Shearwall" in wall_name:
            total_shearwall_volume += wall_vol_m3
        else:
            total_otherwall_volume += wall_vol_m3

#basementwall gwp - 1.9% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash and 30% slag":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_basementwall_volume * v[0]
        total_rebar_weight_kg = total_basementwall_volume * 0.019 * steel_rebar_density[0]
        total_gwp_basementwall = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#otherwall gwp - 1.9% rebar
for k, v in psi_5000_density.items():
    if k == "20% fly ash and 30% slag":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_otherwall_volume * v[0]
        total_rebar_weight_kg = total_otherwall_volume * 0.019 * steel_rebar_density[0]
        total_gwp_otherwall = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#shearwall gwp - 3.4% rebar
for k, v in psi_6000_density.items():
    if k == "30% fly ash":
        # print(v[0], v[1])
        total_concrete_weight_kg = total_shearwall_volume * v[0]
        total_rebar_weight_kg = total_shearwall_volume * 0.034 * steel_rebar_density[0]
        total_gwp_shearwall = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#woodwall framing gwp
for k, v in wood_density.items():
    if k == "wood framing":
        # print(v[0], v[1])
        total_gwp_woodwall = total_woodwall_framing_volume * v[0] * v[1]

#wood sheathing gwp
for k, v in wood_density.items():
    if k == "plywood":
        # print(v[0], v[1])
        total_gwp_woodwallsheathing = total_woodwall_sheathing_volume * v[0] * v[1]

total_gwp_allwall = total_gwp_basementwall + total_gwp_otherwall + total_gwp_shearwall + total_gwp_woodwall + total_gwp_woodwallsheathing
#print(total_gwp_allwall)




########column gwp
total_allcol_volume = 0
total_woodcol_volume = 0
total_steelcol_volume = 0
total_concretecol_volume = 0
for column in column_collector:
    col_name = column.LookupParameter("Family").AsValueString()
    col_vol_ft3 = column.LookupParameter("Volume").AsDouble()
    col_vol_m3 = col_vol_ft3 * 0.0283168466
    if "GS Wood" in col_name:
        total_woodcol_volume += col_vol_m3
    elif "GS Concrete" in col_name:
        total_concretecol_volume += col_vol_m3
    elif "Structural Columns" in col_name:
        total_concretecol_volume += col_vol_m3
    elif "CISC" in col_name:
        total_steelcol_volume += col_vol_m3
    elif "HSS" in col_name:
        total_steelcol_volume += col_vol_m3
    elif "Wide Flange" in col_name:
        total_steelcol_volume += col_vol_m3
    else:
        total_concretecol_volume += col_vol_m3
        
#wood col gwp
for k, v in wood_density.items():
    if k == "wood framing":
        # print(v[0], v[1])
        total_gwp_woodcol = total_woodcol_volume * v[0] * v[1]

#steel col gwp
total_gwp_steelcol = total_steelcol_volume * stee_beam_post_density[0] * stee_beam_post_density[1]

#concrete col gwp - 3.4% rebar
for k, v in psi_6000_density.items():
    if k == "40% fly ash":
        total_concrete_weight_kg = total_concretecol_volume * v[0]
        total_rebar_weight_kg = total_concretecol_volume * 0.034 * steel_rebar_density[0]
        total_gwp_concretecol = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

total_gwp_allcol = total_gwp_concretecol

total_misc.append(total_gwp_woodcol)
total_misc.append(total_gwp_steelcol)


####### ftg gwp
total_allftg_volume = 0
total_pad_strip_ftg_volume = 0
total_mat_ftg_volume = 0
for ftg in ftg_collector:
    ftg_name = ftg.LookupParameter("Family").AsValueString()
    ftg_vol_ft3 = ftg.LookupParameter("Volume").AsDouble()
    ftg_vol_m3 = ftg_vol_ft3 * 0.0283168466
    if "Wall Foundation" in ftg_name:
        total_pad_strip_ftg_volume += ftg_vol_m3
    elif "GS Rectangular Footing" in ftg_name:
        total_pad_strip_ftg_volume += ftg_vol_m3
    elif "Structural Foundations" in ftg_name:
        total_pad_strip_ftg_volume += ftg_vol_m3
    elif "GS Stepped Footing" in ftg_name:
        total_pad_strip_ftg_volume += ftg_vol_m3
    elif "Foundation Slab" in ftg_name:
        total_mat_ftg_volume += ftg_vol_m3
    else:
        total_pad_strip_ftg_volume += ftg_vol_m3

#pad/strip ftg gwp - 1.4% rebar
for k, v in psi_4000_density.items():
    if k == "20% fly ash and 30% slag":
        total_concrete_weight_kg = total_pad_strip_ftg_volume * v[0]
        total_rebar_weight_kg = total_pad_strip_ftg_volume * 0.014 * steel_rebar_density[0]
        total_gwp_pad_strip_ftg = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

#mat ftg gwp - 2.3% rebar
for k, v in psi_4000_density.items():
    if k == "20% fly ash and 30% slag":
        total_concrete_weight_kg = total_mat_ftg_volume * v[0]
        total_rebar_weight_kg = total_mat_ftg_volume * 0.023 * steel_rebar_density[0]
        total_gwp_mat_ftg = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

total_gwp_allftg = total_gwp_pad_strip_ftg + total_gwp_mat_ftg


####### framing gwp
framing_not_found = []
total_allframing_volume = 0
total_woodframing_volume = 0
total_steelframing_volume = 0
total_concreteframing_volume = 0
for fam in framing_collector:
    fam_name = fam.LookupParameter("Family").AsValueString()
    fam_vol_ft3 = fam.LookupParameter("Volume").AsDouble()
    fam_vol_m3 = fam_vol_ft3 * 0.0283168466
    if "GS Wood" in fam_name:
        total_woodframing_volume += fam_vol_m3
    elif "HSS" in fam_name:
        total_steelframing_volume += fam_vol_m3
    elif "Wide Flange" in fam_name:
        total_steelframing_volume += fam_vol_m3
    elif "Channel" in fam_name:
        total_steelframing_volume += fam_vol_m3
    elif "OWSJ" in fam_name:
        total_steelframing_volume += fam_vol_m3
    elif "Concrete" in fam_name:
        total_concreteframing_volume += fam_vol_m3
    else:
        framing_not_found.append(fam_name)

if len(framing_not_found) > 0:
    print("below list are the names of framing type not found, please check with steve:")
    print(framing_not_found)
else:
    pass

#wood framing gwp
for k, v in wood_density.items():
    if k == "PSL":
        # print(v[0], v[1])
        total_gwp_woodframing = total_woodframing_volume * v[0] * v[1]

#steel framing gwp
total_gwp_steelframing = total_steelframing_volume * stee_beam_post_density[0] * stee_beam_post_density[1]

#concrete framing gwp - 2.3% rebar
for k, v in psi_6000_density.items():
    if k == "20% fly ash and 30% slag":
        total_concrete_weight_kg = total_concreteframing_volume * v[0]
        total_rebar_weight_kg = total_concreteframing_volume * 0.023 * steel_rebar_density[0]
        total_gwp_concreteframing = (total_concrete_weight_kg*v[1]) + (total_rebar_weight_kg*steel_rebar_density[1])

total_gwp_allframing = total_gwp_concreteframing

total_misc.append(total_gwp_woodframing)
total_misc.append(total_gwp_steelframing)


##### combine all
total_gwp_misc = sum(total_misc) ### still need to append on wood floor and wood wall
final_gwp = total_gwp_allfloor + total_gwp_allwall + total_gwp_allcol + total_gwp_allftg + total_gwp_allframing + total_gwp_misc

# print("total floor gwp (kg/m3): " + str(total_gwp_allfloor))
# print("total wall gwp (kg/m3): " + str(total_gwp_allwall))
# print("total column gwp (kg/m3): " + str(total_gwp_allcol))
# print("total ftg gwp (kg/m3): " + str(total_gwp_allftg))
# print("total framing gwp (kg/m3): " + str(total_gwp_allframing))
# print("----------------------------------------------------")
# print("Final gwp (kg/m3): " + str(final_gwp))


newt = Transaction(doc)
newt.Start('New Transaction')

###place view to sheets
sheet_name = "Internal Use"

schedule_name1 = "SLAB VOLUME"
schedule_name2 = "WALL VOLUME"
schedule_name3 = "COLUMN VOLUME"
schedule_name4 = "FOUNDATION VOLUME"
#
schedule_name5 = "SLAB FORMWORK AREA"
schedule_name6 = "WALL FORMWORK AREA"
schedule_name7 = "COLUMN FORMWORK AREA"
schedule_name8 = "FOUNDATION FORMWORK AREA"
#
if sheetsize == "#1 - 24x36":
    drafting_view_name = "Quantity & GWP Estimate (24x36)"
    coordinate = XYZ(1.5, 0.99, 0)
    schedule_coordinate1 = XYZ(0.22, 0.88, 0)
    schedule_coordinate2 = XYZ(0.58, 0.88, 0)
    schedule_coordinate3 = XYZ(0.80, 0.88, 0)
    schedule_coordinate4 = XYZ(0.22, 0.3, 0)
    #
    schedule_coordinate5 = XYZ(1.18, 0.88, 0)
    schedule_coordinate6 = XYZ(1.46, 0.88, 0)
    schedule_coordinate7 = XYZ(1.72, 0.88, 0)
    schedule_coordinate8 = XYZ(1.18, 0.3, 0)

elif sheetsize == "#2 - 30x42":
    drafting_view_name = "Quantity & GWP Estimate (30x42)"
    coordinate = XYZ(1.7, 1.25, 0)
    schedule_coordinate1 = XYZ(0.38, 1.27, 0)
    schedule_coordinate2 = XYZ(0.74, 1.27, 0)
    schedule_coordinate3 = XYZ(0.96, 1.27, 0)
    schedule_coordinate4 = XYZ(0.38, 0.4, 0)
    #
    schedule_coordinate5 = XYZ(1.32, 1.27, 0)
    schedule_coordinate6 = XYZ(1.60, 1.27, 0)
    schedule_coordinate7 = XYZ(1.86, 1.27, 0)
    schedule_coordinate8 = XYZ(1.32, 0.4, 0)

elif sheetsize == "#3 - 36x48":
    drafting_view_name = "Quantity & GWP Estimate (36x48)"
    coordinate = XYZ(1.6, 1.5, 0)
    schedule_coordinate1 = XYZ(0.28, 1.72, 0)
    schedule_coordinate2 = XYZ(0.64, 1.72, 0)
    schedule_coordinate3 = XYZ(0.86, 1.72, 0)
    schedule_coordinate4 = XYZ(0.28, 0.6, 0)
    #
    schedule_coordinate5 = XYZ(1.37, 1.72, 0)
    schedule_coordinate6 = XYZ(1.65, 1.72, 0)
    schedule_coordinate7 = XYZ(1.91, 1.72, 0)
    schedule_coordinate8 = XYZ(1.37, 0.6, 0)
#
#
drafting_view = None
for view in drafting_views:
    if view.Name == drafting_view_name:
        drafting_view = view
        break

sheet = None
for sht in sheets:
    if sht.Name == sheet_name:
        sheet = sht
        break

viewport = Viewport.Create(doc, sheet.Id, drafting_view.Id, coordinate)

schedule = None
for sched in collector:
    if sched.Name == schedule_name1:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate1)
    elif sched.Name == schedule_name2:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate2)
    elif sched.Name == schedule_name3:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate3)
    elif sched.Name == schedule_name4:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate4)
    elif sched.Name == schedule_name5:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate5)
    elif sched.Name == schedule_name6:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate6)
    elif sched.Name == schedule_name7:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate7)
    elif sched.Name == schedule_name8:
        schedule = sched
        schedule_instance = ScheduleSheetInstance.Create(doc, sheet.Id, schedule.Id, schedule_coordinate8)

total_slab_area = 0.0
total_transferslab_area = 0.0
for floor in slab_collector:
    floor_param = floor.LookupParameter("Area")
    if floor_param:
        total_slab_area += floor_param.AsDouble()
total_slab_area_m2 = round((total_slab_area * 0.092903), 1)

for floor in slab_collector:
    floor_param = floor.LookupParameter("Area")
    floor_name = floor.LookupParameter("Type").AsValueString()
    if "Slabband" in floor_name:
        total_transferslab_area += floor_param.AsDouble()

total_transferslab_area_m2 = round((total_transferslab_area * 0.092903), 1)
total_typslab_area_m2 = total_slab_area_m2 - total_transferslab_area_m2


total_gwp_per_area = round(final_gwp / total_slab_area_m2, 1)
#print(total_gwp_per_area, final_gwp, total_slab_area_m2)

for string in family_collector:
    param1 = string.LookupParameter("Type").AsValueString()
    param2 = string.LookupParameter("GWP")
    param3 = string.LookupParameter("SD/CD")
    param4 = string.LookupParameter("BP")
    param5 = string.LookupParameter("TENDER")
    param6 = string.LookupParameter("IFC")
    if param1 == "GS_Quantities&Gwp_Global Warming Potential":
        param2.Set(str(total_gwp_per_area))
        if value == "#1 - SD/CD":
            param3.Set(str(total_gwp_per_area))
        elif value == "#2 - Building Permit":
            param4.Set(str(total_gwp_per_area))
        elif value == "#3 - Tender":
            param5.Set(str(total_gwp_per_area))
        elif value == "#4 - IFC":
            param6.Set(str(total_gwp_per_area))

total_gwp_col = round(total_gwp_allcol, 1)/total_slab_area_m2
total_gwp_wall = round(total_gwp_allwall, 1)/total_slab_area_m2
total_gwp_floor = round(total_gwp_allfloor, 1)/total_slab_area_m2
total_gwp_ftg = round(total_gwp_allftg, 1)/total_slab_area_m2
total_gwp_transfer = round(total_gwp_slabband, 1)/total_slab_area_m2
total_gwp_misc = round(total_gwp_misc, 1)/total_slab_area_m2

def set_data():
    for string in family_collector:
        param1 = string.LookupParameter("Type").AsValueString()
        param2 = string.LookupParameter("SLAB GWP")
        #param2_1 = string.LookupParameter("TYP SLAB AREA")
        param3 = string.LookupParameter("WALL GWP")
        param4 = string.LookupParameter("COLUMN GWP")
        param5 = string.LookupParameter("FOUNDATION GWP")
        param6 = string.LookupParameter("TRANSFER GWP")
        #param6_1 = string.LookupParameter("TRANSFER SLAB AREA")
        param7 = string.LookupParameter("MISC GWP")


        if param1 == "GS_Quantities&Gwp_Total Slab GWP":
            param2.Set(str(round(total_gwp_floor, 1)))
            #param2_1.Set(str(round(total_typslab_area_m2, 1)))
        if param1 == "GS_Quantities&Gwp_Total Wall GWP":
            param3.Set(str(round(total_gwp_wall, 1)))
        if param1 == "GS_Quantities&Gwp_Total Column GWP":
            param4.Set(str(round(total_gwp_col, 1)))
        if param1 == "GS_Quantities&Gwp_Total Ftg GWP":
            param5.Set(str(round(total_gwp_ftg, 1)))
        if param1 == "GS_Quantities&Gwp_Total Transfer GWP":
            param6.Set(str(round(total_gwp_transfer, 1)))
            #param6_1.Set(str(round(total_transferslab_area_m2, 1)))
        if param1 == "GS_Quantities&Gwp_Total Misc GWP":
            param7.Set(str(round(total_gwp_misc, 1)))

##U:\Steve\LCA\family

set_data()
set_data()


### SET QUANTITY FAMILY

total_slab_volume = 0.0
for floor in slab_collector:
    floor_name = floor.LookupParameter("Type").AsValueString()
    floor_param = floor.LookupParameter("Volume")
    if "Wood" in floor_name:
        pass
    else:
        if floor_param:
            total_slab_volume += floor_param.AsDouble()
total_slab_volume_cy = int(total_slab_volume / 27)

total_wall_volume = 0.0
for wall in wall_collector:
    wall_name = wall.LookupParameter("Type").AsValueString()
    vol_param = wall.LookupParameter("Volume")
    if "Wood" in wall_name:
        pass
    else:
        if vol_param:
            total_wall_volume += vol_param.AsDouble()
total_wall_volume_cy = int(total_wall_volume / 27)

total_column_volume = 0.0
for column in column_collector:
    col_param = column.LookupParameter("Volume")
    col_name = column.LookupParameter("Type").AsValueString()
    col_type = column.LookupParameter("Family").AsValueString()
    if "H" in col_name:
        pass
    elif "W" in col_name:
        pass
    elif "Wood" in col_type:
        pass
    else:
        total_column_volume += col_param.AsDouble()

total_column_volume_cy = int(total_column_volume / 27)

total_foundation_volume = 0.0
for foundation in ftg_collector:
    ftg_param = foundation.LookupParameter("Volume")
    if ftg_param:
        total_foundation_volume += ftg_param.AsDouble()
total_foundation_volume_cy = int(total_foundation_volume / 27)

total_concrete_volume = total_slab_volume_cy + total_wall_volume_cy + total_column_volume_cy + total_foundation_volume_cy
total_concrete_volume_with_allowance = total_concrete_volume * 1.05
con_volume = "CONCRETE VOLUME:   {:,}".format(total_concrete_volume_with_allowance) + " CY"

# CONCRETE FORMWORK AREA
sog_area_list = []
total_slab_area = 0.0
for floor in slab_collector:
    floor_area_param = floor.LookupParameter("Area")
    floor_name = floor.LookupParameter("Type").AsValueString()
    if "Wood" in floor_name:
        pass
    else:
        if floor_area_param:
            total_slab_area += floor_area_param.AsDouble()

for floor in slab_collector:
    sog_area_param = floor.LookupParameter("Area").AsDouble()
    floor_name = floor.LookupParameter("Type").AsValueString()
    if "SOG" in floor_name:
        sog_area_list.append(sog_area_param)
    else:
        sog_area = 0

sog_area_number = sum(sog_area_list)
total_slab_horiz_area = int(total_slab_area - sog_area_number)
total_slab_area_with_allowance = total_slab_area * 1.05

slab_area = "SLAB AREA:          {:,}".format(round(total_slab_area_with_allowance), 1) + " SF"

total_slab_area2 = []
for floor in slab_collector:
    try:
        floor_core_thk_param = floor.LookupParameter("Thickness").AsDouble()
        floor_perimeter_param = floor.LookupParameter("Perimeter").AsDouble()
        floor_name = floor.LookupParameter("Type").AsValueString()
        if "SOG" in floor_name:
            pass
        elif "Wood" in floor_name:
            pass
        elif floor_core_thk_param != None or floor_perimeter_param != None:
            floor_vert_area = floor_core_thk_param * floor_perimeter_param
            total_slab_area2.append(floor_vert_area)
    except:
        pass
total_floor_vert_area = int(sum(total_slab_area2))

total_slab_formwork_area = total_slab_horiz_area + total_floor_vert_area

total_wall_area = 0.0
for wall in wall_collector:
    wall_area_param = wall.LookupParameter("Area")
    wall_name = wall.LookupParameter("Type").AsValueString()
    if "Wood" in wall_name:
        pass
    else:
        if wall_area_param:
            total_wall_area += wall_area_param.AsDouble()
total_wall_formwork_area = int(total_wall_area * 2)

t_area = []
for column in column_collector:
    col_area = column.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED).AsDouble()
    col_vol = column.LookupParameter("Volume").AsDouble()
    col_Height = column.LookupParameter("Length").AsDouble()
    col_n = column.LookupParameter("Type").AsValueString()
    col_type = column.LookupParameter("Family").AsValueString()
    if "H" in col_n:
        pass
    elif "W" in col_n:
        pass
    elif "Wood" in col_type:
        pass
    else:
        if col_Height != 0:
            col_formwork_area = (float(col_area) * 2) - (float(col_vol) / float(col_Height) * 2)
            t_area.append(col_formwork_area)
total_column_formwork_area = int(sum(t_area))

ft_area = []
total_foundation_area = 0.0
for ftg in ftg_collector:
    try:
        ftg_vol = ftg.LookupParameter("Volume").AsDouble()
        ftg_length = ftg.LookupParameter("Length").AsDouble()
        ftg_width = ftg.LookupParameter("Width").AsDouble()
        if ftg_length != 0 and ftg_width != 0:
            ftg_formwork_area = 2 * (float(ftg_length) + float(ftg_width)) * (
                    float(ftg_vol) / float(ftg_length) / float(ftg_width))
            ft_area.append(ftg_formwork_area)
    except:
        pass

total_foundation_formwork_area = int(sum(ft_area))

total_formwork_area = int(
    total_slab_formwork_area + total_wall_formwork_area + total_column_formwork_area + total_foundation_formwork_area)
total_formwork_area_with_allowance = total_formwork_area * 1.05
formwork_area = "FORWORK AREA:        {:,}".format(total_formwork_area_with_allowance) + " SF"

average_dep = total_concrete_volume_with_allowance * 12 * 27 / total_slab_area_with_allowance
round1 = round(average_dep, 1)
average_formwork_ratio = total_formwork_area_with_allowance / total_slab_area_with_allowance
round2 = round(average_formwork_ratio, 2)
ave_dp = "+/-{}".format(round1) + '"'
ratio = "+/-{}".format(round2)


def set_data2():
    for string in family_collector:
        param1 = string.LookupParameter("Type").AsValueString()
        param2 = string.LookupParameter("SLAB AREA")
        param3 = string.LookupParameter("CONC VOLUME")
        param4 = string.LookupParameter("FORMWORK AREA")
        param5 = string.LookupParameter("AVERAGE DEPTH")
        param6 = string.LookupParameter("FORMWORK RATIO")
        if param1 == "GS_Quantities&Gwp_Total Slab Area":
            param2.Set(slab_area)
        if param1 == "GS_Quantities&Gwp_Total Concrete Volume":
            param3.Set(con_volume)
        if param1 == "GS_Quantities&Gwp_Total Formwork Area":
            param4.Set(formwork_area)
        if param1 == "GS_Quantities&Gwp_Average Depth":
            param5.Set(ave_dp)
        if param1 == "GS_Quantities&Gwp_Formwork Ratio":
            param6.Set(ratio)


set_data2()

newt.Commit()

###write to excel for bar chart to take data
workbook1 = xlsxwriter.Workbook(r'U:\Steve\LCA\temp xlsx\temp.xlsx')
worksheet1 = workbook1.add_worksheet()

worksheet1.write('A1', "SD/CD")
worksheet1.write('A2', "BUILDING PERMIT")
worksheet1.write('A3', "TENDER")
worksheet1.write('A4', "IFC")

for string in family_collector:
    param1 = string.LookupParameter("Type").AsValueString()
    param2 = string.LookupParameter("GWP")
    param3 = string.LookupParameter("SD/CD")
    param4 = string.LookupParameter("BP")
    param5 = string.LookupParameter("TENDER")
    param6 = string.LookupParameter("IFC")
    if param1 == "GS_Quantities&Gwp_Global Warming Potential":
        worksheet1.write('B1', str(param3.AsString()))
        worksheet1.write('B2', str(param4.AsString()))
        worksheet1.write('B3', str(param5.AsString()))
        worksheet1.write('B4', str(param6.AsString()))

workbook1.close()