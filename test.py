# import csv
# with open('rec_1r.csv', mode ='r')as file:
#   csvFile = csv.reader(file)
#   for lines in csvFile:
#         print(lines)

# import csv
# with open('rec_1r.csv', mode ='r') as file:    
#        csvFile = csv.DictReader(file)
#        for lines in csvFile:
#             print(lines)


# import pandas as pd
# csvFile = pd.read_csv('rec_1r.csv')
# first_column = csvFile.iloc[:, 0].values
# second_column = csvFile.iloc[:, 1].values

# # Print the arrays
# print("First Column:", first_column)
# print("Second Column:", second_column)
# #print("Second Column:", type(second_column))


import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

class SignalGlue:
    def __init__(self, signal_x, signal_y):
        self.signal_x = signal_x
        self.signal_y = signal_y

    def glue_signals(self, params):
        # Extract the window and glue parameters
        start_x, size_x = params.get("start_x"), params.get("size_x")
        start_y, size_y = params.get("start_y"), params.get("size_y")
        gap = params.get("gap", 0)
        interpolation_order = params.get("interpolation_order", "linear")

        # Validate that start and size are not None
        if start_x is None or size_x is None or start_y is None or size_y is None:
            raise ValueError("Start and size parameters must be provided and cannot be None.")

        if start_x + size_x > len(self.signal_x) or start_y + size_y > len(self.signal_y):
            raise ValueError("Start and size values exceed signal length.")

        # Cut the relevant parts of the signals
        part_x = self.signal_x[start_x:start_x + size_x]
        part_y = self.signal_y[start_y:start_y + size_y]

        # Create a gap (positive distance) or overlap (negative distance)
        if gap > 0:
            estimated_gap = self.spline_interpolate(part_x, part_y, gap)
            combined_signal = np.concatenate((part_x, estimated_gap, part_y))
        else:
            overlap_length = min(abs(gap), min(len(part_x), len(part_y)))
            overlap_x = part_x[-overlap_length:]
            overlap_y = part_y[:overlap_length]
            interpolated_overlap = self.interpolate_signal(overlap_x, overlap_y, interpolation_order)

            combined_signal = np.concatenate((part_x[:-overlap_length], interpolated_overlap, part_y[overlap_length:]))

        return combined_signal

    def interpolate_signal(self, signal_x, signal_y, method):
        x = np.linspace(0, len(signal_x) - 1, len(signal_x))

        # Perform interpolation
        interpolator = interpolate.interp1d(x, signal_y, kind=method, fill_value="extrapolate")
        interpolated_signal = interpolator(x)

        combined_signal = (signal_x + interpolated_signal) / 2

        return combined_signal
    
    def spline_interpolate(self, part_x, part_y, gap):
        # Create new x positions for the gap
        gap_x = np.linspace(0, gap + len(part_x) - 1, gap)
        
        # Combine the known signals
        combined_x = np.concatenate((part_x, part_y))
        combined_y = np.concatenate((part_x[-1:], part_y[:1]))  # Use the last of part_x and first of part_y

        # Create spline interpolator
        spline = interpolate.CubicSpline(np.arange(len(combined_x)), combined_x)
        
        # Interpolate the gap
        gap_signal = spline(np.arange(len(part_x), len(part_x) + gap))
        
        return gap_signal

# Test SignalGlue
# Example signals
signal1 = np.sin(np.linspace(0, 2 * np.pi, 500))
signal2 = np.cos(np.linspace(0, 2 * np.pi, 500))

# Glue the signals with custom parameters
glue = SignalGlue(signal1, signal2)
glue_params = {
    "start_x": 100,  # Start index for the first signal
    "size_x": 200,   # Size of the segment to extract from the first signal
    "start_y": 50,   # Start index for the second signal
    "size_y": 200,   # Size of the segment to extract from the second signal
    "gap": 100,      # Gap of 100 points
    "interpolation_order": "linear"
}
combined_signal = glue.glue_signals(glue_params)

# Plot original signals with start and size lines
for idx, (signal, title, start, size) in enumerate(zip(
        [signal1, signal2],
        ["Signal 1: Sine Wave", "Signal 2: Cosine Wave"],
        [glue_params["start_x"], glue_params["start_y"]],
        [glue_params["size_x"], glue_params["size_y"]]
    )):
    plt.figure(figsize=(6, 4))
    plt.plot(signal)
    plt.title(title)

    # Add vertical line for start point
    plt.axvline(x=start, color='r', linestyle='--', label='Start Point')

    # Add vertical line for end point (start + size)
    plt.axvline(x=start + size, color='g', linestyle='--', label='End Point (Start + Size)')

    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()

# Generate a plot for the glued signal and save it
plt.plot(combined_signal)
plt.title("Glued Signal")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.savefig("glued_signal.png")
plt.show()
