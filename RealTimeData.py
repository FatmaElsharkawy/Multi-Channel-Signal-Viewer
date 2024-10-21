import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QVBoxLayout
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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
        loadUi('RealTimeUI.ui', self)  # Load the UI file

        # Find the widget and set up the layout
        self.realtime_signal_view = self.findChild(QWidget, 'realtime_signal_view')
        layout = QVBoxLayout(self.realtime_signal_view)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

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
