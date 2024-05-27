# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.pyplot as plt

total_gwp_col_persentage = 21
total_gwp_wall_persentage = 82.4
total_gwp_floor_persentage = 172.6
total_gwp_ftg_persentage = 11.5
total_gwp_misc_persentage = 0.9
#total_gwp_transfer_persentage = 23.9


total_gwp_shearwall_persentage = 62.4
total_gwp_basementwall_persentage = 20.0
total_gwp_transfer_persentage = 23.9
total_gwp_towerslab_persentage = 100.7
total_gwp_parkingslab_persentage = 48.7


x_value = (
total_gwp_col_persentage, total_gwp_wall_persentage, total_gwp_floor_persentage,
total_gwp_ftg_persentage, total_gwp_misc_persentage)

labels = ["COLUMN", "WALL", "SLAB", "FTG", "MISC"]
mycolors = ['#3c78d8', '#6aa84f', '#f1c232', '#999999', '#b4a7d6']
explodes = (0, 0, 0, 0, 0)

#ff8040

labels2 = ["COLUMN", "SHEARWALL", "BASEMENTWALL", "TRANSFER", "TOWERSLAB", "PARKINGSLAB","FTG", "MISC"]
mycolors2 = ['#6f97d6', '#8adb67', '#b2f595', '#ff8040', "#ffd040", "#fcda72",'#999999', '#b4a7d6']

plt.pie([total_gwp_col_persentage, total_gwp_wall_persentage, total_gwp_floor_persentage, total_gwp_ftg_persentage, total_gwp_misc_persentage],
        radius = 1.2,
        labels=labels, colors=mycolors, autopct='%.1f%%', pctdistance=(1-0.3/2),
        wedgeprops=dict(width=0.4, edgecolor='w'))

plt.pie([total_gwp_col_persentage, total_gwp_shearwall_persentage, total_gwp_basementwall_persentage,  total_gwp_transfer_persentage, total_gwp_towerslab_persentage,total_gwp_parkingslab_persentage,total_gwp_ftg_persentage, total_gwp_misc_persentage],
        radius = (1.2-0.4),
        colors = mycolors2, autopct='%.1f%%', pctdistance=(1-0.4/2),
        wedgeprops=dict(width=0.4, edgecolor='w'))



plt.show()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
