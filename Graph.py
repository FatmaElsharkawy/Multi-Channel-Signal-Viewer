import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np
import math
from PyQt5.QtCore import QTimer

class Graph:
    def __init__(self, parent_widget, is_linked, graph_num, title, signal_x, signal_y, signal):
        self.graph_num = graph_num
        self.is_linked = is_linked
        self.title = title
        self.zoom_value = 50
        self.signal_x = [signal_x]
        self.signal_y = [signal_y]
        self.signals_list= [signal]
        self.fig, self.ax = plt.subplots(figsize=(8,5))
        self.signal_plot, = self.ax.plot([], [], lw=2)
        self.frames_num = len(signal_x)
        self.default_window_size_x = (self.signal_x[0][-1] - self.signal_x[0][0]) / 4 
        self.window_size_x = self.default_window_size_x
        self.start, self.end = 0, 0
        self.interval = 10
        self.timer = QTimer()  # QTimer doesn't need a parent here
        self.no_of_signals_on_graph= 1
        # Initialize the Matplotlib canvas and set the parent
        self.canvas = FigureCanvas(self.fig)
        self.fig.patch.set_facecolor('none')
        self.ax.set_facecolor('#1E1E1E')
        self.fig.subplots_adjust(left=0.05, right=0.9, top=0.85, bottom=0.15)
        self.repeat= False

        # Ensure the parent widget has a layout
        if parent_widget.layout() is None:
            layout = QVBoxLayout(parent_widget)
            parent_widget.setLayout(layout)
        else:
            layout = parent_widget.layout()

        # Add the canvas to the parent's layout
        layout.addWidget(self.canvas)

        self.current_frame = 0  # Track the current frame being displayed

        # Connect the timer to the update function
        self.timer.timeout.connect(self.update_graph)
    
    def add_signal(self, signal_x, signal_y, signal):
        self.no_of_signals_on_graph += 1
        self.signals_list.append(signal)
        self.signal_x.append(signal_x)
        self.signal_y.append(signal_y)
        self.visualize_graph()  # Restart visualization to include the new signal

    def init_graph(self):
        self.ax.clear()  # Clear existing plots to reinitialize the graph
        self.ax.set_xlim(self.signal_x[0][0], self.signal_x[0][0] + self.window_size_x)
        self.ax.set_ylim(
            min(min(y) for y in self.signal_y) - 0.2,
            max(max(y) for y in self.signal_y) + 0.2
        )
        
        # Initialize plots for each signal
        self.signal_plots = [
            self.ax.plot([], [], lw=2)[0] for _ in range(self.no_of_signals_on_graph)
        ]
        self.canvas.draw()

    def update_graph(self):
        frame = self.current_frame
        for idx, plot in enumerate(self.signal_plots):
            # Extract x and y data for the current frame
            x_data = self.signal_x[idx][:frame]
            y_data = self.signal_y[idx][:frame]

            # Skip if x_data is empty to avoid index errors
            if len(x_data) == 0:
                continue

            # Adjust x-axis limits based on the current window size
            if x_data[-1] < self.window_size_x:
                self.ax.set_xlim(self.signal_x[idx][0], self.signal_x[idx][0] + self.window_size_x)
            else:
                self.start = x_data[-1] - self.window_size_x
                self.end = x_data[-1]
                self.ax.set_xlim(self.start, self.end)

            # Update the data for the current plot
            plot.set_data(x_data, y_data)

        self.canvas.draw()
        self.current_frame += 1


        # Check for the end of the animation and handle rewinding
        if self.current_frame >= self.frames_num:
            if self.get_rewind():
                self.current_frame = 0  # Reset the frame to rewind
            else:
                self.timer.stop()

    def visualize_graph(self):
        self.current_frame = 0  # Reset frame count when a new signal is added
        self.init_graph()
        self.timer.start(self.interval)  # Restart the timer with the current interval

        
    def pause_signal(self, graph=None):
        self.timer.stop()  # Pause the timer
        if graph is not None:
            graph.timer.stop()

    def resume_signal(self, graph=None):
        self.timer.start(self.interval)
        if graph is not None:
            graph.timer.start()

    def set_speed_value(self, value, graph=None):
        print("I entered speed, value", value)
        self.interval = value
        self.timer.setInterval(self.interval)  # Dynamically adjust the timer interval
        if graph is not None:
            graph.interval= value
            graph.timer.setInterval(graph.interval)
   
    def get_speed_value(self):
        return self.interval
    
    def rewind_signal(self, is_option_chosen, graph=None):
        self.repeat = is_option_chosen
        if self.repeat and not self.timer.isActive():
            # If rewinding is enabled and animation is stopped, restart
            self.current_frame = 0
            self.timer.start(self.interval)
            if graph is not None:
                graph.current_frame = 0
                graph.timer.start(graph.interval)

    def get_rewind(self):
        return self.repeat
    
    
    def set_zoom_value(self, value, graph=None):
        print("I entered zoom value", value)
        self.zoom_value= value
        zoom_ratio =  self.zoom_value/ 50
        self.zoom_graph(zoom_ratio)
        if graph is not None:
            graph.zoom_value= value
            zoom_ratio =  graph.zoom_value/ 50
            graph.zoom_graph(zoom_ratio)

    
    #Based on the zoom_value, we update the window size, to see the effect of zoom in and out
    def zoom_graph(self, zoom_ratio):
        self.window_size_x= self.default_window_size_x/ zoom_ratio
         # Now adjust the x-axis limits based on the zoom level even if the animation is paused.
        current_frame = max(0, self.current_frame - 1)
        for idx in range(self.no_of_signals_on_graph):
            x_data = self.signal_x[idx][:current_frame]

            if len(x_data) == 0:
                continue

            if x_data[-1] < self.window_size_x:
                self.ax.set_xlim(self.signal_x[idx][0], self.signal_x[idx][0] + self.window_size_x)
            else:
                self.start = x_data[-1] - self.window_size_x
                self.end = x_data[-1]
                self.ax.set_xlim(self.start, self.end)

        self.canvas.draw()  # Redraw the canvas to show the zoom effect
    

    def link_graphs(self, graph2):
        #the two objects (self--> refering to graph1) & (graph2) have same speed, zoomed together, paused together, and so on
        pass
    
 

    
