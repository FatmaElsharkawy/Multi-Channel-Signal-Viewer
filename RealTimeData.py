import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import time
import threading

class RealTimePlot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Real-Time Window")
        self.data = []

    def initUI(self):
        loadUi('RealTimeUI.ui', self)  # Load the UI file

        # Find the widget and set up the layout
        self.realtime_signal_view = self.findChild(QWidget, 'realtime_signal_view')
        layout = QVBoxLayout(self.realtime_signal_view)

        # Add message label
        self.message_label = QLabel("Please wait until the response from the website")
        self.message_label.setStyleSheet("color: white;")
        layout.addWidget(self.message_label)

        self.figure = Figure(facecolor='black')  # Set figure background to black
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('black')  # Set the axis background to black
        self.ax.tick_params(axis='x', colors='white')  # X-axis tick color
        self.ax.tick_params(axis='y', colors='white')  # Y-axis tick color

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')

        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))

        threading.Thread(target=self.update_data, daemon=True).start()

    def format_y(self, y, pos):
        return f'{y/1000:.3f}'

    def update_data(self):
        self.show_message("Please wait until the response from the website")

        while True:
            price = self.fetch_price()
            if price:
                self.hide_message()
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
        self.ax.set_facecolor('black')  # Ensure background stays black
        self.figure.patch.set_facecolor('black')  # Set figure background to black
        self.ax.plot(times, prices, 'bo-')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))
        self.ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_y))

        # Add axis labels with custom font properties
        self.ax.set_xlabel('Time', fontsize=14, fontweight='bold', color='white')
        self.ax.set_ylabel('Price * (10^3)', fontsize=14, fontweight='bold', color='white')

        self.ax.spines['bottom'].set_color('white')  # X-axis line color
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')  # Y-axis line color
        self.ax.spines['right'].set_color('white')

        self.ax.tick_params(axis='x', colors='white')  # X-axis tick color
        self.ax.tick_params(axis='y', colors='white')  # Y-axis tick color

        self.canvas.draw()

    def show_message(self, message):
        self.message_label.setText(message)
        self.message_label.show()

    def hide_message(self):
        self.message_label.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    real_time_plot = RealTimePlot()
    real_time_plot.show()
    sys.exit(app.exec_())