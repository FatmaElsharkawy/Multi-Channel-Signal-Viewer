import pyedflib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the EDF file
edf_file_path = "non-rec.edf"
edf = pyedflib.EdfReader(edf_file_path)

# Get information about the file
num_signals = edf.signals_in_file
signal_labels = edf.getSignalLabels()

# Read the signals
signals = []
for i in range(num_signals):
    signals.append(edf.readSignal(i))

# Convert signals to a numpy array for easier manipulation
signals = np.array(signals)

# Close the EDF file
edf.close()

# Display some information
print(f"Number of signals: {num_signals}")
print(f"Signal labels: {signal_labels}")

# Ensure there are signals to plot
if num_signals == 0:
    print("No signals found in the EDF file.")
    exit()

# Function to plot the first signal
def plot_signal(signal):
    plt.figure(figsize=(10, 5))
    plt.plot(signal)
    plt.title(signal_labels[0])
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

# Function to plot the polar graph
def plot_polar(signal):
    theta = np.linspace(0, 2 * np.pi, len(signal))  # Polar angle
    r = signal  # Radius corresponds to signal amplitude
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, projection='polar')
    ax.plot(theta, r)
    ax.set_title("Non-Rectangular (Polar) Graph")
    plt.show()

# Function to create a cine mode plot
def cine_mode(signal, window_size=1000, interval=100):
    fig, ax = plt.subplots(figsize=(10, 5))
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(0, window_size)
    ax.set_ylim(np.min(signal), np.max(signal))
    ax.set_title(f"Cine Mode: {signal_labels[0]}")
    ax.set_xlabel('Sample Number')
    ax.set_ylabel('Amplitude')
    
    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        start = frame * window_size // 10
        end = start + window_size
        if end > len(signal):
            end = len(signal)
            start = end - window_size
        if start < 0:
            start = 0
        line.set_data(np.arange(start, end), signal[start:end])
        return line,

    ani = FuncAnimation(fig, update, frames=range(len(signal) // (window_size // 10)), init_func=init, blit=True, interval=interval)
    plt.show()

# Call the plotting functions
plot_signal(signals[0])  # Plot the first signal
plot_polar(signals[0])   # Plot the polar graph
cine_mode(signals[0])     # Display cine mode for the first signal
