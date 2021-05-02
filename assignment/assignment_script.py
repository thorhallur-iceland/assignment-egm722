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
# save and print figure
fig2.savefig('scatterplot.png', dpi=300)


# Create a pie chart, dividing each farm animal into a wedge represented with total number of each animal and percentage
fig3, ax3 = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
# adding the data
numanimals = ["1608559 Cattle", "1985109 Sheeps", "673261 Pigs", "24805 Poultry"]
data =[float(x.split()[0]) for x in numanimals]
animals =[x.split()[-1] for x in numanimals]


# create a function that calculates percentage
def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d} )".format(pct, absolute)


wedges, texts, autotexts = ax3.pie(data, autopct=lambda pct: func(pct, data), textprops=dict(color="w"))

ax3.legend(wedges, animals, title="Animals", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
plt.setp(autotexts, size=8, weight="bold")

ax3.set_title("Division of Animals in Northern Ireland")
# save and print figure
fig3.savefig('piechart.png')

# add a title
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

# save and print figure
fig.savefig('map.png', dpi=300)

