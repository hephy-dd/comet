"""Simple fake measuremnt example."""

import random
import time
import sys

import comet

class Measure(comet.Process):

    voltage = 0

    def run(self):
        while self.running:
            self.push("reading", random.uniform(.25, 2.5) * self.voltage)
            time.sleep(random.random())

def main():
    app = comet.Application()
    app.title = "Measurement"

    def on_finish():
        app.layout.get("start").enabled = True
        app.layout.get("stop").enabled = False
        app.layout.get("current").value = 0

    def on_reading(value):
        app.layout.get("current").value = value

    def on_start():
        app.layout.get("start").enabled = False
        app.layout.get("stop").enabled = True
        measure = app.processes.get("measure")
        measure.start()

    def on_stop():
        app.layout.get("start").enabled = False
        app.layout.get("stop").enabled = False
        measure = app.processes.get("measure")
        measure.stop()

    def on_voltage(value):
        measure = app.processes.get("measure")
        measure.voltage = value

    measure = Measure(
        finished=on_finish,
        failed=app.show_exception,
        reading=on_reading
    )
    app.processes.add("measure", measure)

    app.layout = comet.Column(
        comet.Label("Voltage"),
        comet.Number(id="voltage", value=0, maximum=1000, decimals=1, suffix="V", changed=on_voltage),
        comet.Label("Current"),
        comet.Number(id="current", readonly=True, value=0, maximum=1000, decimals=3, suffix="mA"),
        comet.Button(id="start", text="Start", clicked=on_start),
        comet.Button(id="stop", text="Stop", enabled=False, clicked=on_stop),
        comet.Stretch()
    )

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
