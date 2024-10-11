import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np
import math

class Graph(QWidget):
    def __init__(self,parent, is_linked, graph_num, title, signal_x, signal_y):
        super().__init__(parent)
        self.graph_num = graph_num
        self.is_linked = is_linked
        self.title = title
        self.zoom_value = 50
        self.signal_x = signal_x
        self.signal_y = signal_y
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.signal_plot, = self.ax.plot([], [], lw=2) 
        self.frames_num = len(signal_x)
        self.default_window_size_x = int(signal_x[-1] - signal_x[0])/ 2
        self.window_size_x= self.default_window_size_x
        self.animated_plot = None
        self.start, self.end = 0,0
        self.interval= 10

        # Initialize the Matplotlib canvas and set the parent
        self.canvas = FigureCanvas(self.fig)
        self.fig.patch.set_facecolor('#2E2E2E')
        self.ax.set_facecolor('#1E1E1E')

        # Layout for the graph
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.fig.tight_layout()

    def init_graph(self):
        print("window size is ", self.window_size_x)
        self.ax.set_xlim(self.signal_x[0], self.signal_x[0] + self.window_size_x)
        self.ax.set_ylim(min(self.signal_y)-2, max(self.signal_y)+2)  
        self.signal_plot.set_data([], [])
        return self.signal_plot,

    def update_graph(self, frame):
        if self.signal_x[frame] < self.window_size_x:
            self.ax.set_xlim(self.signal_x[0], self.signal_x[0] + self.window_size_x)
            self.signal_plot.set_data(self.signal_x[:frame], self.signal_y[:frame])
        else:
            self.start = self.signal_x[frame] - self.window_size_x
            self.end = self.signal_x[frame]
            self.ax.set_xlim(self.start, self.end)
            window_indices = np.where((self.signal_x >= self.start) & (self.signal_x <= self.end))
            self.signal_plot.set_data(self.signal_x[window_indices], self.signal_y[window_indices])

        self.canvas.draw()
        return self.signal_plot,


    def visualize_graph(self):
        self.animated_plot = animation.FuncAnimation(self.fig, self.update_graph, frames=self.frames_num,
                                                     init_func=self.init_graph, blit=True, interval= self.interval, repeat=False)
        self.canvas.draw()

    def pause_signal(self):
        if self.animated_plot is not None:
            self.animated_plot.event_source.stop()
        else:
            print("No animation to pause.")

    def resume_signal(self):
        if self.animated_plot is not None:
            self.animated_plot.event_source.start()
        else:
            print("No animation to resume.")

    def set_zoom_value(self, value):
        print("I entered zoom value", value)
        self.zoom_value= value
        zoom_ratio =  self.zoom_value/ 50
        self.zoom_graph(zoom_ratio)
    
    #Based on the zoom_value, we update the window size, to see the effect of zoom in and out
    def zoom_graph(self, zoom_ratio):
        self.window_size_x= self.default_window_size_x/ zoom_ratio

    def set_speed_value(self, value):
        print("I entered speed, value", value)
        self.interval= value
    