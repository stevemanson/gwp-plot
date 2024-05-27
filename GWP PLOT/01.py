import math

# import matplotlib.pyplot as plt
# import openpyxl
# from openpyxl import load_workbook, workbook
# import warnings
#
#
#
# def load_data(path):
#     warnings.simplefilter(action='ignore', category=UserWarning)
#     return load_workbook(path)
#
# def dot_plot(path_save):
#     x = [0, 10, 20, 30]
#     y = [425, 550, 800, -200]
#     color_SDDD = '#ff8040'
#     color_BP = '#cfb036'
#     color_Tender = '#3275b8'
#
#     string = ["RESIDENTIAL", "OFFICE", "INSTITUTION", "OTHER"]
#
#     plt.xticks(x, string, font='Arial')
#
#     plt.ylabel("EMBODIED CARBON INTENSITY (KgCO2/m^2)", font='Arial')
#     plt.grid()
#     plt.scatter(x, y, color='black')
#
#     x = [2, 8, 22, 35]
#     y = [356, 475, -123, 500]
#     plt.scatter(x, y, color='black')
#
#     x = [1.5]
#     y = [309]
#     plt.scatter(x, y, s=100, color=color_SDDD)
#
#     plt.savefig(path_save, dpi=300)
#
#
# p = r"F:\2021\221259\LCA\2022-07-07\2022-07-20 - Tally Report - 360 West 2nd Ave, Vancouver, BC.xlsx"
#
# z=p.replace('\\', '/')
#
# wb = load_data(z)
#
# pdf_save = r'F:\2021\221554\DRAFTING\PLOTS\2022-10-04 - MODEL FOR LCA\PIE CHART.pdf'
#
# dot_plot(pdf_save)

r = 1.5708
pi1 = math.pi

to_degree = r*180/(pi1)

print(round(to_degree))