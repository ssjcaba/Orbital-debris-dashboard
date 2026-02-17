import folium 
import pandas as pd

def create_map(data):
    m = folium.Map(location=[0,0])
    for index, row in data.iterrows(): 
        folium.Marker(
            location=[row['lat'],row['lon'],
            ] 
            ).add_to(m) 
    return m