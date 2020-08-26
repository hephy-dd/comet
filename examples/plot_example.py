"""Simple plot example using QtChart module."""

import time
import random
import sys, os

import comet
from comet import ui

class FakeDataProducer:
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

def fake_data(process):
    """Fake data generator."""
    source = FakeDataProducer()
    while process.running:
        process.emit('reading', source.read())
        time.sleep(random.uniform(.250, .500))

def main():
    app = comet.Application()
    app.title = "Plot"
    app.about = "An example plot application."

    def on_reset():
        for series in plot.series.values():
            series.clear()
        plot.fit()

    def on_reading(value):
        time, temp, humid = value
        plot.series.get("temp").append(time, temp)
        plot.series.get("humid").append(time, humid)
        if plot.zoomed:
            plot.update("x")
        else:
            plot.fit()

    plot = ui.Plot(legend="bottom")
    plot.add_axis("x", align="bottom", type="datetime")
    plot.add_axis("y1", align="left", text="Temperature [°C]", color="red")
    plot.add_axis("y2", align="right", text="Humidity [%rH]", color="blue")
    plot.add_series("temp", "x", "y1", text="Temperature", color="red")
    plot.add_series("humid", "x", "y2", text="Humidity", color="blue")

    reset_button = ui.Button(text="Reset", clicked=on_reset)

    app.layout = ui.Column(
        plot,
        reset_button
    )

    process = comet.Process(target=fake_data)
    process.reading = on_reading
    process.failed = ui.show_exception
    process.start()
    app.processes.add("process", process)

    return app.run()

if __name__ == '__main__':
    sys.exit(main())
