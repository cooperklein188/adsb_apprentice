from pyopensky.impala import Impala
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

#opening the Impala shell
impala = Impala()

'''example query to find a specific airport'''
# df1 = impala.history(start = 1606842000, stop = 1606842005, airport= "LLBG")

'''query to find all flights in a timeframe (2 seconds)'''
df1 = impala.history(start = 1493632800, stop = 1493632802)

'''function that takes coordinate bounds (latitude, longitude and a radius from this point) and creates a GeoDataFrame with the points in the respective time'''
def loc(df, lat, lon, radius):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))

    # Create a GeoSeries with the target point
    target_point = gpd.GeoSeries([Point(lon, lat)], crs=gdf.crs)
    buffered_target_point = target_point.buffer(radius)  # 1 degree of latitude is approximately 69 miles
    # Use spatial query to find points within 5 miles
    points = gdf[gdf.geometry.within(buffered_target_point.unary_union)]

    return points

'''function will take a dataframe with points and a map, it will return the points on the map. If the map is too small, the plot will expand to show points outside the map'''
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


'''This function does the same as the loc function. However, the loc function returned points within a radius of a coordinate while this returns points within the boxed limits of latitude and longitude'''

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

'''This function finds the specific number of points within the respective region at a given time'''
def findAirNum(df, min_lon, max_lon, min_lat, max_lat):
    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    filtered_points = gdf[
        (gdf['lon'] >= min_lon) & (gdf['lon'] <= max_lon) &
        (gdf['lat'] >= min_lat) & (gdf['lat'] <= max_lat)
    ]

    return (len(filtered_points))
    # return airNum

#example of finding points and returning map on map of Ukraine
df1Filt = loc(df1, 48.3794, 32.5000,15)
plotAirplanes(df1Filt , 'ukraine-detailed-boundary_1059.geojson', )


#example of compiling points to make a histogram
res = {}
for i in range(7):
    df = impala.history(start = int("16" + str(2+i) + "1812000"), stop = int("16" + str(2+i) + "1812002"))
    res[str(df.iloc[0].time)[:10]] = findAirNum(df, 22.0000, 41.0000, 44.0000, 53.0000)

print(res)
df = pd.DataFrame(res)

print(df)