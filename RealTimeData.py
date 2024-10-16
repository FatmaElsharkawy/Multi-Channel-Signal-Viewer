# import requests
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

# class RealTimeSignalViewer(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.layout = QVBoxLayout()
#         self.label = QLabel("Waiting for real-time signal...")
#         self.layout.addWidget(self.label)
#         self.setLayout(self.layout)
        
#         # You can add more UI components here for visualization

#     def fetch_signal(self):
#         """Fetch real-time signal data from a website."""
#         url = "https://example.com/api/signal"  # Replace with the actual URL
#         try:
#             response = requests.get(url)
#             response.raise_for_status()  # Raise an error for bad responses
#             signal_data = response.json()  # Assuming the response is JSON
#             self.update_display(signal_data)  # Update the display with the fetched data
#         except Exception as e:
#             print(f"Error fetching signal: {e}")

#     def update_display(self, signal_data):
#         """Update the UI with the fetched signal data."""
#         # Update the label or other UI components with the new data
#         self.label.setText(f"Latest Signal: {signal_data['value']}")  # Adjust based on your data structure


import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.dates as mdates
import datetime
import time
import threading

class RealTimePlot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = []

    def initUI(self):
        self.setWindowTitle('Real-Time BTC-USD Price')
        self.setGeometry(100, 100, 800, 600)
        
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout(main_widget)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
        
        threading.Thread(target=self.update_data, daemon=True).start()

    def update_data(self):
        while True:
            price = self.fetch_price()
            if price:
                current_time = datetime.datetime.now()
                self.data.append((current_time, price))
                self.data = self.data[-100:]  # Keep only the last 100 points
                self.update_plot()
            time.sleep(5)

    def fetch_price(self):
        url = 'https://api.pro.coinbase.com/products/BTC-USD/ticker'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return float(data['price'])
        return None

    def update_plot(self):
        times, prices = zip(*self.data)
        self.ax.clear()
        self.ax.plot(times, prices, 'ro-')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    real_time_plot = RealTimePlot()
    real_time_plot.show()
    sys.exit(app.exec_())
