from skyfield.api import load, EarthSatellite, wgs84
import numpy as np
import pandas as pd

def load_tle_records(filepath):
    """Read a TLE file and return a list of (name, line1, line2) per satellite."""
    with open(filepath, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]

    if len(lines) < 2:
        raise ValueError("TLE file does not contain enough lines")

    result = []
    i = 0
    while i + 2 <= len(lines):
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]
        result.append((name, line1, line2))
        i += 3
    return result


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


