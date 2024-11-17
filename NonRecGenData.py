import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer

class NonRectangularPlot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, projection='polar')
        self.data = []
        self.times = []
        self.current_index = 0
        self._animating = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot)
        self.initUI()  # Initialize UI elements
        self.load_data()  # Load data from CSV
        self.setup_plot()  # Apply the initial styling

    def initUI(self):
        loadUi('NonRectangularUI.ui', self)
        self.setWindowTitle("NonRectangular Window")
        self.play_button = self.findChild(QPushButton, 'play')
        self.pause_button = self.findChild(QPushButton, 'pause')
        self.play_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.stop)
        self.nonrectangular_signal_view = self.findChild(QWidget, 'nonrectangular_signal_view')
        self.layout = QVBoxLayout(self.nonrectangular_signal_view)
        self.layout.addWidget(self.canvas)  # Add the canvas to the layout

    def load_data(self):
        df = pd.read_csv('mmg.csv')
        self.times = df.iloc[:, 0].tolist() 
        self.data = df.iloc[:, 1].tolist()

    def setup_plot(self):
        self.ax.set_facecolor('black')
        self.figure.patch.set_facecolor('black')  # Set figure background to black

        # Set axis labels and title
        self.ax.set_title('Real-Time MMG Signal', color='white')

        # Customize grid and ticks
        self.ax.grid(True, color='gray')
        self.ax.tick_params(colors='white')  # Set the color of ticks to white

        self.canvas.draw_idle()

    def plot(self):
        if not self._animating or self.current_index >= len(self.times):
            return

        # Append the next data point
        self.current_index += 1

        # Plot the data up to the current index
        self.ax.clear()
        self.ax.plot(self.times[:self.current_index], self.data[:self.current_index], 'b-')
        self.setup_plot()  # Apply the styling

        self.canvas.draw_idle()

    def start(self):
        self._animating = True
        self.timer.start(100)  # Update every 100 ms

    def stop(self):
        self._animating = False
        self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NonRectangularPlot()
    window.show()
    sys.exit(app.exec_())