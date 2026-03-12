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
    # Live URL for Active Satellites
    url = "active.txt"
    records = load_tle_records(url)
    results = compute_positions(records, ts, t)
    return pd.DataFrame(results)

# 1. DATA
df = get_satellite_data()

# 2. SETTINGS
with st.sidebar:
    st.header("⚙️ Settings")
    limit = st.slider("Collision Threshold (km)", 10, 5000, 700)
    st.divider()

# 3. EXECUTION
# We take a slice (first 400) so the map doesn't crash your browser
df_limited = df.head(25) 

danger = find_risks(df_limited, limit)

# IMPORTANT: You need to pass 'danger' here so the dots turn red!
my_map = create_map(df_limited, danger) 

# 4. DISPLAY
# Move the table into an expander so the map can actually show up
with st.expander("📊 View Raw Satellite Data"):
    st.write(df_limited)

st.subheader("🛰️ Live Orbital Map")
st_folium(my_map, width=1000, height=600, key="orbital_map")

with st.sidebar:
    st.header("🛰️ Collision Alerts")
    if len(danger) > 0:
        st.warning(f"Found {len(danger)} risks")
        for risk in danger:
            st.write(f"**{risk['satellite_1']}** vs **{risk['satellite_2']}**")
            # Using standard text instead of LaTeX for distance
            st.write(f"Distance: {risk['distance']} km")
            st.divider() 
    else:
        st.success("All clear! No risks found.")
