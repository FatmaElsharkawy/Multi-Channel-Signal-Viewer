import numpy as np
from scipy import interpolate
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import sys
from pykalman import KalmanFilter  # Kalman filter implementation


class SignalGlue(QtWidgets.QWidget):
    def __init__(self, signal1, signal1_y, signal2, signal2_y):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        self.signal1 = signal1
        self.signal2 = signal2
        self.signal1_y = signal1_y
        self.signal2_y = signal2_y

        self.selected1_x = None
        self.selected2_x = None
        self.selected1_y = None
        self.selected2_y = None


        self.overlap_start = None
        self.overlap_end = None 
        self.x_gap = None

        # Create the plot for the first signal
        plot_widget_x = pg.PlotWidget(title="Signal 1")
        plot_widget_x.plot(signal1, signal1_y, pen='b')
        plot_widget_x.setXRange(0, 10)

        # Create the plot for the second signal
        plot_widget_y = pg.PlotWidget(title="Signal 2")
        plot_widget_y.plot(signal2, signal2_y, pen='r')
        plot_widget_y.setXRange(0, 10)

        # Add draggable regions for selection
        lr_x = pg.LinearRegionItem([0, 50], movable=True, brush=pg.mkBrush(150, 150, 150, 100))  # Movable region
        plot_widget_x.addItem(lr_x)

        lr_y = pg.LinearRegionItem([100, 150], movable=True, brush=pg.mkBrush(150, 50, 150, 100))  # Movable region
        plot_widget_y.addItem(lr_y)

        # Button to open combined window
        combine_button = QtWidgets.QPushButton("Combine and Adjust Gap")
        combine_button.clicked.connect(lambda: self.open_combined_window(
            int(lr_x.getRegion()[0]),
            int(lr_x.getRegion()[1] - lr_x.getRegion()[0]),
            int(lr_y.getRegion()[0]),
            int(lr_y.getRegion()[1] - lr_y.getRegion()[0]),
            gap=0  # Set a default gap value
        ))

        layout.addWidget(plot_widget_x)
        layout.addWidget(plot_widget_y)
        layout.addWidget(combine_button)

        self.setLayout(layout)
        self.setWindowTitle("Signal Selection")
        self.resize(800, 600)

    # def interpolate_signals(self,selected2_x):
    #     """
    #     Glue two signals together, handling either gap or overlap between them.
    #     Interpolates the gap if needed using interp1d.
    #     """

        
    #     if selected2_x[0]<self.selected1_x[0]:
    #         if self.selected1_x[0]<selected2_x[-1]:
                
    #             self.overlap_start=max(min(self.selected1_x),min(selected2_x))
    #             self.overlap_end=min(max(self.selected1_x),max(selected2_x))
    #             print(f"overlap_start: {self.overlap_start}, overlap_end: {self.overlap_end}")
    #             interpolation_function_signal1 = interpolate.interp1d(self.selected1_x, self.selected1_y, kind='cubic')
    #             interpolation_function_signal2 = interpolate.interp1d(selected2_x, self.selected2_y, kind='cubic')
    #             x_overlapped = np.linspace(self.overlap_start, self.overlap_end, num=int(self.overlap_end - self.overlap_start))

    #             signle_1_interpolated = interpolation_function_signal1(x_overlapped)    
    #             signle_2_interpolated = interpolation_function_signal2(x_overlapped)

    #             y_interpolated = (signle_1_interpolated + signle_2_interpolated) / 2 
    #         else:

    #             x_gap = np.linspace(selected2_x[-1], self.selected1_x[0], num=np.int16(self.selected1_x[0] ) - np.int16(selected2_x[-1]))
    #             data_x=np.concatenate([selected2_x, self.selected1_x])   
    #             data_y=np.concatenate([self.selected2_y, self.selected1_y])
    #             print(len(data_x))
    #             print(len(data_y))
    #             interpolation_function_data1 = interpolate.interp1d(data_x, data_y, kind='cubic')
    #             y_interpolated = interpolation_function_data1(x_gap)
    #     else:
    #         if selected2_x[0]<self.selected1_x[-1]:
               
    #             self.overlap_start=max(min(self.selected1_x),min(selected2_x))
    #             self.overlap_end=min(max(self.selected1_x),max(selected2_x))
    #             interpolation_function_signal1 = interpolate.interp1d(self.selected1_x, self.selected1_y, kind='quadratic')
    #             interpolation_function_signal2 = interpolate.interp1d(selected2_x, self.selected2_y, kind='quadratic')
    #             x_overlapped = np.linspace(self.overlap_start, self.overlap_end, num=int(self.overlap_end - self.overlap_start))

    #             signle_1_interpolated = interpolation_function_signal1(x_overlapped)    
    #             signle_2_interpolated = interpolation_function_signal2(x_overlapped)

    #             y_interpolated = (signle_1_interpolated + signle_2_interpolated) / 2
    #         else:
    #             x_gap = np.linspace(self.selected1_x[-1], selected2_x[0],num=(np.int16(selected2_x[0])- np.int16(self.selected1_x[-1])))
    #             data_x=np.concatenate([self.selected1_x, selected2_x])   
    #             data_y=np.concatenate([self.selected1_y, self.selected2_y])
    #             print(len(data_x))
    #             print(len(data_y))
    #             interpolation_function_data1 = interpolate.interp1d(data_x, data_y, kind='cubic')
    #             y_interpolated = interpolation_function_data1(x_gap) 

    #     return np.array(y_interpolated)   
    # 
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
        
       

    def open_glued_signal_window(self):
        """Open a new window to display the glued signal."""
        signal_window = QtWidgets.QWidget()
        signal_layout = QtWidgets.QVBoxLayout()

        # Create the plot widget for the glued signal
        plot_glued = pg.PlotWidget(title="Glued Signal")
        signal_layout.addWidget(plot_glued)

        

        # Set the layout and properties of the signal window
        signal_window.setLayout(signal_layout)
        signal_window.setWindowTitle("Glued Signal Window")
        signal_window.resize(800, 600)

        self.signal_window = signal_window
        signal_window.show()

        return signal_window 
    
    def open_combined_window(self, start_x, size_x, start_y, size_y, gap):
        combined_window = QtWidgets.QWidget()
        combined_layout = QtWidgets.QVBoxLayout()

        # Create the plot widget for both parts (signal_x and signal_y)
        plot_widget = pg.PlotWidget(title="Part X and Part Y: Same Graph")
        combined_layout.addWidget(plot_widget)

        # Cut the relevant parts of the signals
        mask1 = (self.signal1 >= start_x) & (self.signal1 <= start_x + size_x)
        mask2 = (self.signal2 >= start_y) & (self.signal2 <= start_y + size_y)

        self.selected1_x = self.signal1[mask1]
        self.selected1_y = self.signal1_y[mask1] 
        self.selected2_x = self.signal2[mask2]
        self.selected2_y = self.signal2_y[mask2]         
            
        # Plot both selected parts of the signals
        plot_widget.plot(self.selected1_x, self.selected1_y, pen='b')
        plot_widget.plot(self.selected2_x, self.selected2_y, pen='r')

        # Add a gap slider for the user to specify the gap between signals
        gap_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        gap_slider.setRange(-50, 50)  # Set range for the gap to allow negative values for overlap
        gap_slider.setValue(gap)  # Set a default value for the gap
        gap_label = QtWidgets.QLabel(f"Gap: {gap} samples")

        def update_gap_label(value):
            gap_label.setText(f"Gap: {value} samples")

        gap_slider.valueChanged.connect(update_gap_label)

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




        gap_slider.valueChanged.connect(update_movable_signal)

        # Button to create and show the glued signal
        create_glued_button = QtWidgets.QPushButton("Create and Show Glued Signal")

        # def show_glued_signal():
        #     try:
        #         # Calculate the glued signal based on the current gap
        #         # glued= self.interpolate_signals(self.selected1_x,  self.selected2_x, gap_slider.value())
        #         # Open the window to display the glued signal
        #         self.open_glued_signal_window(glued)
        #     except Exception as e:
        #         print(f"Error in gluing signals: {e}")

        # create_glued_button.clicked.connect(show_glued_signal)

        combined_layout.addWidget(gap_label)
        combined_layout.addWidget(gap_slider)
        combined_layout.addWidget(create_glued_button)

        combined_window.setLayout(combined_layout)
        combined_window.setWindowTitle("Adjust Gap and Glue Signals")
        combined_window.resize(800, 600)
        combined_window.show()

        # Keep a reference to prevent the window from closing
        self.combined_window = combined_window

        return combined_window  # Return the window reference


        create_glued_button.clicked.connect(show_glued_signal)

        combined_layout.addWidget(gap_label)
        combined_layout.addWidget(gap_slider)
        combined_layout.addWidget(create_glued_button)

        combined_window.setLayout(combined_layout)
        combined_window.setWindowTitle("Adjust Gap and Glue Signals")
        combined_window.resize(800, 600)
        combined_window.show()

        # Keep a reference to prevent the window from closing
        self.combined_window = combined_window

        return combined_window  # Return the window reference






        create_glued_button.clicked.connect(show_glued_signal)

        combined_layout.addWidget(gap_label)
        combined_layout.addWidget(gap_slider)
        combined_layout.addWidget(create_glued_button)  # Add the button to the layout

        combined_window.setLayout(combined_layout)
        combined_window.setWindowTitle("Adjust Gap and Glue Signals")
        combined_window.resize(800, 600)
        combined_window.show()

        # Keep a reference to prevent the window from closing
        self.combined_window = combined_window

        return combined_window  # Return the window reference
