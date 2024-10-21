#from model.module1 import Signal, Graph
from SignalViewerApp import SignalViewerApp
from Signal import Signal
from Graph import Graph
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QWidget, QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor,QBrush
from PyQt5.QtCore import QPoint
import sys
import numpy as np
import icons.icons_rc
from PyQt5.QtWidgets import QColorDialog, QPushButton, QMainWindow
from PyQt5.QtGui import QColor,QBrush
from SignalGlue import SignalGlue
import numpy as np
from scipy import interpolate
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button

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

class DraggableRectangle:
    def __init__(self, ax):
        self.ax = ax
        self.rect_selector = None  # Initialize without the RectangleSelector
        self.rectangles = []  # List to store created rectangles

    def on_select(self, eclick, erelease):
        # Function to handle rectangle selection
        print(f"Start: ({eclick.xdata}, {eclick.ydata})")
        print(f"End: ({erelease.xdata}, {erelease.ydata})")

        # Create a rectangle from the selection
        rect = plt.Rectangle(
            (eclick.xdata, eclick.ydata), 
            erelease.xdata - eclick.xdata, 
            erelease.ydata - eclick.ydata, 
            
            facecolor='red',  # Fill the rectangle with red color
            alpha=0.5  # Set transparency
        )
        self.ax.add_patch(rect)  # Add the rectangle to the axis
        self.rectangles.append(rect)  # Store the rectangle reference
        plt.draw()  # Update the plot
        
        # Deactivate the selector
        self.deactivate_selector()

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




