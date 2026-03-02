#Step 1: Convert sastellite positions into geocentric coordinates
import math

def calc_distance(row1, row2):
        dx = row1['x'] - row2['x']
        dy = row1['y'] - row2['y']
        dz = row1['z'] - row2['z']

        dist = math.sqrt(dx**2 + dy**2 + dz**2)

