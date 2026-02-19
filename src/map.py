import folium 
import pandas as pd
from parse_tle import compute_positions, load_tle_records
from skyfield.api import load 

def create_map(data):
    m = folium.Map(location=[0,0])
    for index, row in data.iterrows(): 
        folium.Marker(
            location=[row['lat'],row['lon'],
            ], popup=row['name'] 
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