class MainWindowUI(QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        loadUi("MainWindowUI.ui", self)
        self.signal_app = SignalViewerApp()
        self.graph1= None
        self.graph2= None
        self.upload_file_1= self.findChild(QPushButton, "uploadfile_C1")
        self.upload_file_2= self.findChild(QPushButton, "uploadfile_C2")
        self.signal1= None
        self.signal2= None
        self.upload_file_1.clicked.connect(self.show_signal_graph1)
        self.upload_file_2.clicked.connect(self.show_signal_graph2)
        
        
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

        self.signal= Signal(graph_num=1)
        self.graph1 = Graph(self.graph_widget_1, signal_x= self.signal.signal_data_time, signal_y= self.signal.signal_data_amplitude, is_linked=False, title="Graph 1", signal =self.signal, graph_num=1, horizontal_scrollbar=self.horizontal_scrollbar_1)
        self.graph1.visualize_graph()  

        self.glueui_window=None
        self.selected1_x = None
        self.selected2_x = None
        self.selected1_y = None
        self.selected2_y = None
        self.viewer_widget=None        
        self.glue_button = self.findChild(QPushButton, "glue")
        self.glue_button.clicked.connect(self.open_glue_window)

        self.draggable_rect1 = None
        self.draggable_rect2 = None

        self.selection_button_g1 = self.findChild(QPushButton, "snapshot_G1")
        self.selection_button_g2 = self.findChild(QPushButton, "snapshot_G2")

        self.selection_button_g1.clicked.connect(self.activate_rectangle_graph1)
        self.selection_button_g2.clicked.connect(self.activate_rectangle_graph2)
        # self.glue_button.clicked.connect(self.deactivate_both_rectangles)
        self.glue_button.clicked.connect(self.delete_last_rectangle)




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

    def toggle_signal_visibility(self, current_row, state):
        """Toggle the visibility of the signal based on the checkbox state."""
        if current_row >= 0:
            # Get the checkbox state (0 = Unchecked, 2 = Checked)
            visible = (state == Qt.Checked)  # Check if the checkbox is checked
            
            # Get the signal number based on the first column
            signal_num = int(self.table1.item(current_row, 0).text().replace("Signal", "")) - 1
            
            # Update the visibility of the signals in both graphs
            if self.graph1 is not None:
                self.graph1.set_signal_visibility(signal_num, visible)  # Update Graph 1 visibility
            if self.graph2 is not None:
                self.graph2.set_signal_visibility(signal_num, visible)  # Update Graph 2 visibility

        

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


    def contextMenuEvent(self, event):
        self.create_context_menu(event.pos())

   

    def activate_rectangle_graph1(self):
        # Ensure the DraggableRectangle is instantiated for graph1 if not already
        if self.draggable_rect1 is None:
            self.draggable_rect1 = DraggableRectangle(self.graph1.ax)  # Pass the existing axis from Graph1
        self.draggable_rect1.activate_selector(None)  # Activate the rectangle selection on graph1

    def activate_rectangle_graph2(self):
        # Ensure the DraggableRectangle is instantiated for graph2 if not already
        if self.draggable_rect2 is None:
            self.draggable_rect2 = DraggableRectangle(self.graph2.ax)  # Pass the existing axis from Graph2
        self.draggable_rect2.activate_selector(None)  # Activate the rectangle selection on graph2

    # def deactivate_both_rectangles(self):
    #     self.draggable_rect1.clear_rectangles()
    #     self.draggable_rect2.clear_rectangles()
    #     plt.draw()  # Ensure the plot refreshes completely

    def delete_last_rectangle(self):
        """Remove the last added rectangle from the plot."""
        if self.draggable_rect1 is not None:
            self.draggable_rect1.clear_rectangles()  # Clear rectangles from graph1
        if self.draggable_rect2 is not None:
            self.draggable_rect2.clear_rectangles()  # Clear rectangles from graph2

        # Remove the last rectangle from the list of rectangles in the DraggableRectangle class
        if self.draggable_rect1.rectangles:
            self.draggable_rect1.rectangles.pop().remove()  # Remove the last rectangle
        elif self.draggable_rect2.rectangles:
            self.draggable_rect2.rectangles.pop().remove()  # Remove the last rectangle

        plt.draw()    

    def open_glue_window(self):
    # Ensure both signals (signal1 and signal2) are loaded before gluing
        if self.signal1 and self.signal2:
            # self.glue_window = SignalGlue(self.signal1.signal_data_time,self.signal1.signal_data_amplitude, self.signal2.signal_data_time, self.signal2.signal_data_amplitude)
            
            if self.glueui_window is None :
                self.glueui_window=GluedWindow()
            
            self.viewer_widget=self.glueui_window.findChild(QWidget,"viewer")
            self.gap_slider=self.glueui_window.findChild(QSlider,"gap_slider")
            self.gluer(200,300,250,400)
            self.glueui_window.show()


        else:
            print("Load both signals before gluing.")

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
                interpolation_function_signal1 = interpolate.interp1d(self.selected1_x, self.selected1_y, kind='cubic',fill_value="extrapolate")
                interpolation_function_signal2 = interpolate.interp1d(selected2_x, self.selected2_y, kind='cubic',fill_value="extrapolate")
                x_overlapped = np.linspace(self.overlap_start, self.overlap_end, num=int(self.overlap_end - self.overlap_start))

                signal_1_interpolated = interpolation_function_signal1(x_overlapped)
                signal_2_interpolated = interpolation_function_signal2(x_overlapped)

                # Average the overlapped signals
                y_interpolated = (signal_1_interpolated + signal_2_interpolated) / 2
            else:
                # Calculate the gap region between the signals
                self.x_gap = np.linspace(selected2_x[-1], self.selected1_x[0], num=int(self.selected1_x[0] - selected2_x[-1]))
                
                # Concatenate both signals for interpolation over the gap
                data_x = np.concatenate([selected2_x, self.selected1_x])
                data_y = np.concatenate([self.selected2_y, self.selected1_y])
                
                interpolation_function = interpolate.interp1d(data_x, data_y, kind='quadratic',fill_value="extrapolate")
                y_interpolated = interpolation_function(self.x_gap)
        else:
            # If the second signal starts after the first
            if selected2_x[0] < self.selected1_x[-1]:
                # Calculate overlap region
                self.overlap_start = max(min(self.selected1_x), min(selected2_x))
                self.overlap_end = min(max(self.selected1_x), max(selected2_x))
                
                # Interpolate both signals in the overlap region
                interpolation_function_signal1 = interpolate.interp1d(self.selected1_x, self.selected1_y, kind='quadratic',fill_value="extrapolate")
                interpolation_function_signal2 = interpolate.interp1d(selected2_x, self.selected2_y, kind='quadratic',fill_value="extrapolate")
                x_overlapped = np.linspace(self.overlap_start, self.overlap_end, num=int(self.overlap_end - self.overlap_start))

                signal_1_interpolated = interpolation_function_signal1(x_overlapped)
                signal_2_interpolated = interpolation_function_signal2(x_overlapped)

                # Average the overlapped signals
                y_interpolated = (signal_1_interpolated + signal_2_interpolated) / 2
            else:
                # Calculate the gap region between the signals
                self.x_gap = np.linspace(self.selected1_x[-1], selected2_x[0], num=int(selected2_x[0] - self.selected1_x[-1]))
                
                # Concatenate both signals for interpolation over the gap
                data_x = np.concatenate([self.selected1_x, selected2_x])
                data_y = np.concatenate([self.selected1_y, self.selected2_y])
                
                interpolation_function = interpolate.interp1d(data_x, data_y, kind='quadratic',fill_value="extrapolate")
                y_interpolated = interpolation_function(self.x_gap)
        
        return np.array(y_interpolated)        

    def gluer(self,start_x,start_y,end_x,end_y):

        signal_layout = QtWidgets.QVBoxLayout()
        plot_widget = pg.PlotWidget(title="Part X and Part Y: Same Graph")
        signal_layout.addWidget(plot_widget)
        self.viewer_widget.setLayout(signal_layout)

        mask1 = (self.signal1.signal_data_time >= start_x) & (self.signal1.signal_data_time <= end_x)
        mask2 = (self.signal2.signal_data_time >= start_y) & (self.signal2.signal_data_time <= end_y)

        self.selected1_x = self.signal1.signal_data_time[mask1]
        self.selected1_y = self.signal1.signal_data_amplitude[mask1] 
        self.selected2_x = self.signal2.signal_data_time[mask2]
        self.selected2_y = self.signal2.signal_data_amplitude[mask2]         
            
        # Plot both selected parts of the signals
        plot_widget.plot(self.selected1_x, self.selected1_y, pen='b')
        plot_widget.plot(self.selected2_x, self.selected2_y, pen='r')

        # Add a gap slider for the user to specify the gap between signals
        
        self.gap_slider.setRange(-50, 50)  # Set range for the gap to allow negative values for overlap
        self.gap_slider.setValue(0)  # Set a default value for the gap
        # gap_label = QtWidgets.QLabel(f"Gap: {gap} samples")

        # def update_gap_label(value):
        #     gap_label.setText(f"Gap: {value} samples")

        # gap_slider.valueChanged.connect(update_gap_label)

        def update_movable_signal(gap_value):

            plot_widget.clear()

            # Adjust the x-values of the second signal based on the gap value
            selected2_x_moved = np.array([x + gap_value for x in self.selected2_x])
        
            if selected2_x_moved[0]<self.selected1_x[0]:
                if self.selected1_x[0]<selected2_x_moved[-1]:
                    print("1")
                    
                    y_interpolated = self.interpolate_signals(selected2_x_moved)
                    
                    print(f"overlap_start: {self.overlap_start}, overlap_end: {self.overlap_end}")
                    # Find the index corresponding to the overlap start in selected2_x_moved
                    overlap_start_index = np.where(selected2_x_moved >= self.overlap_start)[0][0]

                    # Find the index corresponding to the overlap end in selected1_x
                    overlap_end_index = np.where(self.selected1_x >= self.overlap_end)[0][0]

                    # Plot the regions before and after the overlap
                    plot_widget.plot(selected2_x_moved[0:overlap_start_index], self.selected2_y[0:overlap_start_index], pen='r', name="Signal 1")
                    plot_widget.plot(self.selected1_x[overlap_end_index:], self.selected1_y[overlap_end_index:], pen='b', name="Signal 2")

                    plot_widget.plot(range(int(self.overlap_start),int(self.overlap_end)), y_interpolated, pen='g', name="interpolated")
                
                else:
                    print("2")
                    self.x_gap = np.linspace(selected2_x_moved[-1], self.selected1_x[0], num=np.int16(abs(self.selected1_x[0] ) - np.int16(selected2_x_moved[-1])))
                    plot_widget.plot(selected2_x_moved, self.selected2_y, pen='r', name="Signal 1")
                    plot_widget.plot(self.selected1_x, self.selected1_y, pen='b', name="Signal 2")
                    plot_widget.plot(self.x_gap, self.interpolate_signals(selected2_x_moved), pen='g', name="interpolated")
                    
            else:
                if selected2_x_moved[0]<self.selected1_x[-1]:
                    y_interpolated = self.interpolate_signals(selected2_x_moved)
                    print(f"overlap_start: {self.overlap_start}, overlap_end: {self.overlap_end}")

                    # Find the index corresponding to overlap_start in self.selected1_x
                    overlap_start_index = np.where(self.selected1_x >= self.overlap_start)[0][0]

                    # Find the index corresponding to overlap_end in selected2_x_moved
                    overlap_end_index = np.where(selected2_x_moved >= self.overlap_end)[0][0]

                    # Plot the regions before and after the overlap
                    plot_widget.plot(self.selected1_x[0:overlap_start_index], self.selected1_y[0:overlap_start_index], pen='b', name="Signal 1")
                    plot_widget.plot(selected2_x_moved[overlap_end_index:], self.selected2_y[overlap_end_index:], pen='r', name="Signal 2")

                    plot_widget.plot(range(int(self.overlap_start),int(self.overlap_end)), y_interpolated, pen='g', name="interpolated")


                else:
                    self.x_gap = np.linspace(self.selected1_x[-1], selected2_x_moved[0],num=(np.int16(selected2_x_moved[0])- np.int16(self.selected1_x[-1])))
                    plot_widget.plot(self.selected1_x, self.selected1_y, pen='b', name="Signal 1")
                    plot_widget.plot(selected2_x_moved, self.selected2_y, pen='r', name="Signal 2")
                    plot_widget.plot(self.x_gap, self.interpolate_signals(selected2_x_moved), pen='g', name="interpolated")
                
            # Plot both signals in the combined window with the adjusted gap
            # plot_widget.plot(self.selected1_x, self.selected1_y, pen='b', name="Signal 1")
            # plot_widget.plot(selected2_x_moved, self.selected2_y, pen='r', name="Signal 2")




        self.gap_slider.valueChanged.connect(update_movable_signal)



        

        

    def show_signal_graph1(self):
        signal_file_path,  = self.signal_app.browse_signals()
        self.signal1= Signal(1, csv_path= signal_file_path)
        self.add_row(self.signal, 1)
        data_x= self.signal.signal_data_time
        data_y= self.signal.signal_data_amplitude
        if self.graph1 is not None:
            self.graph1.add_signal(data_x, data_y, self.signal)

    def show_signal_graph2(self):
        signal_file_path, = self.signal_app.browse_signals()
        self.signal2= Signal(2, csv_path= signal_file_path)
        self.add_row(self.signal2, 2)
        data_x= self.signal2.signal_data_time
        data_y= self.signal2.signal_data_amplitude
        if self.graph2 is None:
            self.graph2 = Graph(self.graph_widget_2, signal_x= data_x, signal_y=data_y,title="Graph 2", graph_num=2, is_linked=False, signal= self.signal2,horizontal_scrollbar=self.horizontal_scrollbar_2)
            self.graph2.visualize_graph()
        else: 
            self.graph2.add_signal(data_x, data_y, self.signal2)

    
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
            Signal.row_signal_map_1[row_position]= signal 
            self.table1.insertRow(row_position) 
            self.table1.setItem(row_position, 0, QTableWidgetItem(f"Signal{signal.signal_num}"))
            self.table1.setItem(row_position, 1, QTableWidgetItem("Graph1"))
            self.table1.setItem(row_position, 2, QTableWidgetItem())
            checkbox = QCheckBox()
            checkbox.setChecked(True)  # Set checkbox in the fourth column
            checkbox.stateChanged.connect(lambda state: self.toggle_signal_visibility(row_position, state))  # Connect state change
            self.table1.setCellWidget(row_position, 3, checkbox)

                        
        elif graph_num==2:
            row_position = self.table2.rowCount()
            Signal.row_signal_map_2[row_position]= signal
            self.table2.insertRow(row_position) 
            self.table2.setItem(row_position, 0, QTableWidgetItem(f"Signal{signal.signal_num}"))
            self.table2.setItem(row_position, 1, QTableWidgetItem("Graph2"))
            self.table2.setItem(row_position, 2, QTableWidgetItem("Blue"))
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state: self.toggle_signal_visibility(row_position, state))  
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
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application