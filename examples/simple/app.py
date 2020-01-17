"""Simple fake measuremnt example."""

import random
import time
import sys

import comet

class Measure(comet.Process):

    def run(self):
        while not self.stopRequested():
            print(self.stopRequested(), self.isAlive())
            self.push("value", random.uniform(40., 42.))
            time.sleep(random.random())

def main():
    app = comet.Application()
    app.title = "Measurement"

    def finish():
        app.get('start').enabled = True
        app.get('stop').enabled = False
        app.get("current").value = 0

    def pop(key, value):
        if key == "value":
            app.get("current").value = value

    def on_start(event):
        app.get('start').enabled = False
        app.get('stop').enabled = True
        measure = app.processes.get("measure")
        measure.start()

    def on_stop(event):
        app.get('start').enabled = False
        app.get('stop').enabled = False
        measure = app.processes.get("measure")
        measure.stop()

    measure = Measure(pop=pop, finish=finish, fail=print)
    app.processes.add("measure", measure)

    app.layout = comet.Column(
        comet.Label("Voltage"),
        comet.Number(value=42, maximum=1000, decimals=1, suffix="V"),
        comet.Label("Current"),
        comet.Number(id="current", readonly=True, value=0, maximum=1000, decimals=3, suffix="mA"),
        comet.Button(id="start", text="Start", click=on_start),
        comet.Button(id="stop", text="Stop", enabled=False, click=on_stop),
        comet.Stretch()
    )

    return app.run()

if __name__ == '__main__':
    sys.exit(main())
