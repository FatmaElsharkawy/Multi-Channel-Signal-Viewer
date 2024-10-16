<<<<<<< Updated upstream
#from model.module1 import Signal, Graph
from SignalViewerApp import SignalViewerApp
from Signal import Signal
from Graph import Graph
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.uic import loadUi
import sys
import numpy as np
import icons.icons_rc

class GluedWindow(QMainWindow):
    def __init__(self):
        super(GluedWindow, self).__init__()
        loadUi('GluedUI.ui', self)  # Load the glued UI file
        self.setWindowTitle("Glued Window")

class NonRictangularWindow(QMainWindow):
    def __init__(self):
        super(NonRictangularWindow, self).__init__()
        loadUi('NonRectangularUI.ui', self)  # Load the glued UI file
        self.setWindowTitle("Non-rectangular Window")


class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("MainWindowUI.ui", self)
        self.openWindowButton = self.findChild(QPushButton, "glue")
        self.openWindowButton.clicked.connect(self.open_glued_window)
        self.openWindowButton = self.findChild(QPushButton, "pause_2")
        self.openWindowButton.clicked.connect(self.open_nonrectangular_window)
        self.signal_app = SignalViewerApp()
        self.graph1= None
        self.graph2= None
        self.upload_file_1= self.findChild(QPushButton, "uploadfile_C1")
        self.upload_file_2= self.findChild(QPushButton, "uploadfile_C2")
        self.upload_file_1.clicked.connect(self.show_signal_graph1)
        self.upload_file_2.clicked.connect(self.show_signal_graph2)        

        self.graph_widget_1 = self.findChild(QWidget, "Graph1_signalview")  
        self.graph_widget_2 = self.findChild(QWidget, "Graph2_signalview") 

        self.graph_selected= self.findChild(QComboBox, "comboBox")

        self.table1= self.findChild(QTableWidget, "tableWidget_C1")
        self.table2= self.findChild(QTableWidget, "tableWidget_C2")


        self.pause = self.findChild(QPushButton, "pause")
        self.play = self.findChild(QPushButton, "play")
        self.rewind = self.findChild(QRadioButton, "rewind")
        self.zoom = self.findChild(QSlider, "zoom")
        self.speed = self.findChild(QSlider, "speed")
        self.speed.setMinimum(1)  # Set minimum zoom value
        self.speed.setMaximum(50)  # Set maximum zoom value
        self.speed.setValue(25)  # Set initial zoom value
        
        self.pause.clicked.connect(self.pause_signal)
        self.play.clicked.connect(self.resume_signal)
        self.rewind.clicked.connect(self.rewind_signal)
        self.zoom.valueChanged.connect(self.set_zoom_value)  
        self.speed.valueChanged.connect(self.set_speed_value)  # Connect slider value change to update_zoom method


    def open_glued_window(self):
        # Create and show the secondary window
        self.secondary_window = GluedWindow()
        self.secondary_window.show()    

    def open_nonrectangular_window(self):
        # Create and show the secondary window
        self.secondary_window = NonRictangularWindow()
        self.secondary_window.show()  

    def show_signal_graph1(self):
        signal_file_path,  = self.signal_app.browse_signals()
        self.signal= Signal(1, csv_path= signal_file_path)
        self.add_row(self.signal, 1)
        data_x= self.signal.signal_data_time
        data_y= self.signal.signal_data_amplitude
        if self.graph1 is None:
            self.graph1 = Graph(self.graph_widget_1, signal_x= data_x, signal_y=data_y,title="Graph 1", graph_num=1, is_linked=False, signal =self.signal)
            self.graph1.visualize_graph()
        else: #graph exits, signal will be added only
            self.graph1.add_signal(data_x, data_y, self.signal)


    def show_signal_graph2(self):
        signal_file_path, = self.signal_app.browse_signals()
        self.signal= Signal(2, csv_path= signal_file_path)
        self.add_row(self.signal, 2)
        data_x= self.signal.signal_data_time
        data_y= self.signal.signal_data_amplitude
        if self.graph2 is None:
            self.graph2 = Graph(self.graph_widget_2, signal_x= data_x, signal_y=data_y,title="Graph 2", graph_num=2, is_linked=False, signal= self.signal)
            self.graph2.visualize_graph()
        else: 
            self.graph2.add_signal(data_x, data_y, self.signal)

    def pause_signal(self):
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.pause_signal()
        elif selected_value == 'Graph2': 
            self.graph2.pause_signal()

    def resume_signal(self):
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.resume_signal()
        elif selected_value == 'Graph2': 
            self.graph2.resume_signal()

    def rewind_signal(self):
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.rewind_signal()
        elif selected_value == 'Graph2': 
            self.graph2.rewind_signal()

    def set_zoom_value(self, value):   
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.set_zoom_value(value)
        elif selected_value == 'Graph2': 
            self.graph2.set_zoom_value(value)    

                
    def set_speed_value(self, value):   
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.set_speed_value(value)
        elif selected_value == 'Graph2': 
            self.graph2.set_speed_value(value)    


    def add_row(self, signal, graph_num): 
        if graph_num==1:
            row_position = self.table1.rowCount()
            self.table1.insertRow(row_position) 
            self.table1.setItem(row_position, 0, QTableWidgetItem(f"Signal{signal.signal_num}"))
            self.table1.setItem(row_position, 1, QTableWidgetItem("Graph1"))
            self.table1.setItem(row_position, 2, QTableWidgetItem("Blue"))
            checkbox = QCheckBox()
            self.table1.setCellWidget(row_position, 3, checkbox)  # Set checkbox in the fourth column

                        
        elif graph_num==2:
            row_position = self.table2.rowCount()
            self.table2.insertRow(row_position) 
            self.table2.setItem(row_position, 0, QTableWidgetItem(f"Signal{signal.signal_num}"))
            self.table2.setItem(row_position, 1, QTableWidgetItem("Graph2"))
            self.table2.setItem(row_position, 2, QTableWidgetItem("Blue"))
            checkbox = QCheckBox()
            self.table2.setCellWidget(row_position, 3, checkbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowUI()
    window.show()
=======
#from model.module1 import Signal, Graph
from SignalViewerApp import SignalViewerApp
from Signal import Signal
from Graph import Graph
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.uic import loadUi
import sys
import numpy as np
import icons.icons_rc
import pyqtgraph as pg

class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("MainWindowUI.ui", self)
        self.signal_app = SignalViewerApp()
        self.graph1= None
        self.graph2= None
        self.upload_file_1= self.findChild(QPushButton, "uploadfile_C1")
        self.upload_file_2= self.findChild(QPushButton, "uploadfile_C2")
        self.upload_file_1.clicked.connect(self.show_signal_graph1)
        self.upload_file_2.clicked.connect(self.show_signal_graph2)
      

        self.graph_widget_1 = self.findChild(QWidget, "Graph1_signalview")  
        self.graph_widget_2 = self.findChild(QWidget, "Graph2_signalview") 

        self.graph_selected= self.findChild(QComboBox, "comboBox")

        self.table1= self.findChild(QTableWidget, "tableWidget_C1")
        self.table2= self.findChild(QTableWidget, "tableWidget_C1_2")

        self.linked= self.findChild(QCheckBox, "linked_chechbox")
        self.linked.clicked.connect(self.link_graphs) #it's called each time the button is clicked (checked or unchecked)

        self.pause = self.findChild(QPushButton, "pause")
        self.play = self.findChild(QPushButton, "play")
        self.rewind = self.findChild(QRadioButton, "rewind")
        self.zoom = self.findChild(QSlider, "zoom")
        self.speed = self.findChild(QSlider, "speed")
        self.speed.setMinimum(1)  # Set minimum zoom value
        self.speed.setMaximum(50)  # Set maximum zoom value
        self.speed.setValue(25)  # Set initial zoom value
        
        self.pause.clicked.connect(self.pause_signal)
        self.play.clicked.connect(self.resume_signal)
        self.rewind.clicked.connect(self.rewind_signal)
        self.zoom.valueChanged.connect(self.set_zoom_value)  
        self.speed.valueChanged.connect(self.set_speed_value)  # Connect slider value change to update_zoom method

                
        self.signal= Signal()
        self.graph1 = Graph(self.graph_widget_1, signal_x= self.signal.signal_data_time, signal_y= self.signal.signal_data_amplitude, is_linked=False, title="Graph 1", signal =self.signal, graph_num=1)
        self.graph1.visualize_graph()  

    def show_signal_graph1(self):
        signal_file_path,  = self.signal_app.browse_signals()
        self.signal= Signal(1, csv_path= signal_file_path)
        self.add_row(self.signal, 1)
        data_x= self.signal.signal_data_time
        data_y= self.signal.signal_data_amplitude
        if self.graph1 is not None:
            self.graph1.add_signal(data_x, data_y, self.signal)


    def show_signal_graph2(self):
        signal_file_path, = self.signal_app.browse_signals()
        self.signal= Signal(2, csv_path= signal_file_path)
        self.add_row(self.signal, 2)
        data_x= self.signal.signal_data_time
        data_y= self.signal.signal_data_amplitude
        if self.graph2 is None:
            self.graph2 = Graph(self.graph_widget_2, signal_x= data_x, signal_y=data_y,title="Graph 2", graph_num=2, is_linked=False, signal= self.signal)
            self.graph2.visualize_graph()
        else: 
            self.graph2.add_signal(data_x, data_y, self.signal)

    def pause_signal(self):
        if self.graph_selected.isEnabled() == False:
            self.graph1.pause_signal(self.graph2)
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.pause_signal()
        elif selected_value == 'Graph2': 
            self.graph2.pause_signal()

    def resume_signal(self):
        if self.graph_selected.isEnabled() == False:
            self.graph1.resume_signal(self.graph2)
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.resume_signal()
        elif selected_value == 'Graph2': 
            self.graph2.resume_signal()

    def rewind_signal(self, is_option_chosen):
        if self.graph_selected.isEnabled() == False:
            self.graph1.rewind_signal(self.graph2)
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.rewind_signal(is_option_chosen)
        elif selected_value == 'Graph2': 
            self.graph2.rewind_signal(is_option_chosen)

    def set_zoom_value(self, value):
        if self.graph_selected.isEnabled() == False:
            self.graph1.set_zoom_value(value, self.graph2) 
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.set_zoom_value(value)
        elif selected_value == 'Graph2': 
            self.graph2.set_zoom_value(value)    

                
    def set_speed_value(self, value):
        if self.graph_selected.isEnabled() == False:
            self.graph1.set_speed_value(value, self.graph2) 
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.set_speed_value(value)
        elif selected_value == 'Graph2': 
            self.graph2.set_speed_value(value)    


    def add_row(self, signal, graph_num): 
        if graph_num==1:
            row_position = self.table1.rowCount()
            self.table1.insertRow(row_position) 
            self.table1.setItem(row_position, 0, QTableWidgetItem(f"Signal{signal.signal_num}"))
            self.table1.setItem(row_position, 1, QTableWidgetItem("Graph1"))
            self.table1.setItem(row_position, 2, QTableWidgetItem("Blue"))
            checkbox = QCheckBox()
            self.table1.setCellWidget(row_position, 3, checkbox)  # Set checkbox in the fourth column

                        
        elif graph_num==2:
            row_position = self.table2.rowCount()
            self.table2.insertRow(row_position) 
            self.table2.setItem(row_position, 0, QTableWidgetItem(f"Signal{signal.signal_num}"))
            self.table2.setItem(row_position, 1, QTableWidgetItem("Graph2"))
            self.table2.setItem(row_position, 2, QTableWidgetItem("Blue"))
            checkbox = QCheckBox()
            self.table2.setCellWidget(row_position, 3, checkbox)
    
    def link_graphs(self):
        if self.linked.isChecked():
            print("graphs will be linked")
            self.graph_selected.setEnabled(False)
            self.graph_selected.setStyleSheet("""
                QComboBox {
                    background-color: #D3D3D3;  /* Light gray color to mimic disabled state */
                    color: #A9A9A9;             /* Dark gray text to mimic disabled text */
                    border: 1px solid #A9A9A9;  /* Optional: Add a border color to match */
                }
            """)
            self.graph1.link_graphs(self.graph2)
        else:
            self.graph_selected.setEnabled(True)
            self.graph_selected.setStyleSheet("")  # Resets to the default style

  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowUI()
    window.show()
>>>>>>> Stashed changes
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application