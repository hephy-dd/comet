"""Simple plot example using QtChart module."""

import time
import random
import sys, os
from PyQt5 import QtCore, QtWidgets, QtChart

import comet

class FakeEnvironment(object):
    """Fake data source providing realistic temperature and humidity readings."""

    def __init__(self, temperature=25.0, humidity=50.0):
        self.temperature = temperature
        self.temperature_min = 10
        self.temperature_max = 120
        self.humidity = humidity
        self.humidity_min = 15
        self.humidity_max = 95

    def read(self):
        """Read data, returns temperature and humidity."""
        self.temperature = max(self.temperature_min, min(self.temperature_max, self.temperature + random.uniform(-1, 1)))
        self.humidity = max(self.humidity_min, min(self.humidity_max, self.humidity + random.uniform(-1, 1)))
        return self.temperature, self.humidity

class Plot(QtWidgets.QWidget, comet.UiLoaderMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadUi()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.chart = QtChart.QChart()
        self.chart.setTitle("Environment")
        self.temperature = QtChart.QLineSeries()
        self.temperature.setName("Temperature [°C]")
        self.temperature.setColor(QtCore.Qt.red)
        self.chart.addSeries(self.temperature)
        self.humidity = QtChart.QLineSeries()
        self.humidity.setName("Humidity [%rH]")
        self.humidity.setColor(QtCore.Qt.blue)
        self.chart.addSeries(self.humidity)
        self.chart.createDefaultAxes()
        self.chart.axisX().setRange(0, 1)
        self.chart.axisX().setTitleText("Time [s]")
        self.chart.axisY().setRange(0, 180)
        self.chart.axisY().setTitleText("Temp.[°C]/Humid.[%rH]")
        self.chart.legend().setAlignment(QtCore.Qt.AlignBottom)
        self.ui.chartView.setChart(self.chart)
        self.ui.chartView.setRubberBand(QtChart.QChartView.RectangleRubberBand)
        # Custom context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.chartMenu)
        # Create data source and timing
        self.source = FakeEnvironment()
        self.time = time.time()
        self.delta = 0
        # Create timer to update plot with new data
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read)
        self.timer.start(250)

    def read(self):
        """Read data from source and update plot."""
        temperature, humidity = self.source.read()
        self.temperature.append(QtCore.QPointF(self.delta, temperature))
        self.humidity.append(QtCore.QPointF(self.delta, humidity))
        # Adjust range if not zoomed
        if not self.chart.isZoomed():
            self.chart.axisX().setRange(0, self.delta)
        self.delta += time.time() - self.time
        self.time = time.time()

    def chartMenu(self, pos):
        """Custom context menu for chart."""
        menu = QtWidgets.QMenu(self.tr("Plot menu"), self)
        resetAction = QtWidgets.QAction(self.tr("&Reset Zoom"), self)
        resetAction.triggered.connect(self.chart.zoomReset)
        menu.addAction(resetAction)
        menu.exec_(self.mapToGlobal(pos))

def main():
    app = comet.Application()
    window = comet.MainWindow()
    window.setCentralWidget(Plot())
    window.show()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
