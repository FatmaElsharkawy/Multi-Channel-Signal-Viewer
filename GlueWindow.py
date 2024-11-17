from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from SignalGlue import SignalGlue
class GluedWindow(QMainWindow):
    def __init__(self):
        super(GluedWindow, self).__init__()
        loadUi('GluedUI.ui', self)  # Load the glued UI file
        self.setWindowTitle("Glued Window")


    def open_glue_window(self):
        # Create an instance of the SignalGlue window and show it
        self.glue_window = SignalGlue(self.signal1, self.signal2)
        self.glue_window.show()