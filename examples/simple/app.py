"""Simple fake measurement example."""

import random
import time
import sys

import comet

def measure(process):
    while process.running:
        voltage = process.get('voltage', 0)
        process.events.reading(random.uniform(.25, 2.5) * voltage)
        process.set('voltage', voltage)
        time.sleep(random.random())

def main():
    app = comet.Application()
    app.title = "Measurement"

    def on_finish():
        app.layout.get("start").enabled = True
        app.layout.get("stop").enabled = False
        app.layout.get("current").value = 0

    def on_reading(value):
        print(value)
        app.layout.get("current").value = value

    def on_start():
        app.layout.get("start").enabled = False
        app.layout.get("stop").enabled = True
        process = app.processes.get("measure")
        process.start()

    def on_stop():
        app.layout.get("start").enabled = False
        app.layout.get("stop").enabled = False
        process = app.processes.get("measure")
        process.stop()

    def on_voltage(value):
        process = app.processes.get("measure")
        process.set('voltage', value)

    process = comet.Process(
        target=measure,
        events=dict(
            finished=on_finish,
            failed=comet.show_exception,
            reading=on_reading
        )
    )
    app.processes.add("measure", process)

    app.layout = comet.Column(
        comet.Label("Voltage"),
        comet.Number(id="voltage", value=0, minimum=0, maximum=1000, decimals=1, suffix="V", changed=on_voltage),
        comet.Label("Current"),
        comet.Number(id="current", readonly=True, value=0, decimals=3, suffix="mA"),
        comet.Button(id="start", text="Start", clicked=on_start),
        comet.Button(id="stop", text="Stop", enabled=False, clicked=on_stop),
        comet.Stretch()
    )

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
