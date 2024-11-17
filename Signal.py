from PyQt5.QtWidgets import QColorDialog, QPushButton, QMainWindow
from PyQt5.QtGui import QColor,QBrush
import pandas as pd
from Graph import Graph 

class Signal:
    def __init__(self, graph_num,csv_path= 'mmg_healthy.csv'):
        self.csv_path = csv_path
        csvFile = pd.read_csv(self.csv_path)   
        self.signal_data_time = csvFile.iloc[:, 0].values
        self.signal_data_amplitude = csvFile.iloc[:, 1].values
        self.color= None
        self.visible= True
        self.graph_num= graph_num
        self.signal_num= 0
        self.label=None

    def change_color(self,current_row, graph):
        if current_row >= 0:
            selected_color = QColorDialog.getColor()
            if selected_color.isValid():  # Check if a valid color was selected
                color_name = selected_color.name()
                signal= graph.signals_list[current_row]
                signal.set_color(color_name)

    
    def set_visiblity(self,visible):
        self.visible= visible

    def get_visiblity(self):
        return self.visible

    def set_color(self,new_color):  
        self.color=new_color 
    
    def set_label(self,new_label):  
        self.label=new_label

    def get_label(self):
        return f"Signal{self.signal_num +1 }"
    
    def set_signal_num(self, new_num):
        self.signal_num = new_num
    
    def set_signal_graph_num(self, new_graph_num):
        self.graph_num = new_graph_num

   