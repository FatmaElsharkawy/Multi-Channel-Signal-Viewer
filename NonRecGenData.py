import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button

# Step 1: Initialize parameters for the radar signal
num_targets = 100  # Number of targets
radii = np.random.rand(num_targets) * 10  # Initial distances of targets
angles = np.random.rand(num_targets) * 2 * np.pi  # Initial angles of targets

# Function to update target positions
def update_positions(radii, angles):
    # Update angles and radii to simulate movement
    angles += np.random.uniform(-0.1, 0.1, num_targets)  # Slightly randomize angles
    radii += np.random.uniform(-0.1, 0.1, num_targets)  # Slightly randomize radii (within bounds)
    radii = np.clip(radii, 0, 10)  # Ensure radii stay within bounds (0 to 10)
    return radii, angles

# Stop flag
stop_animation = False

# Stop button callback function
def stop(event):
    global stop_animation
    stop_animation = True

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_ylim(0, 10)

# Add a stop button
stop_ax = plt.axes([0.8, 0.9, 0.1, 0.05])  # Position: [left, bottom, width, height]
stop_button = Button(stop_ax, 'Stop')
stop_button.on_clicked(stop)

# Animation loop
for _ in range(100):  # Number of frames
    if stop_animation:  # Check if stop button was clicked
        break

    ax.clear()  # Clear the previous frame
    ax.set_ylim(0, 10)  # Reset limits

    # Update target positions
    radii, angles = update_positions(radii, angles)

    # Plot points (targets)
    ax.scatter(angles, radii, c='red', s=10, label="Targets")
    plt.title("Moving Radar Signal Simulation")
    plt.legend()

    # Pause to create animation effect
    plt.pause(0.1)  # Pause for 100 ms

# Turn off interactive mode
plt.ioff()
plt.show()
