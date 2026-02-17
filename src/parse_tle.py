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
    """From TLE records, timescale, and times, return a list of snapshot dicts (name, time, lat, lon, alt_km)."""
    collection = []
    for name, line1, line2 in records:
        satellite = EarthSatellite(line1, line2, name, ts)
        geocentric = satellite.at(time)
        subpoint = wgs84.subpoint(geocentric)
        latitude = subpoint.latitude.degrees
        longitude = subpoint.longitude.degrees
        altitude = subpoint.elevation.km
        for j in range(len(time)):
            snapshot = {
                "name": name,
                "time": time[j].utc_iso(),
                "lat": latitude[j],
                "lon": longitude[j],
                "alt_km": altitude[j],
            }
            collection.append(snapshot)
    return collection


