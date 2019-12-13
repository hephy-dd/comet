"""Simple plot example using QtChart module."""

import time
import random
import sys, os
from PyQt5 import QtCore, QtWidgets, QtChart

import comet

class FakeEnvironment(object):
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
        plot = self.ui.plotWidget
        plot.chart().setTitle("Environment")
        plot.chart().legend().setAlignment(QtCore.Qt.AlignBottom)
        self.x = plot.addDateTimeAxis("Time", QtCore.Qt.AlignBottom)
        self.y1 = plot.addValueAxis("Temp.[°C]", QtCore.Qt.AlignLeft, color=QtCore.Qt.red)
        self.y2 = plot.addValueAxis("Humid.[%rH]", QtCore.Qt.AlignRight, color=QtCore.Qt.blue)
        self.temp = plot.addLineSeries("Temperature [°C]", x=self.x, y=self.y1, color=QtCore.Qt.red)
        self.humid = plot.addLineSeries("Humidity [%rH]", x=self.x, y=self.y2, color=QtCore.Qt.blue)
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
        plot = self.ui.plotWidget
        if not plot.chart().isZoomed():
            plot.fit()
        else:
            # TODO
            plot.updateAxis(self.x, self.x.min(), self.x.max())

def main():
    app = comet.Application()
    window = comet.MainWindow()
    window.setCentralWidget(Plot())
    window.show()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
