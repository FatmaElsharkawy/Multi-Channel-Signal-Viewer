import numpy as np
from scipy import interpolate
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import sys
from pykalman import KalmanFilter  # Kalman filter implementation
from ReportGenerator import ReportGenerator  # Import the ReportGenerator class from the ReportGenerator.py file

class SignalGlue:
    def __init__(self, signal_x, signal_y):
        self.signal_x = signal_x
        self.signal_y = signal_y

    def apply_kalman_filter(self, signal):
        """Apply a Kalman filter to smooth the given signal."""
        kf = KalmanFilter(initial_state_mean=signal[0], n_dim_obs=1)
        state_means, _ = kf.smooth(signal)
        return state_means.flatten()

    def interpolate_signal(self, x, y, method='linear'):
        """Interpolate the given signals using the specified method."""
        interp_func = interpolate.interp1d(x, y, kind=method, fill_value="extrapolate")
        new_x = np.linspace(x[0], x[-1], num=len(y))
        return interp_func(new_x)

    def glue_signals(self, part_x, part_y, gap):
        if gap > 0:
            overlap_size = abs(gap)
            part_x_overlap = part_x[-overlap_size:]
            part_y_overlap = part_y[:overlap_size]

            combined_overlap = (part_x_overlap + part_y_overlap) / 2
            smoothed_overlap = self.apply_kalman_filter(combined_overlap)

            combined_signal = np.concatenate((
                part_x[:-overlap_size],
                smoothed_overlap,
                part_y[overlap_size:]
            ))
        else:
            overlap_length = min(abs(gap), min(len(part_x), len(part_y)))
            overlap_x = part_x[-overlap_length:]
            overlap_y = part_y[:overlap_length]
            interpolated_overlap = self.interpolate_signal(overlap_x, overlap_y, "linear")

            combined_signal = np.concatenate((part_x[:-overlap_length], interpolated_overlap, part_y[overlap_length:]))

        return combined_signal


import pyqtgraph.exporters  # For exporting the plot as an image

def open_glued_signal_window(glued_signal):
    """Open a new window to display the glued signal and generate a report."""
    print("Opening window to display the glued signal.")
    # Create a new window for the glued signal
    signal_window = QtWidgets.QWidget()
    signal_layout = QtWidgets.QVBoxLayout()

    # Create the plot widget for the glued signal
    plot_glued = pg.PlotWidget(title="Glued Signal")
    signal_layout.addWidget(plot_glued)

    # Ensure glued_signal is not empty before plotting
    if glued_signal.size > 0:
        # Plot the glued signal
        plot_glued.plot(glued_signal, pen='g', name="Glued Signal")
    else:
        print("Glued signal is empty, nothing to plot.")

    # Set the layout and properties of the signal window
    signal_window.setLayout(signal_layout)
    signal_window.setWindowTitle("Glued Signal Window")
    signal_window.resize(800, 600)

    # Keep a reference to avoid garbage collection
    app.signal_window = signal_window

    # ---- Create Buttons ----
    # Button to generate the report
    generate_report_button = QtWidgets.QPushButton("Generate Report")
    signal_layout.addWidget(generate_report_button)

    # Button to add another image to the report
    add_image_button = QtWidgets.QPushButton("Add Another Image")
    #signal_layout.addWidget(add_image_button)

    # Create an instance of the ReportGenerator class outside the functions
    report_gen = ReportGenerator()

    # ---- Report Generation Logic ----
    def generate_report():
        try:
            # Calculate statistics on the glued signal
            report_gen.calculate_statistics(glued_signal)

            # Save a snapshot of the plot as an image
            exporter = pg.exporters.ImageExporter(plot_glued.plotItem)
            exporter.export('glued_signal.png')  # Save the initial image

            # Add the snapshot to the report
            report_gen.add_snapshot("glued_signal.png")

            # Generate the PDF report
            report_gen.generate_report("signal_report.pdf")
            print("Report generated successfully: signal_report.pdf")

        except Exception as e:
            print(f"Error generating report: {e}")

    # Connect the generate report button to the function
    generate_report_button.clicked.connect(generate_report)

    # ---- Add Another Image Logic ----
    def add_another_image():
        try:
            # Save a new screenshot of the current plot
            new_image_file = 'glued_signal_additional.png'
            exporter = pg.exporters.ImageExporter(plot_glued.plotItem)
            exporter.export(new_image_file)  # Save the current image

            # Add the newly saved image to the report
            report_gen.add_snapshot(new_image_file)
            print(f"Added additional image to report: {new_image_file}")

        except Exception as e:
            print(f"Error adding image to report: {e}")

    # Connect the add image button to the function
    add_image_button.clicked.connect(add_another_image)

    # Show the window
    signal_window.show()

    return signal_window






