import numpy as np
from scipy import interpolate
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import sys
from pykalman import KalmanFilter  # Kalman filter implementation


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
    
    def open_glued_signal_window(glued_signal):
        """Open a new window to display the glued signal."""
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
        signal_window.show()


