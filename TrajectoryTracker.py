import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os
import sys
# Initialize variables
vSummary = []
aSummary = []
Summary = []
window_sizev = 800
window_sizea= 50


# Get the passed CSV path
#csv_path = "/Users/mollykirk/Desktop/Behavioral test data /Seltzer 1 Post.mp4_output.csv"
csv_path = sys.argv[1]
print(f"Received CSV csv_path: {csv_path}")

# Get the parent folder name
data = pd.read_csv(csv_path, skiprows=2)

# Pull columns from the data
time = data.iloc[:, 1].values  # Time (second column)
x_center = data.iloc[:, 2].values  # X center (third column)
y_center = data.iloc[:, 3].values  # Y center (fourth column)
length = data.iloc[:, 4].values
area = data.iloc[:, 5].values
headx = data.iloc[:, 6].values
heady = data.iloc[:, 7].values
tailx = data.iloc[:, 8].values
taily = data.iloc[:, 9].values
curve_length = data.iloc[:, 10].values

# Calculate velocity
velocity = np.zeros(len(time))
for j in range(1, len(time)-1):
    deltaT = time[j] - time[j-1]
    deltaX = x_center[j] - x_center[j-1]
    deltaY = y_center[j] - y_center[j-1]
    velocity[j] = np.sqrt(deltaX**2 + deltaY**2) / deltaT

Avelocity = np.mean(velocity)
Svelocity = np.std(velocity)

# Calculate acceleration
acceleration = np.zeros(len(velocity))
for j in range(1, len(velocity)-1):
    deltaV = velocity[j] - velocity[j-1]
    deltaT = time[j] - time[j-1]
    acceleration[j] = deltaV / deltaT
    
# Smooth the velocity using a moving average
smoothed_velocity = np.zeros(len(velocity))
for l in range(len(velocity)):
    window_start = max(0, l - window_sizev + 1)
    window_end = l + 1
    window_values = velocity[window_start:window_end]
    smoothed_velocity[l] = np.mean(window_values)

# Smooth the acceleration using a moving average
smoothed_acceleration = np.zeros(len(acceleration))
for l in range(len(acceleration)):
    window_start = max(0, l - window_sizea + 1)
    window_end = l + 1
    window_values = acceleration[window_start:window_end]
    smoothed_acceleration[l] = np.mean(window_values)

# Plot the data
fig, axs = plt.subplots(2, 3, figsize=(15, 8))
axs[0, 0].plot(time[:-1], length[:-1])
axs[0, 0].set_title('Length')
axs[0, 0].set_xlabel('Time (Sec)')
axs[0, 0].set_ylabel('Pixels')
axs[0, 0].set_xlim(np.min(time[:-1]), np.max(time[:-1]))
axs[0, 0].set_ylim(np.min(length[:-1]), np.max(length[:-1]))

axs[0, 1].plot(time[:-1], area[:-1])
axs[0, 1].set_title('Area')
axs[0, 1].set_xlabel('Time (Sec)')
axs[0, 1].set_ylabel('Pixels^2')
axs[0, 1].set_xlim(np.min(time[:-1]), np.max(time[:-1]))
axs[0, 1].set_ylim(np.min(area[:-1]), np.max(area[:-1]))
    
axs[0, 2].plot(x_center[:-1], y_center[:-1])
axs[0, 2].set_title('Displacement')
axs[0, 2].set_xlabel('Pixels')
axs[0, 2].set_ylabel('Pixels')
axs[0, 2].set_xlim(np.min(x_center[:-1]), np.max(x_center[:-1]))
axs[0, 2].set_ylim(np.min(y_center[:-1]), np.max(y_center[:-1]))

axs[1, 0].plot(time[:-1], smoothed_velocity[:-1])
axs[1, 0].set_title('Velocity')
axs[1, 0].set_xlabel('Time (Sec)')
axs[1, 0].set_ylabel('Velocity (Pixels/Sec)')
axs[1, 0].set_xlim(np.min(time[:-1]), np.max(time[:-1]))
axs[1, 0].set_ylim(np.min(smoothed_velocity[:-1]), np.max(smoothed_velocity[:-1]))

axs[1, 1].plot(time[:-2], smoothed_acceleration[:-2])
axs[1, 1].set_title('Acceleration')
axs[1, 1].set_xlabel('Time(Sec)')
axs[1, 1].set_ylabel('Acceleration(Pixels/Sec^2)')
axs[1, 1].set_xlim(np.min(time[:-2]), np.max(time[:-2]))
axs[1, 1].set_ylim(np.min(smoothed_acceleration[:-2]), np.max(smoothed_acceleration[:-2]))

# Create line segments between consecutive (x, y) points
points = np.array([x_center[:-1], y_center[:-1]]).T
segments = np.stack([points[:-1], points[1:]], axis=1)

# Create a LineCollection with smoothed velocity-based coloring
lc = LineCollection(segments, cmap='jet', norm=plt.Normalize(np.min(smoothed_velocity[:-1]), np.max(smoothed_velocity[:-1])))
lc.set_array(smoothed_velocity[:-1])  # Use smoothed velocity for coloring
lc.set_linewidth(2)

# Add the LineCollection to the plot
axs[1, 2].add_collection(lc)
axs[1, 2].set_title('Path Colored by Smoothed Velocity')
axs[1, 2].set_xlabel('Pixels')
axs[1, 2].set_ylabel('Pixels')
axs[1, 2].set_xlim(np.min(x_center[:-1]), np.max(x_center[:-1]))
axs[1, 2].set_ylim(np.min(y_center[:-1]), np.max(y_center[:-1]))

# Add a colorbar for smoothed velocity
fig.colorbar(lc, ax=axs[1, 2], label='Smoothed Velocity (Pixels/Sec)')


plt.tight_layout()
save_path= os.path.splitext(csv_path)[0]
plt.savefig(save_path + '.png')  # Save the figure as PNG
# Create the full path with '.png' appended

