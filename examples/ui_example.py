"""Simple UI demonstration example."""

import random
import sys

import comet
from comet import ui

def main():
    app = comet.Application()
    app.title = "UI Demo"
    app.width = 1200
    app.height = 300
    app.window.minimum_size = 1000, 300
    app.window.maximum_width = 1400

    values = ["Chapman", "Cleese", "Gilliam", "Idle", "Jones", "Palin"]

    tab1 = ui.Tab(title="Tab 1", layout=ui.Column(
        ui.Row(
            ui.Column(
                ui.GroupBox(title="Numbers", layout=ui.Column(
                    ui.Label(text="Number 1"),
                    ui.Number(value=1, minimum=0, maximum=10, step=1, prefix="#"),
                    ui.Label(text="Number 2"),
                    ui.Number(value=2.345, minimum=0, maximum=10, step=.1, decimals=3, suffix="mV"),
                    ui.Label(text="Number 3"),
                    ui.Number(value=1.23, minimum=0, maximum=10, decimals=2, suffix="mA", readonly=True),
                    ui.Label(text="Number 4"),
                    ui.Number(value=4.2, minimum=0, maximum=10, decimals=1, suffix="dB", enabled=False)
                ))
            ),
            ui.Column(
                ui.GroupBox(title="Text", layout=ui.Column(
                    ui.Label(text="Text 1"),
                    ui.Text(value="Chapman"),
                    ui.Label(text="Text 2"),
                    ui.Text(value="Cleese", clearable=True),
                    ui.Label(text="Text 3"),
                    ui.Text(value="Idle", readonly=True),
                    ui.Label(text="Text 4"),
                    ui.Text(value="Palin", enabled=False)
                ))
            ),
            ui.Spacer(),
            stretch=(2, 2, 3)
        ),
        ui.Spacer(),
        stretch=(0, 1)
    ))

    def on_append():
        list1.append(f"Spam {len(list1)}")
        list1.current = list1[0]

    def on_remove():
        if list1.current is not None:
            list1.remove(list1.current)

    list1 = ui.List()
    tab2 = ui.Tab(title="Tab 2", layout=ui.Column(
        ui.Row(
            ui.GroupBox(title="List 1", layout=ui.Column(
                list1,
                ui.Button(text="&Add", clicked=on_append),
                ui.Button(text="&Remove", clicked=on_remove)
            )),
            ui.GroupBox(title="List 2", layout=ui.List(items=values)),
            ui.GroupBox(title="List 3", layout=ui.List(items=values, enabled=False))
        ),
        ui.Spacer(),
        stretch=(0, 1)
    ))

    table1 = ui.Table(header=["Key", "Value"])
    tab3 = ui.Tab(title="Tab 3", layout=ui.Column(
        table1
    ))

    tree1 = ui.Tree(header=["Key", "Value"])
    tab4 = ui.Tab(title="Tab 4", layout=ui.Column(
        tree1
    ))

    first = ui.Button(text="Click")
    scroll = ui.ScrollArea(layout=ui.Column(*[ui.CheckBox(text=f"Option {i+1}", checked=random.choice([True, False])) for i in range(64)]))
    second = ui.Column(
        scroll
    )
    tab5 = ui.Tab(title="Tab 5", layout=first)
    tab5.layout = second
    del first

    tab6 = ui.Tab(title="Tab 6", layout=ui.Row(
        ui.Column(
            ui.Label("Metric 1"),
            ui.Metric('V', decimals=3, changed=lambda value: print(value)),
            ui.Label("Metric 2"),
            ui.Metric('A', prefixes='munp', changed=lambda value: print(value)),
            ui.Spacer()
        ),
        ui.Spacer(),
        stretch=(1, 2)
    ))

    def on_changed(value):
        app.message = value

    def on_click():
        app.message = combobox1.current

    tabs = ui.Tabs(tab1, tab2, tab3, tab4, tab5, tab6)
    combobox1 = ui.ComboBox(items=values)

    app.layout = ui.Row(
        ui.Column(
            ui.GroupBox(title="GroupBox 1", layout=ui.Column(
                ui.Button(text="Button 1", clicked=on_click),
                ui.Button(text="Button 2", enabled=False),
                ui.Button(text="Button 3", checkable=True),
                ui.Button(text="Button 4", checkable=True, enabled=False),
                ui.Button(text="Button 5", checkable=True, checked=True)
            )),
            ui.GroupBox(title="GroupBox 2", layout=ui.Column(
                ui.CheckBox(text="CheckBox 1"),
                ui.CheckBox(text="CheckBox 2", enabled=False),
                ui.CheckBox(text="CheckBox 3", checked=True, enabled=False),
                ui.CheckBox(text="CheckBox 4", checked=True)
            )),
            ui.GroupBox(title="GroupBox 3", layout=ui.Column(
                ui.ComboBox(),
                combobox1,
                ui.ComboBox(items=values, current="Cleese", changed=on_changed),
                ui.ComboBox(items=values, current="Idle", enabled=False)
            )),
            ui.Spacer()
        ),
        tabs,
        stretch=(2, 7)
    )

    # Populate table
    spam = table1.append(["Spam", 42])
    spam[0].checked = True
    #spam[0].enabled = False
    ham = table1.append(["Ham", 41])
    ham[0].checked = True
    #ham[0].enabled = False

    # Populate tree
    spam = tree1.append(["Spam", 42])
    spam[0].checked = True
    spam.append(["Ham", 41])
    spam.append(["Eggs", 40])

    # Add an remove tab
    tab = ui.Tab()
    tabs.insert(0, tab)
    tab.title = "Spam"
    tabs.remove(tab)

    app.message = "Notification message..."
    app.progress = 3, 4

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
