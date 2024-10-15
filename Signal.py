from PyQt5.QtWidgets import QColorDialog, QPushButton, QMainWindow
from PyQt5.QtGui import QColor,QBrush
import pandas as pd
from Graph import Graph 
 

# from SignalViewerApp import SignalViewerApp 

class Signal():
    signals_num_graph1, signals_num_graph2= 0,0
    row_signal_map_1= {} #row_signal_map[row]= signal
    row_signal_map_2= {} 
   
    def __init__(self, graph_num, csv_path= 'rec_1r.csv'):
        super().__init__()
        self.csv_path = csv_path
        csvFile = pd.read_csv(self.csv_path)   

        self.signal_data_time = csvFile.iloc[:, 0].values
        self.signal_data_amplitude = csvFile.iloc[:, 1].values
        self.signal_type= None
        self.color= "blue" 
        self.speed=None
        self.visible= True
        self.graph_num= graph_num

        
        if graph_num ==1: 
            Signal.signals_num_graph1 +=1 
            self.signal_num= Signal.signals_num_graph1
        elif graph_num==2:
            Signal.signals_num_graph2 +=1 
            self.signal_num= Signal.signals_num_graph2
        
        self.label=f"Signal{self.signal_num}"
        
        print(self.label, self.signal_num)

    def change_color(self,current_row):
        print("aafter")
        if current_row >= 0:
            # Get the graph_number of the selected signal
            selected_color = QColorDialog.getColor()


        
            if selected_color.isValid():  # Check if a valid color was selected
                
                color_name = selected_color.name()
                 
                self.row_signal_map_1[current_row].color= color_name

    def set_visible(self,visible):
        self.visible= visible

    def set_color(self,new_color):  
        self.color=new_color 
    def set_label(self,new_label):  
        self.label=new_label

# signal = Signal()

# # Generate example signal data (Sine wave)
# signal.signal_data = np.sin(np.linspace(0, 2 * np.pi, 1000))  # Example signal data: sine wave

# # Change the color and label of the signal
# signal.change_color('green')  # Set the signal color to green
# signal.add_label('Sine ')  # Set the signal label to "Sine Wave"

# # Plot the signal using the updated color and label
# plt.plot(signal.signal_data, color=signal.color, label=signal.label)
# plt.title(f"{signal.label} Signal")
# plt.xlabel("Time")
# plt.ylabel("Amplitude")
# plt.legend()
# plt.show()