# Multi-Channel-Signal-Viewer
A desktop application to view signals and manipulate them, with additional features such as non-rectangualar graph, real time plot, and signals glue.
## DEMO:


https://github.com/user-attachments/assets/ec24e819-38f9-4f47-af15-040ff51063cb



## Features:
### Signal File Browsing
### Real-Time Signal Integration
### Two main identical graphs for signal visualization.
Independent or linked operation, allowing synchronized zoom, pan, timeframes, and playback speeds.
### Dynamic Signal Visualization:
Cine mode display for all signals, simulating real-time ICU monitors.

Controls for play, pause, rewind, and customize playback speeds.

### Graph Manipulations:
Change color, add labels/titles, zoom in/out, show/hide signals.
Scroll and pan signals within boundary conditions using sliders and mouse.
Transfer signals between graphs.

### Non-Rectangular Graph:
One graph with a unique polar visualization

### Signal Glue Operation:

Combine parts of two signals from the rectangular graphs into a third graph using customizable interpolation.
Adjustable parameters: window start, size, gap, overlap, and interpolation order.

### Export & Reporting:
Generate PDF reports with snapshots and statistical data (mean, std, min, max, and duration).

## Install Dependencies:

Ensure you have Python 3.7 or above installed, and then install the following libraries:

PyQt5
pyqtgraph
ReportLab
SciPy
NumPy
Matplotlib

## Usage
Clone the repo
```python
git clone https://github.com/YoussefHassanien/Signal-Viewer.git
```

Install the following libraries
```python
pip install numpy scipy pyqt5 qtgraph reportlab
```

Navigate to project directory

Write in the command prompt run MainWindow.py






