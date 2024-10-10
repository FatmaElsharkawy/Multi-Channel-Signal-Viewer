import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from UI_file import MainWindow
from ReportGenerator import  generate_pdf

class SignalViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize the UI
        self.ui = MainWindow()
        self.ui.setupUi(self)
        
        # Set the initial file paths as None
        self.file_path = None
        self.file_extension = None
        self.real_time_signal= None


        # Connect the button click event to the function
        self.ui.upload_file.clicked.connect(self.browse_signals)
        self.ui.export_pdf.clicked.connect(self.export_pdf)
    
    @pyqtSlot()
    def browse_signals(self):
        # Open a file dialog for the user to select a signal file
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open Signal File", "", 
                                                         "Signal Files (*.edf *.csv *.hdf5)")
        if self.file_path:
            # Extract the file extension
            self.file_extension = self.file_path.split('.')[-3].lower()
            self.check_extension()
        else:
            QMessageBox.warning(self, "No file selected", "Please select a signal file to upload.")
    
    def check_extension(self):
        # Example validation for allowed file extensions
        if self.file_extension not in ['csv', 'edf', 'hdf5']:
            QMessageBox.warning(self, "Unsupported File", "The selected file type is not supported.")
        else:
            # Proceed with further processing, e.g., load the file into memory
            QMessageBox.information(self, "File Uploaded", f"File uploaded successfully: {self.file_path}")

    def export_pdf(self):
        saved_file_path, _= QFileDialog.getSaveFileName(self, 'Export PDF', "", "PDF Files (*.pdf)")
        
        if saved_file_path:
            if not file_path.endswith(".pdf"):
                file_path += ".pdf"
            # Generate and save the PDF
            generate_pdf(file_path)
    
    def get_signal_path(self):
        return self.file_path

    @staticmethod
    def connect_website():
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SignalViewerApp()
    window.show()
    sys.exit(app.exec_())