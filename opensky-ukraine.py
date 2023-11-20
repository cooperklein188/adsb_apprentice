from pyopensky.impala import Impala
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt


impala = Impala()

'''18 columns!!!'''
# Index(['time', 'icao24', 'lat', 'lon', 'velocity', 'heading', 'vertrate',     
#        'callsign', 'onground', 'alert', 'spi', 'squawk', 'baroaltitude',      
#        'geoaltitude', 'lastposupdate', 'lastcontact', 'hour'],
#       dtype='object') 

# #day 1: 12/1/2020
# df1 = impala.history(start = 1606842000, stop = 1606842005, airport= "LLBG")

# #day 2: 12/2/2020
# df2 = impala.history(start = 1606928400, stop = 1606928405, airport= "LLBG")

df1 = impala.history(start = 1493632800, stop = 1493632802)
#2 seconds will offer every point without repetition

# df2 = impala.history(start = 1543770000, stop = 1543770030)

def loc(df, lat, lon, buff):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))

    # Create a GeoSeries with the target point
    target_point = gpd.GeoSeries([Point(lon, lat)], crs=gdf.crs)
    buffered_target_point = target_point.buffer(buff)  # 1 degree of latitude is approximately 69 miles
    # Use spatial query to find points within 5 miles
    points = gdf[gdf.geometry.within(buffered_target_point.unary_union)]

    return points

# print(loc(df1, 59.706024, 30.775085))
# df1Filt = loc(df1, 31.7683, 35.2137, 3) #buffer of 1 will be within 69 miles of jerusalem
# df1Filt = loc(df1, 48.3794, 32.5000,15)

# df2Filt = loc(df2, 31.7683, 35.2137, 1) #buffer of 1 will be within 69 miles of jerusalem

def plotAirplanes(df, map):
    area = gpd.read_file(map)
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    fig, ax = plt.subplots(figsize=(10, 10))
    area.plot(ax=ax, facecolor='none', edgecolor='black')
    gdf.plot(ax=ax, color='red', markersize=10, label='Points')
    plt.title('Noon, May 1, 2022')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plt.legend()

    # plt.savefig('22MAY01_WED1200_10sec')

    plt.show()


# plotAirplanes(df1Filt , 'ukraine-detailed-boundary_1059.geojson', )

# plotAirplanes(df1Filt , 'israel-detailed-boundary_942.geojson', )
# plotAirplanes(df2Filt , 'israel-detailed-boundary_942.geojson', )



'''example with specified range'''

def plotAirplaneRange(df, map, min_lon, max_lon, min_lat, max_lat):
    area = gpd.read_file(map)
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    filtered_points = gdf[
        (gdf['lon'] >= min_lon) & (gdf['lon'] <= max_lon) &
        (gdf['lat'] >= min_lat) & (gdf['lat'] <= max_lat)
    ]

    fig, ax = plt.subplots(figsize=(10, 10))
    area.plot(ax=ax, facecolor='none', edgecolor='black')
    filtered_points.plot(ax=ax, color='red', markersize=10, label='Points')
    plt.title('Map with Points Overlay')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plt.legend()

    plt.show()


def findAirNum(df, min_lon, max_lon, min_lat, max_lat):
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    filtered_points = gdf[
        (gdf['lon'] >= min_lon) & (gdf['lon'] <= max_lon) &
        (gdf['lat'] >= min_lat) & (gdf['lat'] <= max_lat)
    ]

    return (len(filtered_points))
    # return airNum

res = {}
for i in range(7):
    df = impala.history(start = int("16" + str(2+i) + "1812000"), stop = int("16" + str(2+i) + "1812002"))
    res[str(df.iloc[0].time)[:10]] = findAirNum(df, 22.0000, 41.0000, 44.0000, 53.0000)

print(res)
df = pd.DataFrame(res)

print(df)