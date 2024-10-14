#from model.module1 import Signal, Graph
from SignalViewerApp import SignalViewerApp
from Signal import Signal
from Graph import Graph
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QVBoxLayout, QWidget, QSlider, QRadioButton
from PyQt5.uic import loadUi
import sys
import numpy as np
import icons.icons_rc

class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("MainWindowUI.ui", self)
        self.signal_params = Signal()
        self.signal_app = SignalViewerApp()

        # Generating some sample data for the signal
        #data_x= np.linspace(0,20,1000)
        #data_y= np.cos(2*np.pi*data_x)

        #print(data_x)
        #self.color_push_button = self.findChild(QPushButton, "color")
        #self.color_push_button.clicked.connect(self.signal_params.change_color)
        
        self.pause = self.findChild(QPushButton, "pause")
        self.play = self.findChild(QPushButton, "play")
        self.rewind = self.findChild(QRadioButton, "rewind")
        self.upload_file= self.findChild(QPushButton, "uploadfile_C1")

        self.graph_widget = self.findChild(QWidget, "Graph1_signalview")  
        self.graph = Graph(self.graph_widget, signal_x= data_x, signal_y=data_y,title="Graph 1", graph_num=1, is_linked=False)

        # Generating some sample data for the signal
        data_x= self.signal_params.signal_data_time
        data_y= self.signal_params.signal_data_amplitude
        

        # Connect button to pause functionality
        self.pause.clicked.connect(self.graph.pause_signal)
        self.play.clicked.connect(self.graph.resume_signal)
        self.rewind.clicked.connect(self.graph.rewind_signal)
        self.upload_file.clicked.connect(self.signal_app.browse_signals)


        # Automatically visualize the signal in the widget
        self.graph.visualize_graph()
        
         # Connect slider to zoom functionality
        self.zoom = self.findChild(QSlider, "zoom")
        self.zoom.valueChanged.connect(self.graph.set_zoom_value)  # Connect slider value change to update_zoom method

        # Connect slider to speed functionality
        self.speed = self.findChild(QSlider, "speed")
        self.speed = self.findChild(QSlider, "speed")
        self.speed.setMinimum(1)  # Set minimum zoom value
        self.speed.setMaximum(50)  # Set maximum zoom value
        self.speed.setValue(25)  # Set initial zoom value
        self.speed.valueChanged.connect(self.graph.set_speed_value)  # Connect slider value change to update_zoom method
        




                     

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowUI()
    window.show()
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application