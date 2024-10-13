import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QPoint
from PyQt5.uic import loadUi
import icons.icons_rc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('MainWindowUI.ui', self)  
        
        #Changing the color of the graph
        self.signals_info_table2 = self.findChild(QTableWidget, "tableWidget_C2")
        self.signals_info_table2.setColumnCount(4)
        self.signals_info_table2.setHorizontalHeaderLabels(["Signal", "Graph No", "Color", "Visibility"])     
        self.signals_info_table2.horizontalHeader().sectionClicked.connect(self.show_colors2)

        self.signals_info_table1 = self.findChild(QTableWidget, "tableWidget_C1")
        self.signals_info_table1.setColumnCount(4)
        self.signals_info_table1.setHorizontalHeaderLabels(["Signal", "Graph No", "Color", "Visibility"])     
        self.signals_info_table1.horizontalHeader().sectionClicked.connect(self.show_colors1)
    
    def show_colors2(self, column):
        if column == 2:  # Color column
            # Open color dialog
            color = QColorDialog.getColor()
            if color.isValid():
                # Add the selected color to the table in the "Color" column
                row_count = self.signals_info_table2.rowCount()
                self.signals_info_table2.insertRow(row_count)  # Add a new row
                self.signals_info_table2.setItem(row_count, column, QTableWidgetItem("Color"))  # Placeholder text
                self.signals_info_table2.item(row_count, column).setBackground(color)

    def show_colors1(self, column):
        if column == 2:  # Color column
            # Open color dialog
            color = QColorDialog.getColor()
            if color.isValid():
                # Add the selected color to the table in the "Color" column
                row_count = self.signals_info_table1.rowCount()
                self.signals_info_table1.insertRow(row_count)  # Add a new row
                self.signals_info_table1.setItem(row_count, column, QTableWidgetItem("Color"))  # Placeholder text
                self.signals_info_table1.item(row_count, column).setBackground(color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())        
        