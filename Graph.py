import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class Graph(QWidget):
    def __init__(self,parent, is_linked, graph_num , title, signal_x, signal_y, window_size ):
        super().__init__(parent)
        self.graph_num= graph_num
        self.is_linked= is_linked
        self.title="Graph 1"
        self.zoom_ratio= 50
        self.signal_x= signal_x
        self.signal_y = signal_y
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.signal_plot, = self.ax.plot([], [], lw=2) 
        self.frames_num= len(signal_x)
        self.window_size= window_size
        self.animated_plot= None
        # Initialize the Matplotlib canvas and set the parent
        self.canvas = FigureCanvas(self.fig)
        self.fig.patch.set_facecolor('#2E2E2E')  # Change figure background color (dark grey)
        self.ax.set_facecolor('#1E1E1E')  # Change the axes background color (darker grey)
        
        # Layout for the graph
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.fig.tight_layout()


   # the following methods (init_graph, updated_graph, and visualize) is to visualize the signal continuously
    def init_graph(self):
        self.ax.set_xlim(self.signal_x[0], self.signal_x[0] + self.window_size)  # Initial x-axis window based on signal_x
        self.ax.set_ylim(min(self.signal_y), max(self.signal_y))  
        self.signal_plot.set_data([], [])
        return self.signal_plot,

    def update_graph(self, frame):
        if self.signal_x[frame] < self.window_size:
            # Keep the initial x-axis window fixed until the signal reaches the window end
            self.ax.set_xlim(self.signal_x[0], self.signal_x[0] +  self.window_size)
            self.signal_plot.set_data(self.signal_x[:frame], self.signal_y[:frame])
        else:
            # Scroll the x-axis based on the signal_x values
            start = self.signal_x[frame] - self.window_size
            end = self.signal_x[frame] 
            self.ax.set_xlim(start, end)
            window_indices = np.where((self.signal_x >= start) & (self.signal_x <= end))
            self.signal_plot.set_data(self.signal_x[window_indices], self.signal_y[window_indices])
            

        return self.signal_plot,

    def visualize_graph(self):
        animated_plot = animation.FuncAnimation(fig= self.fig, func= self.update_graph, frames= self.frames_num,
                                      init_func=self.init_graph, blit=True, interval=10, repeat= False)
        
        self.canvas.draw()
        
    def pause_signal(self):
        if self.animated_plot is not None:
            self.animated_plot.pause()  
        else:
            print("No animation to pause.")

    def resume_signal(self):
        if self.animated_plot is not None:
            self.animated_plot.resume()  
        else:
            print("No animation to resume.")

    def set_signal(self, signal_x, signal_y):
        self.signal_x= signal_x
        self.signal_y= signal_y

    def set_title(self, title):
        self.title= title
