#from model.module1 import Signal, Graph
from SignalViewerApp import SignalViewerApp
from Signal import Signal
from Graph import Graph
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
import sys
import numpy as np

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("MainWindow.ui", self)
        self.signal_params = Signal()
        self.signal_app = SignalViewerApp()
        self.color_push_button = self.findChild(QPushButton, "color_push_button")
        self.color_push_button.clicked.connect(self.signal_params.change_color)

        self.pushButton_6 = self.findChild(QPushButton, "pushButton_6")

        self.graph_widget = self.findChild(QWidget, "Graph1_widget")


        # Generating some sample data for the signal
        # data_x= self.signal_params.signal_data_time
        # data_y= self.signal_params.signal_data_amplitude
        t = np.linspace(0, 20, 1000)  # Time vector extended to 20 seconds
        data = np.sin(2 * np.pi * t)  # Example signal (sine wave)

        # Create the Graph instance, embedding it in "Graph1_widget"
        self.graph = Graph(self.graph_widget, signal_x= t, signal_y=data, window_size=10, title="Graph 1", graph_num=1, is_linked=False)

        # Automatically visualize the signal in the widget
        self.graph.visualize_graph()
        
        # Connect button to pause functionality
        self.pushButton_6.clicked.connect(self.graph.pause_signal)




                     

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application