def open_combined_window(start_x, size_x, start_y, size_y, gap):
    combined_window = QtWidgets.QWidget()
    combined_layout = QtWidgets.QVBoxLayout()

    # Create the plot widget for both parts (signal_x and signal_y)
    plot_widget = pg.PlotWidget(title="Part X and Part Y: Same Graph")
    combined_layout.addWidget(plot_widget)

    # Cut the relevant parts of the signals
    part_x = glue.signal_x[start_x:start_x + size_x]
    part_y = glue.signal_y[start_y:start_y + size_y]

    # Create a plot for the glued signals
    plot_combined = plot_widget.plot(part_x, pen='b', name="Part X: Fixed")
    plot_movable = plot_widget.plot(np.arange(size_x + gap, size_x + gap + size_y), part_y, pen='r', name="Part Y: Movable")

    # Add a gap slider for the user to specify the gap between signals
    gap_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    gap_slider.setRange(-50, 100)  # Set range for the gap to allow negative values for overlap
    gap_slider.setValue(gap)  # Set a default value for the gap
    gap_label = QtWidgets.QLabel(f"Gap: {gap} samples")

    def update_gap_label(value):
        gap_label.setText(f"Gap: {value} samples")

    gap_slider.valueChanged.connect(update_gap_label)

    def update_movable_signal(gap_value):
        # Calculate the new starting x-coordinate for signal_y based on the gap value
        new_x = np.arange(size_x + gap_value, size_x + gap_value + size_y)
        plot_movable.setData(new_x, part_y)

    gap_slider.valueChanged.connect(update_movable_signal)

    # Button to create and show the glued signal
    create_glued_button = QtWidgets.QPushButton("Create and Show Glued Signal")

    def show_glued_signal():
        print("Create and Show Glued Signal button clicked.")
        try:
            # Calculate the glued signal based on the current gap
            glued_signal = glue.glue_signals(part_x, part_y, gap_slider.value())
            print("Glued signal calculated successfully.")

            # Open the window to display the glued signal
            open_glued_signal_window(glued_signal)
        except Exception as e:
            print(f"Error in gluing signals: {e}")



    create_glued_button.clicked.connect(show_glued_signal)

    combined_layout.addWidget(gap_label)
    combined_layout.addWidget(gap_slider)
    combined_layout.addWidget(create_glued_button)  # Add the button to the layout

    combined_window.setLayout(combined_layout)
    combined_window.setWindowTitle("Adjust Gap and Glue Signals")
    combined_window.resize(800, 600)
    combined_window.show()

    # Keep a reference to prevent the window from closing
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

# Button to open combined window
combine_button = QtWidgets.QPushButton("Combine and Adjust Gap")
combine_button.clicked.connect(lambda: open_combined_window(
    int(lr_x.getRegion()[0]),
    int(lr_x.getRegion()[1] - lr_x.getRegion()[0]),
    int(lr_y.getRegion()[0]),
    int(lr_y.getRegion()[1] - lr_y.getRegion()[0]),
    gap=20  # Set a default gap value
))

layout.addWidget(plot_widget_x)
layout.addWidget(plot_widget_y)
layout.addWidget(combine_button)

main_window.setLayout(layout)
main_window.setWindowTitle("Signal Selection")
main_window.resize(800, 600)
main_window.show()

# Start the Qt event loop
sys.exit(app.exec_())
