"""Simple plot example using QtChart module."""

import time
import random
import sys, os

from PyQt5 import QtCore, QtWidgets

import comet

class FakeEnvironment:
    """Fake data source providing realistic temperature and humidity readings."""

    def __init__(self, temperature=25.0, humidity=50.0):
        self.time = time.time()
        self.temperature = temperature
        self.temperature_min = 10
        self.temperature_max = 120
        self.humidity = humidity
        self.humidity_min = 15
        self.humidity_max = 95

    def read(self):
        """Read data, returns time, temperature and humidity."""
        self.temperature = max(self.temperature_min, min(self.temperature_max, self.temperature + random.uniform(-1, 1)))
        self.humidity = max(self.humidity_min, min(self.humidity_max, self.humidity + random.uniform(-1, 1)))
        self.time = time.time()
        return self.time, self.temperature, self.humidity

class Plot(QtWidgets.QWidget, comet.UiLoaderMixin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadUi()
        chart =  self.ui.chartView.chart()
        chart.setTitle("Environment")
        chart.legend().setAlignment(QtCore.Qt.AlignBottom)
        self.x = chart.addDateTimeAxis(QtCore.Qt.AlignBottom)
        self.x.setTitleText("Time")
        self.y1 = chart.addValueAxis(QtCore.Qt.AlignLeft)
        self.y1.setTitleText("Temp.[°C]",)
        self.y1.setLinePen(QtCore.Qt.red)
        self.y2 = chart.addValueAxis(QtCore.Qt.AlignRight)
        self.y2.setLinePen(QtCore.Qt.blue)
        self.temp = chart.addLineSeries(self.x, self.y1)
        self.temp.setName("Temperature [°C]")
        self.temp.setColor(QtCore.Qt.red)
        self.humid = chart.addLineSeries(self.x, self.y2)
        self.humid.setName("Humidity [%rH]")
        self.humid.setColor(QtCore.Qt.blue)
        # Create data source and timing
        self.source = FakeEnvironment()
        # Create timer to update plot with new data
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read)
        self.timer.start(250)

    def read(self):
        """Read data from source and update plot."""
        time, temp, humid = self.source.read()
        self.temp.data().append(time, temp)
        self.humid.data().append(time, humid)
        # Adjust range if not zoomed
        chart = self.ui.chartView.chart()
        if not chart.isZoomed():
            chart.fit()
        else:
            # TODO
            chart.updateAxis(self.x, self.x.min(), self.x.max())

def main():
    app = comet.Application()
    window = comet.MainWindow()
    window.setCentralWidget(Plot())
    window.show()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
