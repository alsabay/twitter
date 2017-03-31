"""
geoplot.py - plots lat long locations of tweets from mongodb using basemap package
Author: Al Sabay

"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pprint
import json

# create map
#m = Basemap(projection='mill', llcrnrlat=20, urcrnrlat=50, llcrnrlon=-130, urcrnrlon=-60, resolution='c')
m = Basemap('mill')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents(color='brown', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')

#m.bluemarble()
#lat,lon = 29.76, -95.36
#x,y = m(lon,lat)
#m.plot(x,y,'ro')

# get tweet coordinates from mongodb
client = MongoClient('localhost', 27017)
db = client.twit_db
for doc in db.tweet.find({},{"coordinates":1}):
    if doc.get("coordinates"):
        s = doc["coordinates"]["coordinates"]
        lat,lon = s[1],s[0]
        x,y = m(lon,lat)
        m.plot(x,y,'y.')

# plot location on map
plt.title('Tweet locations')
plt.show()


