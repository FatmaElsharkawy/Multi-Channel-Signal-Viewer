import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer
from threading import Thread

class NonRectangularPlot:
    def __init__(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='polar')
        self.num_targets = 100
        self.radii = np.random.rand(self.num_targets) * 10
        self.angles = np.random.rand(self.num_targets) * 2 * np.pi
        self._animating = False  # Flag to control the animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot)

    def update_positions(self):
        self.angles += np.random.uniform(-0.1, 0.1, self.num_targets)
        self.radii += np.random.uniform(-0.1, 0.1, self.num_targets)
        self.radii = np.clip(self.radii, 0, 10)
        return self.angles, self.radii

    def plot(self):
        if not self._animating:
            return

        self.ax.clear()
        self.ax.set_ylim(0, 10)
        angles, radii = self.update_positions()
        self.ax.scatter(angles, radii, c='red', s=10)
        self.canvas.draw_idle()

    def start(self):
        self._animating = True
        self.timer.start(100)  # Update every 100 ms

    def stop(self):
        self._animating = False
        self.timer.stop()
