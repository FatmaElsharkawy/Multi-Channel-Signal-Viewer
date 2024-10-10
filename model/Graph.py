

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Graph:
    def __init__(self, is_linked, graph_num , title, zoom_ratio, signal_x, signal_y ):
        self.graph_num= graph_num
        self.is_linked= is_linked
        self.title="Graph 1"
        self.zoom_ratio= 50
        self.signal_x= signal_x
        self.signal_y = signal_y
        self.fig, self.ax = plt.subplots()
        self.signal_plot, = self.ax.plot([], [], lw=2) 
        self.frames_num= len(signal_x)

   # the following methods (init_graph, updated_graph, and visualize) is to visualize the signal continuously
    def init_graph(self):
        self.ax.set_xlim(min(self.signal_x), max(self.signal_x))  
        self.ax.set_ylim(min(self.signal_y), max(self.signal_y))  
        self.signal_plot.set_data([], [])
        return self.signal_plot,

    def update_graph(self, frame):
        self.signal_plot.set_data(self.signal_x[:frame], self.signal_y[:frame])
        return self.signal_plot,

    def visualize_graph(self):
        ani = animation.FuncAnimation(fig= self.fig, func= self.update_graph, frames= self.frames_num,
                                      init_func=self.init_graph, blit=True, interval=50)
        plt.show()
        

    def set_signal(self, signal_x, signal_y):
        self.signal_x= signal_x
        self.signal_y= signal_y

    def set_title(self, title):
        self.title= title
