from turtle import title
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import geopandas as gpd
import folium
import osmnx as ox
import networkx as nx
from shapely.geometry import Point

df = pd.read_csv('../preprocessing/00_data/data.csv')
df = df.drop('Unnamed: 0',axis=1)

geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
geo_df = gpd.GeoDataFrame(df, geometry=geometry)

#shp出力
geo_df.to_file(driver='ESRI Shapefile', filename='geo.shp', encoding='utf-8')

# shpをgeojsonに変換
df = gpd.read_file('geo.shp')
df.to_file('geo.geojson', driver='GeoJSON', encoding='utf-8')
