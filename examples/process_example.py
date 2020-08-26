import random
import time
import sys

import comet
from comet import ui

def main():
    app = comet.Application()

    def on_activated(item):
        ui.show_info(text=format(item.value))

    def on_selected(item):
        print("Item", format(item.value))

    table = ui.Table()
    table.header = "Name", "Status", "HV", "Current", "Temp.", "Calib."
    table.stretch = True
    table.activated = on_activated
    table.selected = on_selected
    for i in range(10):
        table.append([
            f"Unnamed{i}",
            "OK",
            "",
            "n/a",
            "n/a",
            f"{random.random()*1000:.0f} ohm"
        ])
        # First column user checkable
        table[i][0].checkable = True
        table[i][0].checked = random.choice([True, False])
        # First column editabled
        table[i][0].readonly = False

    table.qt.setCurrentItem(table[0][0].qt)
    table.fit()

    def on_activated(index, item):
        ui.show_info(text=format(item[index].value))

    def on_selected(item):
        print("Item", format(item[0].value))

    tree = ui.Tree()
    tree.header = "Measurement", "Status"
    tree.activated = on_activated
    tree.selected = on_selected
    tree.append(["Flute 1", "OK"])
    tree.clear()
    tree.append(["Flute 2", "OK"])
    tree.insert(0, ["Flute 3", "Meas..."])
    tree[0][0].checked = True
    tree[0][1].color = "red"
    tree[0][1].background = "blue"
    #tree[0][1].color = None
    tree[0][1].background = None

    tree.append(["Flute 4", "OK"])
    tree.append(["Flute 5", "OK"])
    tree.append(["Flute 6"])

    tree.qt.setCurrentItem(tree[2].qt)

    tree.remove(tree[3])

    for i, item in enumerate(tree):
        if i == 1:
            item.expanded = True
        item[0].checked = True
        item.append(["Test 1", "OK"])
        item.append(["Test 2", "OK"])
        item.insert(0, ["Test 3", "OK"])
        item.children[0][0].checked = True
        item.children[1][0].checked = False
        item.children[2][0].checked = True

    for item in tree:
        print(item[0].checked)
        for item in item.children:
            print(item[0].checked)

    def measure(process):
        while process.running:
            for i in range(10):
                value = random.choice([True, False])
                process.emit('hv', i, value)
                value = random.uniform(22., 24.)
                process.emit('temp', i, value)
            for i in range(2):
                value = random.choice(["OK", "FAIL"])
                process.emit('status', i, value)
            time.sleep(1)

    def on_hv(i, value):
        item = table[i][2]
        if table[i][0].checked:
            item.value = {True: "ON", False: "OFF"}[value]
            item.color = {True: "green", False: "red"}[value]
            item.bold = not value
        else:
            item.value = None

    def on_temp(i, value):
        item = table[i][4]
        if table[i][0].checked:
            item.value = value
            item.color = "green"
            if item.value < 22.5:
                item.color = "red"
        else:
            item.value = None

    def on_status(i, value):
        color = {"OK": "green", "FAIL": "red"}[value]
        tree[i][1].value = value
        tree[i][1].color = color
        tree[i][1].bold = value == "FAIL"
        for item in tree[i].children:
            if item[0].checked:
                item[1].value = value
                item[1].color = color
                item[1].bold = value == "FAIL"
            else:
                item[1].value = None

    app.layout = ui.Column(
        table,
        tree
    )

    process = comet.Process(target=measure)
    process.hv = on_hv
    process.temp = on_temp
    process.status = on_status
    app.processes.add("process", process)
    process.start()

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
