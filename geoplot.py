"""
geoplot.py - plots lat long locations of tweets from mongodb
Author: Al Sabay

"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection='mill', llcrnrlat=20, urcrnrlat=50, llcrnrlon=-130, urcrnrlon=-60, resolution='c')
#m = Basemap('mill')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents(color='brown', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
#m.bluemarble()

#query mongodb for tweet locations and keywords

lat,lon = 29.76, -95.36
x,y = m(lon,lat)
m.plot(x,y,'ro')

plt.title('Tweet locations')
plt.show()


