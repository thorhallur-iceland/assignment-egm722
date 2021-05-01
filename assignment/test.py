import os

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd


from helpers import slug

datafile = pd.readfile('data_files/API_SE.PRM.UNER_DS2_en_csv_v2_2252701')
shapefile = gpd.readfile('data_files/ne_10m_admin_0_countries.shp')

colors = 9
cmap = 'Blues'
fig, figsize = (16, 10)
year = '2020'
cols = ['Country Name', 'Country Code', year]
title = 'Children out of school, primary {}'.format(year)
imgfile = 'img/{}.png'.format(slug(title))

gdf = gpd.read_file(shapefile)[['ADM0_A3', 'geometry']].to_crs('+proj=robin')
gdf.sample(5)

df = pd.read_csv(datafile, skiprows=4, usecols=cols)
df.sample(5)

merged = gdf.merge(df, left_on='ADM0_A3', right_on='Country Code')
merged.describe()

ax = merged.dropna().plot(column=year, cmap=cmap, figsize=figsize, scheme='equal_interval', k=colors, legend=True)

merged[merged.isna().any(axis=1)].plot(ax=ax, color='#fafafa', hatch='///')

ax.set_title(title, fontdict={'fontsize': 20}, loc='left')


ax.set_axis_off()
ax.set_xlim([-1.5e7, 1.7e7])
ax.get_legend().set_bbox_to_anchor((.12, .4))
ax.get_figure()

fig.savefig('map2.png', dpi=300)