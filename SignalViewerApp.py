import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from Signal import Signal
class SignalViewerApp():
    def __init__(self):
        
        #global ui_instance
        # Initialize the UI
        # self.ui = MainWindow()
        # self.ui.setupUi(self)
        # ui_instance = self.ui 
        # Set the initial file paths as None
        self.file_path_list = []
        self.file_path=None
        self.file_extension = None


        # Connect the button click event to the function
        # Ui_signalViewer.upload_file.clicked.connect(self.browse_signals)
        # Ui_signalViewer.export_pdf.clicked.connect(self.export_pdf)
    
    @pyqtSlot()
    def browse_signals(self):
        # Open a file dialog for the user to select a signal file
        self.file_path, _ = QFileDialog.getOpenFileName(None, "Open Signal File", "", 
                                                         "Signal Files (*.edf *.csv *.hdf5)")
        if self.file_path:
            # Extract the file extension
            self.file_extension = self.file_path.split('.')[-1].lower()
            if self.check_extension():
                return self.file_path,
        else:
            QMessageBox.warning(None, "No file selected", "Please select a signal file to upload.")
    
    def check_extension(self):
        # Example validation for allowed file extensions
        if self.file_extension not in ['csv', 'edf', 'hdf5']:
            QMessageBox.warning(None, "Unsupported File", "The selected file type is not supported.")
        else:
            # Proceed with further processing, e.g., load the file into memory
            #QMessageBox.information(None, "File Uploaded", f"File uploaded successfully: {self.file_path}")
            self.file_path_list.append(self.file_path)
            return True
            

    def export_pdf(self):
        saved_file_path, _= QFileDialog.getSaveFileName(None, 'Export PDF', "", "PDF Files (*.pdf)")
        
        if saved_file_path:
            if not file_path.endswith(".pdf"):
                file_path += ".pdf"
            # Generate and save the PDF
            # generate_pdf(file_path)
    
    def get_signal_path(self, signal_num):
        if  isinstance(signal_num, int):
            return self.file_path_list[signal_num-1]

    

