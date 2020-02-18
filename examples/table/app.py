import random
import time
import sys

import comet

def main():
    app = comet.Application()

    app.layout = comet.Column(
        comet.Table(
            id="table",
            stretch=True,
            header=["Name", "Status", "HV", "Current", "Temp.", "Calib."]
        ),
        comet.Tree(
            id="tree",
            header=["Measurement", "Status"]
        )
    )

    def on_entered(item):
        comet.show_info("Item", format(item.value))

    table = app.get("table")
    table.entered = on_entered
    for i in range(10):
        table.append([
            f"Unnamed{i}",
            "OK",
            "",
            "n/a",
            "n/a",
            "1200 ohm"
        ])
        table[i][0].checked = random.choice([True, False])
        table[i][0].readonly = True

    table.fit()

    tree = app.get("tree")
    tree.append(["Flute 1", "OK"])
    tree.clear()
    tree.append(["Flute 2", "OK"])
    tree.insert(0, ["Flute 3", "Meas..."])
    tree[0][0].checked = True
    tree[0][1].color = "red"
    tree[0][1].background = "blue"
    #tree[0][1].color = None
    tree[0][1].background = None

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


    class Process(comet.Process):

        def run(self):
            while self.running:
                for i in range(10):
                    value = random.choice([True, False])
                    self.push("hv", i, value)
                    value = random.uniform(22., 24.)
                    self.push("temp", i, value)
                for i in range(2):
                    value = random.choice(["OK", "FAIL"])
                    self.push("status", i, value)
                time.sleep(1)

    def on_hv(i, value):
        item = table[i][2]
        if table[i][0].checked:
            item.value = {True: "ON", False: "OFF"}[value]
            item.color = {True: "green", False: "red"}[value]
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
        color = {"OK":"green","FAIL":"red"}[value]
        tree[i][1].value = value
        tree[i][1].color = color
        for item in tree[i].children:
            if item[0].checked:
                item[1].value = value
                item[1].color = color
            else:
                item[1].value = None

    process = app.processes.add("Process", Process(
        hv=on_hv,
        temp=on_temp,
        status=on_status,
    ))
    process.start()

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
