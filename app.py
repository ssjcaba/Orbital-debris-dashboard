import streamlit as st
import folium
import pandas as pd
from skyfield.api import load
from streamlit_folium import st_folium
from src.risk import find_risks

# Import your custom functions
from src.parse_tle import load_tle_records, compute_positions
from src.map import create_map

# 1. SETUP: Header of website
st.title("Orbital Debris Tracker")
st.write("Pulls live satellite data from NASA and other agencies, tracks satellites and shows them on interactive maps.")

# 2. CACHING: This stops the flashing by "remembering" the data
@st.cache_data
def get_satellite_data():
    ts = load.timescale()
    t = ts.now()
    # Loading and computing
    records = load_tle_records("data/tle_raw.txt")
    results = compute_positions(records, ts, t)
    return pd.DataFrame(results)

# 3. EXECUTION: Get the data and build the map
df = get_satellite_data()
danger = find_risks(df)
my_map = create_map(df) 

# 4. DISPLAY: Added a 'key' here to tell Streamlit not to refresh the component
st_folium(my_map, width=700, height=500, key="orbital_map")



st.title("Risk of Collision")

with st.sidebar:
    st.header("🛰️ Collision Alerts")
    
    if len(danger) > 0:
        st.warning(f"Found {len(danger)} risks")
        
        for risk in danger:
            st.write(f"**{risk['satellite_1']}** vs **{risk['satellite_2']}**")
            st.write(f"Distance: {risk['distance']} km")
            st.divider() 
            
    else:
        st.success("All clear! No risks found.")