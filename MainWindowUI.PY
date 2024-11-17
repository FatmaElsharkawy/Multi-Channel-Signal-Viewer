from SignalViewerApp import SignalViewerApp
from Signal import Signal
from Graph import Graph
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem, QCheckBox, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor,QBrush
from PyQt5.QtCore import QPoint
import sys
import numpy as np
import icons.icons_rc
from PyQt5.QtWidgets import QColorDialog, QPushButton, QMainWindow
from PyQt5.QtGui import QColor,QBrush
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button
from scipy import interpolate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from threading import Thread
from RealTimeData import RealTimePlot
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from pyqtgraph.exporters import ImageExporter
from NonRecGenData import NonRectangularPlot

class GluedWindow(QMainWindow):
    def __init__(self):
        super(GluedWindow, self).__init__()
        loadUi('GluedUI.ui', self)  # Load the glued UI file
        self.setWindowTitle("Glued Window")

class DraggableRectangle:
    def __init__(self, ax):
        self.ax = ax
        self.rect_selector = None  # Initialize without the RectangleSelector
        self.rectangles = [] 
        self.datax_start = None 
        self.datax_end = None 

    def on_select(self, eclick, erelease):
        # Function to handle rectangle selection
        print(f"Start: ({eclick.xdata}, {eclick.ydata})")
        print(f"End: ({erelease.xdata}, {erelease.ydata})")
        self.datax_start = eclick.xdata
        self.datax_end = erelease.xdata
        
        rect = plt.Rectangle(
            (eclick.xdata, eclick.ydata), 
            erelease.xdata - eclick.xdata, 
            erelease.ydata - eclick.ydata, 
            
            facecolor='white',  # Fill the rectangle with red color
            alpha=0.5  # Set transparency
        )
        self.ax.add_patch(rect)  # Add the rectangle to the axis
        self.rectangles.append(rect)  # Store the rectangle reference
        plt.draw()  # Update the plot
        
        
        # Deactivate the selector
        # self.deactivate_selector()

    def activate_selector(self, event):
        """This function activates the RectangleSelector when called."""
        if self.rect_selector is None:  # Create it only once
            self.rect_selector = RectangleSelector(
                self.ax, 
                onselect=self.on_select, 
                interactive=True  # Make the rectangle draggable and resizable
            )
            print(f"RectangleSelector activated on {self.ax.get_title()}.")
        else:
            self.rect_selector.set_active(True)  # Re-activate if already created

    def deactivate_selector(self):
        """Deactivate the rectangle selector."""
        if self.rect_selector is not None:
            self.rect_selector.set_active(False)  # Deactivate the selector
            print(f"RectangleSelector deactivated on {self.ax.get_title()}.")

    def clear_rectangles(self):
        """Remove all created rectangles from the axis."""
        for rect in self.rectangles:
            rect.remove()  # Remove the rectangle from the plot
        self.rectangles.clear()  # Clear the list of rectangles
        plt.draw() 
    def get_datax_start(self):
        return self.datax_start
    def get_datax_end(self):
        return self.datax_end

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
       
        self.glue_button = self.findChild(QPushButton, "glue")
        
        self.graph_widget_1 = self.findChild(QWidget, "Graph1_signalview")  
        self.graph_widget_2 = self.findChild(QWidget, "Graph2_signalview") 

        self.graph_selected= self.findChild(QComboBox, "comboBox")

        self.table1= self.findChild(QTableWidget, "tableWidget_C1")
        self.table2= self.findChild(QTableWidget, "tableWidget_C1_2")

        self.linked= self.findChild(QCheckBox, "linked_chechbox")
        self.linked.clicked.connect(self.link_graphs) #it's called each time the button is clicked (checked or unchecked)
        
        self.horizontal_scrollbar_1 = self.findChild(QSlider, "graph1_Hslider")
        self.horizontal_scrollbar_2 = self.findChild(QSlider, "graph2_Hslider")    
  
        self.pause = self.findChild(QPushButton, "pause")
        self.play = self.findChild(QPushButton, "play")
        self.replay = self.findChild(QPushButton, "replay")
        self.rewind = self.findChild(QRadioButton, "rewind")
        self.zoom = self.findChild(QSlider, "zoom")
        self.speed = self.findChild(QSlider, "speed")
        
        self.speed.setMinimum(1)  # Set minimum zoom value
        self.speed.setMaximum(100)  # Set maximum zoom value
        self.speed.setValue(50)  # Set initial zoom value

        self.pause.clicked.connect(self.pause_signal)
        self.play.clicked.connect(self.resume_signal)
        self.replay.clicked.connect(self.replay_signal)
        self.rewind.clicked.connect(self.rewind_signal)
        self.zoom.valueChanged.connect(self.set_zoom_x) 
        self.zoom.valueChanged.connect(self.set_zoom_y)
        self.speed.valueChanged.connect(self.set_speed_value) 

        #Laila part 
        #NonRec. button
        self.openWindowButton = self.findChild(QPushButton, "pause_2")
        self.openWindowButton.clicked.connect(self.open_nonrectangular_window)

        #real-time button
        self.real_time_button = self.findChild(QPushButton, "real_time")
        self.real_time_button.clicked.connect(self.open_real_time_window)


        #Judy part for glue
        self.glueui_window=None
        self.selected1_x = None
        self.selected2_x = None
        self.selected1_y = None
        self.selected2_y = None
        self.viewer_widget=None        
        self.glue_button = self.findChild(QPushButton, "glue")
        

        self.draggable_rect1 = None
        self.draggable_rect2 = None

        self.selection_button_g1 = self.findChild(QPushButton, "snapshot_G1")
        self.selection_button_g2 = self.findChild(QPushButton, "snapshot_G2")

        self.selection_button_g1.clicked.connect(self.activate_rectangle_graph1)
        self.selection_button_g2.clicked.connect(self.activate_rectangle_graph2)
        self.glue_button.clicked.connect(self.delete_last_rectangle) 
        self.glue_button.clicked.connect(self.open_glue_window)
        self.combobox_order=None
        self.inetrpolation_order="linear" 

        self.glue_start_data1 = None
        self.glue_end_data1 = None
        self.glue_start_data2 = None
        self.glue_end_data2 = None

        self.stat_glued_datax=[]
        self.stat_glued_datay=[]
        self.list_ydata_stat=[]
        self.snapshot_taker=None
        self.report_generator=self.findChild(QPushButton,"glue_report")
        self.report_generator.clicked.connect(self.open_report_window)
    
    # look here again  
    def set_default_signals(self):
        signal= Signal(graph_num=1)
        self.graph1 = Graph(self.graph_widget_1,graph_num=1, signal =signal, horizontal_scrollbar=self.horizontal_scrollbar_1, graph2=self.graph2)
        self.add_row(signal=signal, graph= self.graph1, table= self.table1)
        self.graph1.visualize_graph()

        signal= Signal(graph_num=2)
        self.graph2 = Graph(self.graph_widget_2,graph_num=2, signal = signal, horizontal_scrollbar=self.horizontal_scrollbar_2, graph2=self.graph1)
        self.add_row(signal=signal, graph= self.graph2, table= self.table2)
        self.graph1.other_graph=self.graph2
        self.graph2.visualize_graph()  

    def show_signal_graph1(self):
        signal_file_path,  = self.signal_app.browse_signals()
        signal= Signal(1, csv_path= signal_file_path)
        self.add_row(signal, graph=self.graph1, table=self.table1)
        data_x= signal.signal_data_time
        data_y= signal.signal_data_amplitude
        if self.graph1 is not None:
            self.graph1.add_signal(data_x, data_y, signal)
        else:
            self.graph1= Graph(self.graph_widget_1,graph_num=1, signal =signal, horizontal_scrollbar=self.horizontal_scrollbar_1, graph2=self.graph2)

    def show_signal_graph2(self):
        signal_file_path, = self.signal_app.browse_signals()
        signal= Signal(2, csv_path= signal_file_path)
        self.add_row(signal, graph=self.graph2, table=self.table2)
        data_x= signal.signal_data_time
        data_y= signal.signal_data_amplitude
        if self.graph2 is not None: 
            self.graph2.add_signal(data_x, data_y, signal)
        else:
            self.graph2= Graph(self.graph_widget_2 ,graph_num=2, signal =signal, horizontal_scrollbar=self.horizontal_scrollbar_2, graph2=self.graph1)
    #Switch Functionality
    def switch_graph(self,table, graph, row_index):
        print("switch order gievn")
        if table == self.table1: #we switch from table1 to table2
            removed_signal= self.graph1.remove_signal(row_index)
            self.graph2.add_signal(removed_signal.signal_data_time, removed_signal.signal_data_amplitude, removed_signal)
            signal_label = self.table1.item(row_index, 0).text()
            self.add_row(removed_signal, self.graph2, self.table2, signal_label)
        elif table== self.table2:
            removed_signal= self.graph2.remove_signal(row_index)
            self.graph1.add_signal(removed_signal.signal_data_time, removed_signal.signal_data_amplitude, removed_signal)
            signal_label= self.table2.item(row_index, 0).text()
            self.add_row(removed_signal, self.graph1, self.table1, signal_label)
        self.remove_row(table, row_index)

    def pause_signal(self):
        if self.graph_selected.isEnabled() == False:
            self.graph1.pause_signal(self.graph2)
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
    
    def replay_signal(self):
        if self.graph_selected.isEnabled() == False:
            self.graph1.replay_signal(self.graph2)
    
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.replay_signal()
        elif selected_value == 'Graph2': 
            self.graph2.replay_signal()

    def rewind_signal(self, is_option_chosen):
        print(is_option_chosen)
        if self.graph_selected.isEnabled() == False:
            self.graph1.rewind_signal(self.graph2)
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.rewind_signal(is_option_chosen)
        elif selected_value == 'Graph2': 
            self.graph2.rewind_signal(is_option_chosen)

    def set_zoom_x(self, value):
        if self.graph_selected.isEnabled() == False:
            self.graph1.set_zoom_x(value, self.graph2) 
   
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.set_zoom_x(value)
        elif selected_value == 'Graph2': 
            self.graph2.set_zoom_x(value)  
    
    def set_zoom_y(self, value):
        if self.graph_selected.isEnabled() == False:
            self.graph1.set_zoom_y(value, self.graph2) 
   
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.set_zoom_y(value)
        elif selected_value == 'Graph2': 
            self.graph2.set_zoom_y(value)  
            
    def set_speed_value(self, value):
        if self.graph_selected.isEnabled() == False:
            self.graph1.set_speed_value(value, self.graph2) 
    
        selected_value = self.graph_selected.currentText()
        if selected_value == 'Graph1':
            self.graph1.set_speed_value(value)
        elif selected_value == 'Graph2': 
            self.graph2.set_speed_value(value)    


    def add_row(self, signal, graph, table, signal_label=None):
        row_position = table.rowCount()
        table.insertRow(row_position)
        signal.set_signal_num(row_position)
        print(f"signal.signal_num {signal.signal_num}")
        if signal_label==None or signal_label.startswith("Signal"):
                label_item= table.setItem(row_position, 0, QTableWidgetItem(signal.get_label()))
                if label_item is not None:
                    label_item.setFlags(label_item.flags() | Qt.ItemIsEditable)
        else:
                label_item= signal_label
                table.setItem(row_position, 0, QTableWidgetItem(label_item))
        
        table.setItem(row_position, 1, QTableWidgetItem(f"Graph{graph.graph_num}"))
        table.setItem(row_position, 2, QTableWidgetItem())

    def remove_row(self, table, row_index):
        table.removeRow(row_index)
       
    def create_context_menu(self, position):
        context_menu = QMenu(self)
        if self.table1.underMouse():
            table = self.table1
            graph= self.graph1
        elif self.table2.underMouse():
            table = self.table2
            graph= self.graph2
        else:
            return  # No valid table found

        # Get the selected row index
        selected_row = table.selectionModel().currentIndex().row()

        change_color_action = context_menu.addAction("Change Color")
        change_color_action.triggered.connect(lambda:  self.control_color(table,selected_row))
        switch_graph_action = context_menu.addAction("Switch Graph")        
        switch_graph_action.triggered.connect(lambda:  self.switch_graph(table,graph,selected_row))
        change_visibility_action = context_menu.addAction("Toggle Visibility")        
        change_visibility_action.triggered.connect(lambda: self.toggle_signal_visibility(graph,selected_row))
        remove_action = context_menu.addAction("Remove Signal")        
        remove_action.triggered.connect(lambda: self.remove_action(table,graph,selected_row))

        # Get the global position of the cursor
        cursor_position = QCursor.pos()

        # Offset the context menu to the middle of the screen
        offset = QPoint(-int(context_menu.width() / 2), -int(context_menu.height() / 2))
        context_menu.exec_(cursor_position + offset)
    
    def contextMenuEvent(self, event):
        self.create_context_menu(event.pos())
    
    def remove_action(self,table, graph, row_index):
        self.remove_row(table, row_index)
        removed_signal= graph.remove_signal(row_index)


    def toggle_signal_visibility(self, graph, current_row):  #current row is the row_index
        if current_row >= 0:
           signal = graph.signals_list[current_row]
           is_visible= signal.get_visiblity()
           graph.set_signal_visibility(current_row, is_visible)
           signal.set_visiblity(not is_visible)
    
    def control_color(self, table, current_row):
        if current_row >= 0:
            signal_num =current_row
            selected_color = QColorDialog.getColor()
            if selected_color.isValid():  # Check if a valid color was selected
                color_name = selected_color.name()  # Get the color name (e.g., #ff0000)
                if table == self.table1 and self.graph1 is not None:
                    self.graph1.set_signal_color(signal_num,color_name) #update the plot color
                    self.graph1.signals_list[signal_num].set_color(color_name) #update the signal color attribute
                elif table == self.table2 and self.graph2 is not None:
                    self.graph2.set_signal_color(signal_num,color_name)
                    self.graph2.signals_list[signal_num].set_color(color_name)
                # Set the background color of the item in the table
                table.item(current_row, 2).setBackground(QBrush(QColor(color_name)))

                print("Color changed to:", color_name)
    
    
    def link_graphs(self):
        if self.linked.isChecked():
            print("graphs will be linked")
            self.graph_selected.setEnabled(False)
            self.graph1.is_linked = True
            self.graph2.is_linked = True
        else:
            self.graph_selected.setEnabled(True)
            self.graph1.is_linked = False
            self.graph2.is_linked = False


    ##GLUE PART
    def activate_rectangle_graph1(self):
        # Ensure the DraggableRectangle is instantiated for graph1 if not already
        if self.draggable_rect1 is None:
            self.draggable_rect1 = DraggableRectangle(self.graph1.ax) 
             # Pass the existing axis from Graph1
        self.draggable_rect1.activate_selector(None) 
        
         

    def activate_rectangle_graph2(self):
        # Ensure the DraggableRectangle is instantiated for graph2 if not already
        if self.draggable_rect2 is None:
            self.draggable_rect2 = DraggableRectangle(self.graph2.ax)  # Pass the existing axis from Graph2
        self.draggable_rect2.activate_selector(None)
        
         # Activate the rectangle selection on graph2

    # def deactivate_both_rectangles(self):
    #     self.draggable_rect1.clear_rectangles()
    #     self.draggable_rect2.clear_rectangles()
    #     plt.draw()  # Ensure the plot refreshes completely

    def delete_last_rectangle(self):
        """Remove the last added rectangle from the plot."""
        if self.draggable_rect1 is not None:
            self.glue_start_data1 = self.draggable_rect1.get_datax_start()
            self.glue_end_data1 = self.draggable_rect1.get_datax_end()
            print(f"start: {self.glue_start_data1}, end: {self.glue_end_data1}")
            self.draggable_rect1.clear_rectangles()      
        if self.draggable_rect2 is not None:
            self.glue_start_data2 = self.draggable_rect2.get_datax_start()      
            self.glue_end_data2 = self.draggable_rect2.get_datax_end()
            print(f"start: {self.glue_start_data2}, end: {self.glue_end_data2}")
            self.draggable_rect2.clear_rectangles()  # Clear rectangles from graph2

        # Remove the last rectangle from the list of rectangles in the DraggableRectangle class
        if self.draggable_rect1.rectangles:
            self.draggable_rect1.rectangles.pop().remove() 
            
        elif self.draggable_rect2.rectangles:
            self.draggable_rect2.rectangles.pop().remove()
              
        
        plt.draw()    

    def open_glue_window(self):
    # Ensure both signals (signal1 and signal2) are loaded before gluing.
    # Ensure there is only one signal on both graphs

        if self.graph1.no_of_signals_on_graph==1 and self.graph2.no_of_signals_on_graph==1:
            signal1= self.graph1.signals_list[0]
            signal2=self.graph2.signals_list[0]
            
            if signal1 and signal2:            
                if self.glueui_window is None :
                    self.glueui_window=GluedWindow()
                self.snapshot_taker=self.glueui_window.findChild(QPushButton,"snapshot_pushbutton")
                self.snapshot_taker.clicked.connect(self.snapshot_)
                self.combobox_order=self.glueui_window.findChild(QComboBox,"order_combobox")
                self.combobox_order.currentIndexChanged.connect(self.handle_combobox_change)
                self.viewer_widget=self.glueui_window.findChild(QWidget,"viewer")
                self.gap_slider=self.glueui_window.findChild(QSlider,"gap_slider")
                self.gluer(self.glue_start_data1,self.glue_start_data2,self.glue_end_data1,self.glue_end_data2, signal1, signal2)
                self.glueui_window.show()

            else:
                print("Load both signals before gluing.")
        else:
            print("visualize only one signal on graph")

    def interpolate_signals(self, selected2_x):
        """
        Glue two signals together, handling either gap or overlap between them.
        Interpolates the gap if needed using interp1d.
        """
        # If the second signal starts before the first
        if selected2_x[0] < self.selected1_x[0]:
            # Check if there's an overlap
            
            
            if self.selected1_x[0] < selected2_x[-1]:
                # Calculate overlap region
                self.overlap_start = max(min(self.selected1_x), min(selected2_x))
                self.overlap_end = min(max(self.selected1_x), max(selected2_x))
                print(f"overlap_start: {self.overlap_start}, overlap_end: {self.overlap_end}")

                # Interpolate both signals in the overlap region
                interpolation_function_signal1 = interpolate.interp1d(self.selected1_x, self.selected1_y, kind=self.inetrpolation_order)
                interpolation_function_signal2 = interpolate.interp1d(selected2_x, self.selected2_y, kind=self.inetrpolation_order)
                x_overlapped = np.linspace(self.overlap_start, self.overlap_end, num=1000)

                signal_1_interpolated = interpolation_function_signal1(x_overlapped)
                signal_2_interpolated = interpolation_function_signal2(x_overlapped)

                # Average the overlapped signals
                y_interpolated = (signal_1_interpolated + signal_2_interpolated) / 2
            else:
                # Calculate the gap region between the signals
                self.x_gap = np.linspace(selected2_x[-1], self.selected1_x[0], num=int(self.selected1_x[0] - selected2_x[-1]+1))
                
                # Concatenate both signals for interpolation over the gap
                data_x = np.concatenate([selected2_x, self.selected1_x])
                data_y = np.concatenate([self.selected2_y, self.selected1_y])
                
                interpolation_function = interpolate.interp1d(data_x, data_y, kind=self.inetrpolation_order)
                y_interpolated = interpolation_function(self.x_gap)
        else:
            # If the second signal starts after the first
            if selected2_x[0] < self.selected1_x[-1]:
                # Calculate overlap region
                self.overlap_start = max(min(self.selected1_x), min(selected2_x))
                self.overlap_end = min(max(self.selected1_x), max(selected2_x))
                
                # Interpolate both signals in the overlap region
                interpolation_function_signal1 = interpolate.interp1d(self.selected1_x, self.selected1_y, kind=self.inetrpolation_order)
                interpolation_function_signal2 = interpolate.interp1d(selected2_x, self.selected2_y, kind=self.inetrpolation_order)
                x_overlapped = np.linspace(self.overlap_start, self.overlap_end, num=1000)

                signal_1_interpolated = interpolation_function_signal1(x_overlapped)
                signal_2_interpolated = interpolation_function_signal2(x_overlapped)

                # Average the overlapped signals
                y_interpolated = (signal_1_interpolated + signal_2_interpolated) / 2
            else:
                # Calculate the gap region between the signals
                self.x_gap = np.linspace(self.selected1_x[-1], selected2_x[0], num=int(selected2_x[0] - self.selected1_x[-1]+1))
                
                # Concatenate both signals for interpolation over the gap
                data_x = np.concatenate([self.selected1_x, selected2_x])
                data_y = np.concatenate([self.selected1_y, self.selected2_y])
                
                interpolation_function = interpolate.interp1d(data_x, data_y, kind=self.inetrpolation_order,fill_value="extrapolate")
                y_interpolated = interpolation_function(self.x_gap)
        
        return np.array(y_interpolated)        

    def gluer(self,start_x,start_y,end_x,end_y, signal1, signal2):

        signal_layout = QtWidgets.QVBoxLayout()
        plot_widget = pg.PlotWidget(title="Part X and Part Y: Same Graph")
        signal_layout.addWidget(plot_widget)
        self.viewer_widget.setLayout(signal_layout)

        mask1 = (signal1.signal_data_time >= start_x) & (signal1.signal_data_time <= end_x)
        mask2 = (signal2.signal_data_time >= start_y) & (signal2.signal_data_time <= end_y)

        self.selected1_x = signal1.signal_data_time[mask1]
        self.selected1_y = signal1.signal_data_amplitude[mask1] 
        self.selected2_x = signal2.signal_data_time[mask2]
        self.selected2_y = signal2.signal_data_amplitude[mask2]         
            
        # Plot both selected parts of the signals
        plot_widget.plot(self.selected1_x, self.selected1_y, pen='b')
        plot_widget.plot(self.selected2_x, self.selected2_y, pen='r')

        # Add a gap slider for the user to specify the gap between signals
        
        self.gap_slider.setRange(-50, 50)  # Set range for the gap to allow negative values for overlap
        self.gap_slider.setValue(0)  # Set a default value for the gap
        

        def update_movable_signal(gap_value):

            plot_widget.clear()

            # Adjust the x-values of the second signal based on the gap value
            selected2_x_moved = np.array([x + gap_value for x in self.selected2_x])

            # Check if there's an overlap between the two signals
            if selected2_x_moved[0] < self.selected1_x[0]:  # If selected2_x_moved starts before selected1_x
                if self.selected1_x[0] < selected2_x_moved[-1]:  # Overlapping case
                    print("1")

                    # Interpolating the second signal based on moved x-values
                    y_interpolated = self.interpolate_signals(selected2_x_moved)

                    # Find the overlap indices
                    overlap_start_index = np.where(selected2_x_moved >= self.overlap_start)[0][0]
                    overlap_end_index = np.where(self.selected1_x >= self.overlap_end)[0][0]

                    # Plot the regions before and after the overlap
                    # plot_widget.plot(selected2_x_moved[0:overlap_start_index], self.selected2_y[0:overlap_start_index], pen='r', name="Signal 1")
                    # plot_widget.plot(self.selected1_x[overlap_end_index:], self.selected1_y[overlap_end_index:], pen='b', name="Signal 2")

                    # Plot the interpolated section
                    x_range = np.linspace(self.overlap_start, self.overlap_end, num=1000)
                    # plot_widget.plot(x_range, y_interpolated, pen='g', name="interpolated")
                    self.stat_glued_datax=np.concatenate([selected2_x_moved[0:overlap_start_index],x_range,self.selected1_x[overlap_end_index:]])
                    self.stat_glued_datay=np.concatenate([ self.selected2_y[0:overlap_start_index],y_interpolated,self.selected1_y[overlap_end_index:]])
                    
                    x_axis_res=np.concatenate([selected2_x_moved[0:overlap_start_index],x_range,self.selected1_x[overlap_end_index:]])
                    y_axis_res=np.concatenate([self.selected2_y[0:overlap_start_index],y_interpolated,self.selected1_y[overlap_end_index:]])
                    plot_widget.plot(x_axis_res, y_axis_res, pen='g', name="interpolated")

                else:  # No overlap case
                    print("2")
                    self.x_gap = np.linspace(selected2_x_moved[-1], self.selected1_x[0], num=int(abs(self.selected1_x[0] - selected2_x_moved[-1])) + 1)

                    plot_widget.plot(selected2_x_moved, self.selected2_y, pen='r', name="Signal 1")
                    plot_widget.plot(self.selected1_x, self.selected1_y, pen='b', name="Signal 2")

                    # Interpolate the second signal
                    y_interpolated = self.interpolate_signals(selected2_x_moved)

                    if len(self.x_gap) != len(y_interpolated):
                        min_length = min(len(self.x_gap), len(y_interpolated))
                        self.x_gap = self.x_gap[:min_length]
                        y_interpolated = y_interpolated[:min_length]

                    plot_widget.plot(self.x_gap, y_interpolated, pen='g', name="interpolated")
                    self.stat_glued_datax=np.concatenate([selected2_x_moved,self.x_gap,self.selected1_x])
                    self.stat_glued_datay=np.concatenate([self.selected2_y,y_interpolated,self.selected1_y])

            else:  # Case where the first part of the second signal overlaps with the end of the first signal
                if selected2_x_moved[0] < self.selected1_x[-1]:
                    # Interpolating the second signal
                    y_interpolated = self.interpolate_signals(selected2_x_moved)

                    # Find the overlap indices
                    overlap_start_index = np.where(self.selected1_x >= self.overlap_start)[0][0]
                    overlap_end_index = np.where(selected2_x_moved >= self.overlap_end)[0][0]

                    # Plot the regions before and after the overlap
                    # plot_widget.plot(self.selected1_x[0:overlap_start_index], self.selected1_y[0:overlap_start_index], pen='b', name="Signal 1")
                    # plot_widget.plot(selected2_x_moved[overlap_end_index:], self.selected2_y[overlap_end_index:], pen='r', name="Signal 2")

                    # Plot the interpolated section
                    x_range = np.linspace(self.overlap_start, self.overlap_end, num=1000)

                    self.stat_glued_datax=np.concatenate([self.selected1_x[0:overlap_start_index],x_range,selected2_x_moved[overlap_end_index:]])
                    self.stat_glued_datay=np.concatenate([self.selected1_y[0:overlap_start_index],y_interpolated ,self.selected2_y[overlap_end_index:]])

                    x_axis_res=np.concatenate([self.selected1_x[0:overlap_start_index],x_range,selected2_x_moved[overlap_end_index:]])
                    y_axis_res=np.concatenate([self.selected1_y[0:overlap_start_index],y_interpolated,self.selected2_y[overlap_end_index:]])
                    plot_widget.plot(x_axis_res, y_axis_res, pen='g', name="interpolated")
                    # plot_widget.plot(x_axis_res, y_axis_res, pen='g', name="interpolated")


                else:  # No overlap, just plot the two signals with an interpolated line
                    self.x_gap = np.linspace(self.selected1_x[-1], selected2_x_moved[0], num=int(abs(selected2_x_moved[0] - self.selected1_x[-1])) + 1)

                    plot_widget.plot(self.selected1_x, self.selected1_y, pen='b', name="Signal 1")
                    plot_widget.plot(selected2_x_moved, self.selected2_y, pen='r', name="Signal 2")

                    y_interpolated = self.interpolate_signals(selected2_x_moved)

                    if len(self.x_gap) != len(y_interpolated):
                        min_length = min(len(self.x_gap), len(y_interpolated))
                        self.x_gap = self.x_gap[:min_length]
                        y_interpolated = y_interpolated[:min_length]

                    plot_widget.plot(self.x_gap, y_interpolated, pen='g', name="interpolated")

                    self.stat_glued_datax=np.concatenate([self.selected1_x,self.x_gap,selected2_x_moved])
                    self.stat_glued_datay=np.concatenate([self.selected1_y,y_interpolated,self.selected2_y])

        # Connect the gap slider to the update function
        self.gap_slider.valueChanged.connect(update_movable_signal)


    
    def open_nonrectangular_window(self):
        self.secondary_window = NonRectangularPlot()
        self.secondary_window.show()

    def open_real_time_window(self):
        self.real_time_window = RealTimePlot()
        self.real_time_window.show()

    def open_report_window(self):
        if not self.list_ydata_stat:
            print("No Data")
            return
        self.report_window=ReportWindow(self.list_ydata_stat)
        self.report_window.show()    

    def handle_combobox_change(self, index):
        self.inetrpolation_order = self.combobox_order.currentText()
        print(f"Selected item: {self.inetrpolation_order}")

    def snapshot_(self):
        self.list_ydata_stat.append(self.stat_glued_datay)


