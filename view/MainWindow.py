from model import Signal
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton
from PyQt5.uic import loadUi
import sys
class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("MainWindow.ui", self)
        self.signal_params=Signal()
        self.color_push_button =self.findChild(QPushButton, "color_push_button")

        self.color_push_button.clicked.connect(self.signal_params.change_color) 


                     

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application
