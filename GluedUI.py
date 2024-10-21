from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
import sys
import numpy as np

class GluedUI(QMainWindow):
    def __init__(self):
        super(GluedUI, self).__init__()
        loadUi("GluedUI.ui", self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GluedUI()
    window.show()
    sys.exit(app.exec_())  # Use sys.exit to properly exit the application