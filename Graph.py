import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np
import math
from PyQt5.QtCore import QTimer


class Graph:
    def __init__(self, parent_widget, graph_num, signal, horizontal_scrollbar, graph2 ,is_linked = False ):
        self.graph_num = graph_num
        self.title = f"Graph{self.graph_num}"
        self.zoom_value = 50
        self.signal_x = [signal.signal_data_time]
        self.signal_y = [signal.signal_data_amplitude]
        self.signals_list = [signal]
        self.no_of_signals_on_graph = 1
        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.default_window_size_x = (self.signal_x[0][-1] - self.signal_x[0][0]) / 50
        self.window_size_x = self.default_window_size_x
        self.y_min_limit= min(self.signal_y[0]) - 0.2
        self.y_max_limit= max(self.signal_y[0]) + 0.2
        self.start, self.end = 0, 0
        self.interval = 50
        self.repeat = False
        self.is_linked= is_linked
        self.other_graph = graph2 
        
        self.frames_num = len(self.signal_x[0])  # Length of the first signal's time data
        self.first_frame = None
        self.last_frame = None
        self.first_frame_came = False

        self.toggle_visibility_list = []

        self.timer = QTimer()
        self.canvas = FigureCanvas(self.fig)  # Used to embed matplotlib figure into QTwidget
        #some designs 
        self.fig.patch.set_facecolor('none')
        self.ax.set_facecolor('#1E1E1E')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['bottom'].set_color('white')  
        self.ax.tick_params(axis='x', colors='white')  
        self.ax.tick_params(axis='y', colors='white')
        self.fig.subplots_adjust(left=0.05, right=0.9, top=0.85, bottom=0.15)

        if parent_widget.layout() is None:
            layout = QVBoxLayout(parent_widget)
            parent_widget.setLayout(layout)
        else:
            layout = parent_widget.layout()

        # Add the canvas to the parent's layout
        layout.addWidget(self.canvas)
        self.fig.tight_layout()
        self.current_frame = 0  # Track the current frame being displayed

        # Connect the timer to the update function
        self.timer.timeout.connect(self.update_graph)
        
        #pan functionality
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.dragging = False
        self.start_press_event = None

    def add_signal(self, signal_x, signal_y, signal):
        self.signals_list.append(signal)
        self.signal_x.append(signal_x)
        self.signal_y.append(signal_y)
        self.visualize_graph()

    def remove_signal(self, signal_index):
        removed_signal = self.signals_list.pop(signal_index)
        self.signal_x.pop(signal_index)
        self.signal_y.pop(signal_index)
        self.signal_plots.pop(signal_index)
        self.visualize_graph()
        return removed_signal

    def get_numSignals_onGraph(self):
        return len(self.signals_list)

    def init_graph(self):
        self.first_frame_came = False
        self.ax.clear()  # Clear existing plots to reinitialize the graph
        if len(self.signals_list)>0:
            self.ax.set_xlim(self.signal_x[0][0], self.signal_x[0][0] + self.window_size_x)
            self.y_min_limit=  min(min(y) for y in self.signal_y) - 0.2
            self.y_max_limit= max(max(y) for y in self.signal_y) + 0.2
            self.ax.set_ylim(self.y_min_limit,self.y_max_limit)
            
            # Initialize plots for each signal
            self.signal_plots = [
                self.ax.plot([], [], lw=2)[0] for idx in range(self.get_numSignals_onGraph())
            ]
            self.canvas.draw()
        else: # all signals are removed from the graph
            return 

    def update_graph(self):
        frame = self.current_frame
        if len(self.signals_list) >0:
            for idx, plot in enumerate(self.signal_plots):
                if idx in self.toggle_visibility_list:
                    continue
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
                    if not self.first_frame_came:
                        self.first_frame = self.current_frame
                        self.first_frame_came = True
                
                # Update the data for the current plot
                plot.set_data(x_data, y_data)

            self.canvas.draw()
            self.current_frame += 1
            
            # Rewind or stop
            if self.current_frame >= self.frames_num:
                if self.get_rewind():
                    self.replay_signal() # Reset the frame to rewind
                else:
                    self.timer.stop()
        else: 
            print("no plots or signals to show on this graph")
            self.current_frame=0
            self.canvas.draw()
            self.timer.stop()


    def visualize_graph(self):
        self.current_frame = 0  # Reset frame count when a new signal is added
        self.init_graph()
        self.timer.start(self.interval)


    def set_signal_visibility(self, signal_index, is_visible):
        if 0 <= signal_index < len(self.signal_plots):
            if is_visible: # the signal is visible, we want to toggle its visibility
                self.toggle_visibility_list.append(signal_index)
            elif is_visible == False: #we want to toggle it to true
                self.toggle_visibility_list.remove(signal_index)
            print(self.toggle_visibility_list) #to debug
            self.canvas.draw()

    def set_signal_color(self, signal_index, color):
        if 0 <= signal_index < len(self.signal_plots):
            self.signal_plots[signal_index].set_color(color)
            self.canvas.draw()
        else:
            print("Signal index out of range.")   


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
        self.interval = 101- value
        self.timer.setInterval(self.interval)  # Dynamically adjust the timer interval
        if graph is not None:
            graph.interval= 101- value
            graph.timer.setInterval(graph.interval)
   
    def get_speed_value(self):
        return self.interval
          
    def rewind_signal(self, is_option_chosen, graph=None):
        self.repeat = is_option_chosen
        print(f"self.repeat{self.repeat}")
        if graph is not None:
            graph.repeat = is_option_chosen

    def get_rewind(self):
        return self.repeat
    
    def replay_signal(self, graph2=None):
        self.visualize_graph()
        if graph2 is not None:
            graph2.visualize_graph()


    def set_zoom_x(self, value, graph=None):
        print("I entered zoom value", value)
        self.zoom_value= value
        zoom_ratio =  self.zoom_value/ 50
        self.zoom_graph_x(zoom_ratio)
        if graph is not None:
            graph.zoom_value= value
            zoom_ratio =  graph.zoom_value/ 50
            graph.zoom_graph_x(zoom_ratio)

    
    #Based on the zoom_value, we update the window size, to see the effect of zoom in and out
    def zoom_graph_x(self, zoom_ratio):
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
    
    def set_zoom_y(self, zoom_value, graph=None):
        zoom_ratio= zoom_value/50
        self.zoom_graph_y(zoom_ratio)
        if graph is not None:
            graph.zoom_graph_y(zoom_ratio)
    
    def zoom_graph_y(self, zoom_ratio):
        y_min_limit= self.y_min_limit/ zoom_ratio
        y_max_limit= self.y_max_limit/zoom_ratio
        self.ax.set_ylim(y_min_limit, y_max_limit)
        self.canvas.draw()
        
    def on_press(self, event):
        """Handles the mouse press event to start dragging/panning."""
        if event.button == 1:  # Left mouse button for panning
            self.dragging = True
            self.start_press_event = event

    def on_motion(self, event):
        """Handles the mouse motion event to pan the graph with x lower limit of 0 and y limits between -1 and 2."""
        if self.dragging and self.start_press_event:
            if event.xdata is not None and event.ydata is not None and self.start_press_event.xdata is not None and self.start_press_event.ydata is not None:
                dx = event.xdata - self.start_press_event.xdata
                dy = event.ydata - self.start_press_event.ydata

                # Get the current x and y axis limits
                current_xlim = self.ax.get_xlim()
                current_ylim = self.ax.get_ylim()

                # Calculate the new x-axis limits after panning
                new_xlim_start = current_xlim[0] - dx
                new_xlim_end = current_xlim[1] - dx

                # Calculate the new y-axis limits after panning
                new_ylim_start = current_ylim[0] - dy
                new_ylim_end = current_ylim[1] - dy

                # Ensure the lower x limit doesn't go below zero
                if new_xlim_start < 0:
                    new_xlim_start = 0
                    new_xlim_end = new_xlim_start + (current_xlim[1] - current_xlim[0])

                # Ensure the y limits stay within the range [-1, 2]
                if new_ylim_start < -1:
                    new_ylim_start = -1
                    new_ylim_end = new_ylim_start + (current_ylim[1] - current_ylim[0])
                if new_ylim_end > 2:
                    new_ylim_end = 2
                    new_ylim_start = new_ylim_end - (current_ylim[1] - current_ylim[0])

                # Set the new x and y axis limits
                self.ax.set_xlim(new_xlim_start, new_xlim_end)
                self.ax.set_ylim(new_ylim_start, new_ylim_end)

                # Redraw the canvas with the new limits
                self.canvas.draw()

                # Apply the same limits to the other graph if linked
                if self.is_linked and self.other_graph:
                    self.other_graph.ax.set_xlim(new_xlim_start, new_xlim_end)
                    self.other_graph.ax.set_ylim(new_ylim_start, new_ylim_end)
                    self.other_graph.canvas.draw()

    def on_release(self, event):
        """Handles the mouse release event to stop dragging."""
        if event.button == 1:  # Left mouse button
            self.dragging = False
    
    
 