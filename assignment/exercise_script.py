import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
import pandas as pd
from matplotlib.pyplot import pie, axis, show


# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


# load the datasets
towns = gpd.read_file('data_files/Towns.shp')
farms = gpd.read_file('data_files/farms2.shp')
counties = gpd.read_file('data_files/Counties.shp')
mdm = pd.read_csv('data_files/MDM_data.csv')


# calculate max, min, mean and sum area of the counties.
max_area = counties['Area_SqKM'].max()
min_area = counties['Area_SqKM'].min()
mean_area = counties['Area_SqKM'].mean()
sum_area = counties['Area_SqKM'].sum()
print(counties[counties['Area_SqKM'] > 10])
print("max area: {0} km2".format(max_area))
print("min area: {0} km2".format(min_area))
print("mean area: {0} km2".format(mean_area))
print("sum area: {0} km2".format(counties['Area_SqKM'].sum()))

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.

# set the value column that will be visualised
variable = 'NumberOfFa'
# set the range for the choropleth values
vmin, vmax = 0, 1200
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, 1, figsize=(10,10), subplot_kw=dict(projection=myCRS))

# Create a scatterplot graph of the relationship between Farms and Farmers
fig2, ax2 = plt.subplots(figsize=(10, 6))

ax2.scatter(x=farms['NumberOfFa'], y=farms['TotalNumbe'], edgecolors='r')
plt.xlabel('Farmers')
plt.ylabel('Farms')
plt.title('Relations between Number of Farmers and Farms')

fig2.savefig('scatterplot.png', dpi=300)

# create pie chart of number of farm animals kept in Norther Ireland

x = [1608559, 1985109, 673261, 24805]
labels = ['Cattle', 'Sheeps', 'Pigs', 'Poultry']
colors = ['tab:blue', 'tab:cyan', 'tab:orange', 'tab:red']

fig3, ax3 = plt.subplots(figsize=(10, 10))
ax3.pie(x, labels = labels, colors = colors)
ax3.set_title('Division of farm animals in Northern Ireland')
fig3.savefig('piechart.png', dpi=300)

# add a title and annotation
ax.set_title('Total Farms in each District', fontdict={'fontsize': '25', 'fontweight': '3'})

# Create colorbar legend
sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax))

# empty array for the data range
sm.set_array([])
# add the colorbar to the figure
ax_sm = fig.colorbar(sm, ax=ax)
ax_sm.set_label('Total Farms', fontdict={'fontsize': '15', 'fontweight': '3'})
# create map
farms.plot(column=variable, cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', transform=myCRS)


fig.savefig('map.png', dpi=300)

