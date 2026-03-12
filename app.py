import streamlit as st
import pandas as pd
from skyfield.api import load
from streamlit_folium import st_folium
from src.risk import find_risks
from src.parse_tle import load_tle_records, compute_positions
from src.map import create_map

st.set_page_config(page_title="Orbital Tracker", layout="wide")
st.title("Orbital Debris Tracker")

@st.cache_data
def get_satellite_data():
    ts = load.timescale()
    t = ts.now()
    records = load_tle_records("data/tle_raw.txt")
    results = compute_positions(records, ts, t)
    return pd.DataFrame(results)

# 1. DATA
df = get_satellite_data()

# 2. DIAGNOSTIC BONE (Look at the X, Y, Z columns here!)
st.subheader("Data Preview")
st.write(df.head())

# 3. SETTINGS
with st.sidebar:
    st.header("⚙️ Settings")
    limit = st.slider("Collision Threshold (km)", 10, 5000, 700)
    st.divider()

# 4. EXECUTION
danger = find_risks(df, limit)
my_map = create_map(df) 

# 5. DISPLAY
st_folium(my_map, width=900, height=500, key="orbital_map")

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