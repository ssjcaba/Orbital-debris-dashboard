import folium 
import pandas as pd
from src.parse_tle import compute_positions, load_tle_records
from skyfield.api import load 

def create_map(data, danger_list):
    m = folium.Map(location=[0,0], tiles="CartoDB dark_matter")
    
    # Create a simple set of names that are in danger for fast lookup
    danger_names = set()
    for d in danger_list:
        danger_names.add(d['satellite_1'])
        danger_names.add(d['satellite_2'])

    for index, row in data.iterrows():
        # THE LOGIC: If the satellite is in our danger set, make it RED.
        # Otherwise, make it CYAN (or blue).
        if row['name'] in danger_names:
            dot_color = "red"
            dot_radius = 5  # Make it slightly bigger to stand out
        else:
            dot_color = "cyan"
            dot_radius = 2

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=dot_radius,
            color=dot_color,
            fill=True,
            popup=row['name']
        ).add_to(m)
        
    return m



if __name__ == "__main__":
    ts = load.timescale()
    t = ts.now()
    
    records = load_tle_records("data/tle_raw.txt")
    
    raw_results = compute_positions(records, ts, t) 
    
    data = pd.DataFrame(raw_results)
    
    my_map = create_map(data)
    my_map.save("satellite_viewer.html")
    print(f"Success! Mapped {len(data)} satellites.")