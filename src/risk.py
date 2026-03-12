import numpy as np

def calc_distance(sat1, sat2):
    # Standard 3D distance formula
    pos1 = np.array([sat1['x'], sat1['y'], sat1['z']])
    pos2 = np.array([sat2['x'], sat2['y'], sat2['z']])
    dist = np.linalg.norm(pos1 - pos2)
    return dist

def find_risks(df, threshold):
    risks = []
    # Loop through the list to compare pairs
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            sat1 = df.iloc[i]
            sat2 = df.iloc[j]
            
            distance = calc_distance(sat1, sat2)
            
            if distance < threshold:
                risks.append({
                    "satellite_1": sat1['name'],
                    "satellite_2": sat2['name'],
                    "distance": round(distance, 2)
                })
    return risks