class ReportWindow(QDialog):
    def __init__(self, all_cropped_data: list):
        super().__init__()
        self.setWindowTitle("Generate Report")

        # Apply dark mode stylesheet with blue buttons
        self.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e;  /* Dark background */
                color: white;               /* White text */
            }
            QTextEdit {
                background-color: #3e3e3e;  /* Darker background for text area */
                color: white;               /* White text */
                border: 1px solid #5e5e5e;  /* Border for text area */
            }
            QPushButton {
                background-color: #4a90e2;  /* Blue button background */
                color: white;               /* White text on button */
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #357ab8;  /* Darker blue on hover */
            }
            QScrollArea {
                background-color: #3e3e3e;  /* Darker scroll area background */
            }
        """)

        # Adjust window size for better display
        self.setGeometry(100, 100, 800, 600)

        self.all_cropped_data = all_cropped_data  # Data passed from the main window

        # Create a layout and text area for writing the report
        layout = QVBoxLayout()

        # Add a text area for the user to write the report
        self.report_text = QTextEdit(self)
        self.report_text.setPlaceholderText("Write your report here...")
        self.report_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.report_text)

        # Scrollable area for the graphs
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Display the cropped data as graphs horizontally
        self.graph_widgets = []
        for cropped_data in self.all_cropped_data:
            graph_widget = pg.PlotWidget(self)
            graph_widget.plot(cropped_data, pen='white')  # White plot lines for dark background
            graph_widget.setBackground('#2e2e2e')  # Dark background for the plot widget
            graph_widget.setFixedHeight(250)  # Adjusted height for better display
            graph_widget.setFixedWidth(400)  # Wider graphs for horizontal layout
            self.graph_widgets.append(graph_widget)
            self.scroll_layout.addWidget(graph_widget)

        # Button to save the report
        save_button = QPushButton("Save Report")
        save_button.clicked.connect(self.save_report)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_report(self):
        """Save the report as a PDF file with graphs."""
        report_text = self.report_text.toPlainText()

        if not report_text:
            print("No report text to save.")
            return

        # File dialog to select where to save the PDF
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf)")

        if file_name:
            # Create a PDF canvas
            c = canvas.Canvas(file_name, pagesize=letter)
            width, height = letter

            # Add a header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, height - 40, "User Report")

            # Write the report text on the PDF
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 80, "Report Content:")
            text_lines = report_text.split('\n')
            y_pos = height - 100

            # Add text content
            for line in text_lines:
                c.drawString(60, y_pos, line)
                y_pos -= 15

            y_pos -= 20
            c.drawString(50, y_pos, "Graphs of the cropped data:")
            y_pos -= 40

            # Save each graph as an image and add it to the PDF
            for idx, graph_widget in enumerate(self.graph_widgets):
                # Get the data from the plotted curve
                curve = graph_widget.plotItem.curves[0]
                data = curve.getData()[1]

                # Calculate the mean, std, maximum point, and minimum point of the graph
                mean = np.mean(data)
                std = np.std(data)
                max_point = np.max(data)
                min_point = np.min(data)

                # Create statistics table data
                table_data = [
                    ["Statistic", "Value"],
                    ["Mean", f"{mean:.2f}"],
                    ["Std", f"{std:.2f}"],
                    ["Max", f"{max_point:.2f}"],
                    ["Min", f"{min_point:.2f}"],
                ]

                # Define the table and style
                table = Table(table_data, colWidths=[150, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))

                # Save each graph as a PNG image
                exporter = ImageExporter(graph_widget.plotItem)
                image_path = f"graph_{idx}.png"
                exporter.export(image_path)

                # Load the image and draw it on the PDF
                c.drawImage(image_path, 50, y_pos - 150, width=400, height=150)
                os.remove(image_path)

                # Add bold and underlined graph title
                c.setFont("Helvetica-Bold", 12)
                c.drawString(60, y_pos - 170, f"Graph {idx + 1}")
                c.line(60, y_pos - 173, 140, y_pos - 173)  # Underline

                # Draw the statistics table below the graph
                y_pos -= 200
                table.wrapOn(c, width - 100, height)
                table.drawOn(c, 60, y_pos - 80)

                # Create a new page if space runs out
                y_pos -= 120
                if y_pos < 100:
                    c.showPage()
                    y_pos = height - 60

            # Save the PDF
            c.save()
            print(f"Report saved to {file_name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindowUI()
    window.show()
    window.set_default_signals()
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application