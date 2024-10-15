#from model.module1 import Signal, Graph
from SignalViewerApp import SignalViewerApp
from Signal import Signal
from Graph import Graph
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu
from PyQt5.uic import loadUi
from PyQt5.QtGui import QCursor,QBrush
from PyQt5.QtCore import QPoint
import sys
import numpy as np
import icons.icons_rc
from PyQt5.QtWidgets import QColorDialog, QPushButton, QMainWindow
from PyQt5.QtGui import QColor,QBrush

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

        self.horizontal_scrollbar = self.findChild(QSlider, "graph1_Hslider")
        # self.horizontal_scrollbar.valueChanged.connect(self.zoom)
        

        # Other initializations ...

    
        #print(data_x)
        #self.color_push_button = self.findChild(QPushButton, "color")
        #self.color_push_button.clicked.connect(self.signal_params.change_color)


    

        self.horizontal_scrollbar_1 = self.findChild(QSlider, "graph1_Hslider")

        self.horizontal_scrollbar_2 = self.findChild(QSlider, "graph2_Hslider")    
        
        # self.horizontal_scrollbar.valueChanged.connect(self.graph1.scroll_horizontal_effect)
        # self.horizontal_scrollbar.setRange(0,int(len(data_x) - self.graph.window_size_x))
        # print(f"Setting scrollbar range: 0 to {len(data_x) - self.graph.window_size_x}")
        # # self.horizontal_scrollbar.setMaximum(10)
        # self.horizontal_scrollbar.valueChanged.connect(self.graph.scroll_horizontal)
        # self.graph.frame_changed.connect(self.update_scrollbar)

        

         # Connect slider to speed functionality
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


    def create_context_menu(self, position):
        context_menu = QMenu(self)

        # Determine which table the right-click occurred in
        if self.table1.underMouse():
            table = self.table1
        elif self.table2.underMouse():
            table = self.table2
        else:
            return  # No valid table found

        # Get the selected row index
        selected_row = table.selectionModel().currentIndex().row()
        current_row = table.currentRow()

        # Add "Switch Graph" action and connect it to the switch_graph function with the selected row
        switch_graph_action = context_menu.addAction("Switch Graph")
        # switch_graph_action.triggered.connect(lambda: self.switch_graph(selected_row))
        
        change_color_action = context_menu.addAction("Change Color")
        change_color_action.triggered.connect(
            lambda:  self.control_color(table,current_row)
        )

        # Get the global position of the cursor
        cursor_position = QCursor.pos()

        # Offset the context menu to the middle of the screen
        offset = QPoint(-int(context_menu.width() / 2), -int(context_menu.height() / 2))
        context_menu.exec_(cursor_position + offset)

    def update_scrollbar(self, frame):
        if frame < self.horizontal_scrollbar.maximum():
            self.horizontal_scrollbar.setValue(frame)
        else:
            self.horizontal_scrollbar.setValue(self.horizontal_scrollbar.maximum())

    def control_color(self, table, current_row):
        if current_row >= 0:
            # Get the corresponding Signal instance for the selected row
            signal_num = int(table.item(current_row, 0).text().replace("Signal", ""))-1
            
            # Retrieve the selected color
            selected_color = QColorDialog.getColor()
            
            if selected_color.isValid():  # Check if a valid color was selected
                color_name = selected_color.name()  # Get the color name (e.g., #ff0000)

                # Update the color in the signal
                if table == self.table1 and self.graph1 is not None:
                    self.graph1.set_signal_color(signal_num,color_name)  # Update signal's color attribute
                     # Call method to update plot color
                elif table == self.table2 and self.graph2 is not None:
                    self.graph2.set_signal_color(signal_num,color_name)
                    
                
                # Set the background color of the item in the table
                table.item(current_row, 2).setBackground(QBrush(QColor(color_name)))

                print("Color changed to:", color_name)


       
        

    # def scroll_horizontal(self, value):
    #     if self.graph_selected.currentText() == 'Graph1':
    #         self.graph1.scroll_horizontal_affect(value)
    #     elif self.graph_selected.currentText() == 'Graph2':
    #         self.graph2.scroll_horizontal_affect(value)


    def contextMenuEvent(self, event):
        self.create_context_menu(event.pos())


    # def scroll_horizontal(self, value):
    #     signal_file_path,  = self.signal_app.browse_signals()
    #     self.signal= Signal(1, csv_path= signal_file_path)
    #     data_x= self.signal.signal_data_time


    #     self.horizontal_scrollbar.setMaximum(data_x[-1])
        

   

        

    
       

       
       
        



    def show_signal_graph1(self):
        signal_file_path,  = self.signal_app.browse_signals()
        self.signal= Signal(1, csv_path= signal_file_path)
        self.add_row(self.signal, 1)
        data_x= self.signal.signal_data_time
        data_y= self.signal.signal_data_amplitude
        if self.graph1 is None:
            self.graph1 = Graph(self.graph_widget_1, signal_x= data_x, signal_y=data_y,title="Graph 1", graph_num=1, is_linked=False, signal =self.signal,horizontal_scrollbar=self.horizontal_scrollbar_1)
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
            self.graph2 = Graph(self.graph_widget_2, signal_x= data_x, signal_y=data_y,title="Graph 2", graph_num=2, is_linked=False, signal= self.signal,horizontal_scrollbar=self.horizontal_scrollbar_2)
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
                self.graph1.rewind_signal(is_option_chosen, self.graph2)
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
            Signal.row_signal_map_1[row_position]= signal 
            self.table1.insertRow(row_position) 
            self.table1.setItem(row_position, 0, QTableWidgetItem(f"Signal{signal.signal_num}"))
            self.table1.setItem(row_position, 1, QTableWidgetItem("Graph1"))
            self.table1.setItem(row_position, 2, QTableWidgetItem("Blue"))
            checkbox = QCheckBox()
            self.table1.setCellWidget(row_position, 3, checkbox)  # Set checkbox in the fourth column

                        
        elif graph_num==2:
            row_position = self.table2.rowCount()
            Signal.row_signal_map_2[row_position]= signal
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
        
        else:
            self.graph_selected.setEnabled(True)
            self.graph_selected.setStyleSheet("")  # Resets to the default style


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowUI()
    window.show()
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application