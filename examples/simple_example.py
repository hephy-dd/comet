"""Simple fake measurement example."""

import random
import time
import sys

import comet
from comet import ui

def measure(process):
    while process.running:
        voltage = process.get('voltage', 0)
        process.emit('reading', random.uniform(.25, 2.5) * voltage)
        process.set('voltage', voltage)
        time.sleep(random.random())

def main():
    app = comet.Application()
    app.title = "Measurement"

    def on_finish():
        start_button.enabled = True
        stop_button.enabled = False
        current_number.value = 0

    def on_reading(value):
        print(value)
        current_number.value = value

    def on_start():
        start_button.enabled = False
        stop_button.enabled = True
        process = app.processes.get("measure")
        process.start()

    def on_stop():
        start_button.enabled = False
        stop_button.enabled = False
        process = app.processes.get("measure")
        process.stop()

    def on_voltage(value):
        process = app.processes.get("measure")
        process.set('voltage', value)

    process = comet.Process(target=measure)
    process.finished = on_finish
    process.failed = ui.show_exception
    process.reading = on_reading
    app.processes.add("measure", process)

    voltage_number = ui.Number(value=0, minimum=0, maximum=1000, decimals=1, suffix="V", changed=on_voltage)
    current_number = ui.Number(readonly=True, value=0, decimals=3, suffix="mA", stylesheet="color: red")
    start_button = ui.Button(text="Start", clicked=on_start)
    stop_button = ui.Button(text="Stop", enabled=False, clicked=on_stop)

    l = ui.Column(
        ui.Label("Voltage"),
        voltage_number,
        ui.Label("Current"),
        current_number,
        start_button,
        stop_button,
        ui.Spacer()
    )
    app.layout = l

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
