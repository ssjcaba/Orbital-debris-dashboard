
import math

def calc_distance(row1, row2):
        dx = row1['x'] - row2['x']
        dy = row1['y'] - row2['y']
        dz = row1['z'] - row2['z']

        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        return dist

#Below is a function that takes my entire table 
# And compares every satellite to each other to find
#the danger zone pairs

def find_risks(df):
    risks = []
    for i in range(len(df)):

        for j in range(i + 1, len(df)):
            sat1 = df.iloc[i]
            sat2 = df.iloc[j]

            dist = calc_distance(sat1,sat2)
            if dist < 700:
                risks.append({
                    "satellite_1": sat1['name'],
                    "satellite_2": sat2['name'],
                    "distance": dist
                })
    return risks 

