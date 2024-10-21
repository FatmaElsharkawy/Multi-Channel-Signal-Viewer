import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Button

# Load data
df = pd.read_csv("radar_data.csv", header=None, sep=',')  # Use sep=',' for comma-separated data

# Use only 10% of the data
df_sampled = df.sample(frac=0.1, random_state=1)  # Randomly sample 10% of the data
radii = df_sampled[0].values  # First column for distances (radii)
angles = df_sampled[1].values  # Second column for angles

# Function to update target positions
def update_positions(radii, angles):
    # Update angles and radii to simulate movement
    angles += np.random.uniform(-0.1, 0.1, len(radii))  # Slightly randomize angles
    radii += np.random.uniform(-0.1, 0.1, len(radii))  # Slightly randomize radii
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
for _ in range(30):  # Number of frames
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

    # Break the loop if stop button is clicked
    if stop_animation:
        break

# Turn off interactive mode
plt.ioff()
plt.show()
