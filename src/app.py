import streamlit as st
import folium
from src.parse_tle import load_tle_records, compute_positions
from map import create_map
from skyfield.api import load, EarthSatellite, wgs84
import pandas as pd

#header of website
title = st.title("Orbital Debris Tracker")
description = st.write("Pulls live satellite data from NASA and other agencies, tracks satellites and shows them on interactive maps. Spots when objects get too close and flags possible collision risks, turning complex space data into clear, easy to understand visuals")

#time we want to display our satellites at
ts = load.timescale()
t = ts.now()

#loaded and computed TLE records
records = load_tle_records("tle_raw.txt")
results = compute_positions(records, ts, t)

frame = pd.DataFrame(results)

create_map(frame) 