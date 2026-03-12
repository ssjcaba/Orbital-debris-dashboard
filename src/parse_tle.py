from skyfield.api import load, EarthSatellite, wgs84
import numpy as np
import pandas as pd
import requests

def load_tle_records(source):
    # If source starts with http, it's a URL; otherwise, it's a file
    if source.startswith('http'):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Add a timeout so it doesn't hang forever
        response = requests.get(source, headers=headers, timeout=10)
        data = response.text.splitlines(
        response = requests.get(source)
        data = response.text.splitlines()
    else:
        with open(source, 'r') as f:
            data = f.readlines()
            
    # Your existing logic to group lines into 3s goes here...
    records = []
    for i in range(0, len(data) - 2, 3):
        records.append((data[i].strip(), data[i+1].strip(), data[i+2].strip()))
    return records


def compute_positions(records, ts, time):
    """From TLE records, timescale, and times, return a list of snapshot dicts."""
    collection = []
    
    # Figure out if 'time' is an array or a single time object
    try:
        num_times = len(time)
        is_array = True
    except TypeError:
        num_times = 1
        is_array = False

    for name, line1, line2 in records:
        satellite = EarthSatellite(line1, line2, name, ts)
        geocentric = satellite.at(time)
        subpoint = wgs84.subpoint(geocentric)
        
        # New: Get the X, Y, Z coordinates in kilometers
        pos_km = geocentric.position.km
        
        lat = subpoint.latitude.degrees
        lon = subpoint.longitude.degrees
        alt = subpoint.elevation.km
        
        if is_array:
            # Handle multiple times (e.g., a path)
            for j in range(num_times):
                snapshot = {
                    "name": name,
                    "time": time[j].utc_iso(),
                    "lat": lat[j],
                    "lon": lon[j],
                    "alt_km": alt[j],
                    # Extracting specific j-index for arrays
                    "x": pos_km[0][j],
                    "y": pos_km[1][j],
                    "z": pos_km[2][j],
                }
                collection.append(snapshot)
        else:
            # Handle a single time (e.g., a current snapshot)
            snapshot = {
                "name": name,
                "time": time.utc_iso(),
                "lat": lat,
                "lon": lon,
                "alt_km": alt,
                # Simple extraction for single time
                "x": pos_km[0],
                "y": pos_km[1],
                "z": pos_km[2],
            }
            collection.append(snapshot)
            
    return collection


