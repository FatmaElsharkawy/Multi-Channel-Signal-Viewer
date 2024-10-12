import pyedflib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm

# Load the EDF file
edf_file_path = "non-rec.edf"
edf = pyedflib.EdfReader(edf_file_path)

# Get information about the file
num_signals = edf.signals_in_file
signal_labels = edf.getSignalLabels()

# Read the signals with a progress bar
signals = []
for i in tqdm(range(num_signals), desc="Reading Signals"):
    signals.append(edf.readSignal(i))

# Convert signals to a numpy array for easier manipulation
signals = np.array(signals)

# Close the EDF file
edf.close()


# Ensure there are signals to plot
if num_signals == 0:
    print("No signals found in the EDF file.")
    exit()

# Function to normalize a signal
def normalize_signal(signal):
    min_val = np.min(signal)
    max_val = np.max(signal)
    return (signal - min_val) / (max_val - min_val)  # Normalize to [0, 1]

# Function to plot the first signal

# Function for cine mode in polar graph where the signal "wraps around" and completes
def cine_mode_polar(signal, label="Signal", window_size=1000, interval=100):
    theta = np.linspace(0, 2 * np.pi, len(signal))  # Polar angle for the whole signal
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    line, = ax.plot([], [], lw=2)
    ax.set_title(f"Cine Mode Polar: {label}")
    
    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        end = (frame + 1) * window_size // 10
        if end > len(signal):
            end = len(signal)
        line.set_data(theta[:end], signal[:end])
        return line,

    ani = FuncAnimation(fig, update, frames=range(len(signal) // (window_size // 10)), init_func=init, blit=True, interval=interval)
    plt.show()

# Select the default signal "Abdomin1"
try:
    signal_index = signal_labels.index('Abdomen_1')
except ValueError:
    print("'Abdomien_1' signal not found in the file.")
    exit()

selected_signal = signals[signal_index]

# Automatically normalize the signal
normalized_signal = normalize_signal(selected_signal)


# Display cine mode for the normalized signal with fixed window size and interval
cine_mode_polar(normalized_signal, label=signal_labels[signal_index])
