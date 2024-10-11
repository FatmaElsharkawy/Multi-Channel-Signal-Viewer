from PyQt5.QtWidgets import QColorDialog, QPushButton, QMainWindow
from PyQt5.QtGui import QColor
import pandas as pd

# from SignalViewerApp import SignalViewerApp 

class Signal():

    def __init__(self):
        super().__init__()
        
        self.cvs_file_name = 'rec_1r.csv'
        csvFile = pd.read_csv(self.cvs_file_name)   

        self.signal_data_time = csvFile.iloc[:, 0].values
        self.signal_data_amplitude = csvFile.iloc[:, 1].values
        
        self.signal_type= None
        self.color= "blue" 
        self.speed=None
        self.label="Signal"
        
        #self.ui = Ui_signalViewer()
        # self.ui.setupUi(self)
        
        print("before")

    def change_color(self):
        print("aafter")
        selected_color = QColorDialog.getColor()
        if selected_color.isValid():  # Check if a valid color was selected
            color_name = selected_color.name()  # Get the color name (e.g., #ff0000)
            # Use self.ui.color_push_button to reference the button through the ui attribute
            self.color = color_name  # Update the signal color
            print(self.color)
        
    def add_label(self,new_label):
        
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