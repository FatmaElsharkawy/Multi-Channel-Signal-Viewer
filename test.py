import numpy as np
from scipy import interpolate
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore  # Ensure QtCore is imported
import sys
import matplotlib.pyplot as plt

class SignalGlue(QtWidgets.QApplication):
    def __init__(self, signal_x, signal_y):
        self.signal_x = signal_x
        self.signal_y = signal_y

    def glue_signals(self, params):
        # Extract the window and glue parameters
        start_x, size_x = params.get("start_x"), params.get("size_x")
        start_y, size_y = params.get("start_y"), params.get("size_y")
        gap = params.get("gap", 0)

        # Validate that start and size are not None
        if start_x is None or size_x is None or start_y is None or size_y is None:
            raise ValueError("Start and size parameters must be provided and cannot be None.")

        if start_x + size_x > len(self.signal_x) or start_y + size_y > len(self.signal_y):
            raise ValueError("Start and size values exceed signal length.")

        # Cut the relevant parts of the signals
        part_x = self.signal_x[start_x:start_x + size_x]
        part_y = self.signal_y[start_y:start_y + size_y]

        # Create combined signal with the specified gap
        combined_signal = np.concatenate((part_x, np.zeros(gap), part_y))

        return combined_signal

def open_combined_window(start_x, size_x, start_y, size_y, gap):
    combined_window = QtWidgets.QWidget()
    combined_layout = QtWidgets.QVBoxLayout()

    # Create the plot for the combined signals
    plot_widget = pg.PlotWidget(title="Combined Signals")
    plot_widget.setXRange(0, (size_x + gap + size_y), padding=0)  # Set x range based on sizes and gap
    plot_widget.setYRange(-1.5, 1.5, padding=0)  # Set y range

    # Create the combined signal
    glue_params = {
        "start_x": start_x,
        "size_x": size_x,
        "start_y": start_y,
        "size_y": size_y,
        "gap": gap,
    }
    combined_signal = glue.glue_signals(glue_params)

    # Plot the combined signal
    plot_widget.plot(combined_signal, pen='purple', name='Combined Signal')

    # Add button to plot the combined signal
    combined_layout.addWidget(plot_widget)
    combined_window.setLayout(combined_layout)
    combined_window.setWindowTitle("Combined Signals")
    combined_window.resize(800, 600)
    combined_window.show()

    # Ensure the window stays open until closed by the user
    combined_window.setAttribute(QtWidgets.Qt.WA_QuitOnClose, False)

    # Store a reference to the combined window to keep it open
    app.combined_window = combined_window

    return combined_window  # Return the window reference

# PyQt application setup
app = QtWidgets.QApplication(sys.argv)

# Example signals
signal1 = np.sin(np.linspace(0, 2 * np.pi, 500))  # Sine wave
signal2 = np.cos(np.linspace(0, 2 * np.pi, 500))  # Cosine wave

# Create an instance of the SignalGlue class
glue = SignalGlue(signal1, signal2)

# Create the main window
main_window = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()

# Create the plot for the sine wave
plot_widget_x = pg.PlotWidget(title="Signal 1: Sine Wave")
plot_widget_x.plot(signal1, pen='b')

# Create the plot for the cosine wave
plot_widget_y = pg.PlotWidget(title="Signal 2: Cosine Wave")
plot_widget_y.plot(signal2, pen='r')

# Add draggable regions for selection
lr_x = pg.LinearRegionItem([100, 200], movable=True, brush=pg.mkBrush(150, 150, 150, 100))  # Movable sine part
plot_widget_x.addItem(lr_x)

lr_y = pg.LinearRegionItem([150, 250], movable=True, brush=pg.mkBrush(150, 50, 150, 100))  # Movable cosine part
plot_widget_y.addItem(lr_y)

# Add a gap input for user to specify the gap between signals
gap_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
gap_slider.setRange(0, 100)  # Set range for the gap
gap_slider.setValue(20)  # Set a default value for the gap
gap_label = QtWidgets.QLabel("Gap: 20 samples")

def update_gap_label(value):
    gap_label.setText(f"Gap: {value} samples")

gap_slider.valueChanged.connect(update_gap_label)

layout.addWidget(plot_widget_x)
layout.addWidget(plot_widget_y)
layout.addWidget(gap_label)
layout.addWidget(gap_slider)

# Button to open combined window
combine_button = QtWidgets.QPushButton("Combine Selected Signals")
combine_button.clicked.connect(lambda: open_combined_window(
    int(lr_x.getRegion()[0]),
    int(lr_x.getRegion()[1] - lr_x.getRegion()[0]),
    int(lr_y.getRegion()[0]),
    int(lr_y.getRegion()[1] - lr_y.getRegion()[0]),
    gap_slider.value()  # Get gap value from the slider
))

layout.addWidget(combine_button)

main_window.setLayout(layout)
main_window.setWindowTitle("Signal Selection")
main_window.resize(800, 600)
main_window.show()

# Start the Qt event loop
sys.exit(app.exec_())

 



























