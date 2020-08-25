"""Simple UI demonstration example."""

import random
import sys

import comet

from comet import ui

def main():
    app = comet.Application()
    app.title = "UI Demo"

    values = ["Chapman", "Cleese", "Gilliam", "Idle", "Jones", "Palin"]

    tab1 = comet.Tab(title="Tab 1", layout=comet.Column(
        comet.Row(
            comet.Column(
                comet.GroupBox(title="Numbers", layout=comet.Column(
                    comet.Label(text="Number 1"),
                    comet.Number(value=1, minimum=0, maximum=10, step=1, prefix="#"),
                    comet.Label(text="Number 2"),
                    comet.Number(value=2.345, minimum=0, maximum=10, step=.1, decimals=3, suffix="mV"),
                    comet.Label(text="Number 3"),
                    comet.Number(value=1.23, minimum=0, maximum=10, decimals=2, suffix="mA", readonly=True),
                    comet.Label(text="Number 4"),
                    comet.Number(value=4.2, minimum=0, maximum=10, decimals=1, suffix="dB", enabled=False)
                ))
            ),
            comet.Column(
                comet.GroupBox(title="Text", layout=comet.Column(
                    comet.Label(text="Text 1"),
                    comet.Text(value="Chapman"),
                    comet.Label(text="Text 2"),
                    comet.Text(value="Cleese", clearable=True),
                    comet.Label(text="Text 3"),
                    comet.Text(value="Idle", readonly=True),
                    comet.Label(text="Text 4"),
                    comet.Text(value="Palin", enabled=False)
                ))
            ),
            comet.Spacer(),
            stretch=(2, 2, 3)
        ),
        comet.Spacer(),
        stretch=(0, 1)
    ))

    def on_append():
        list1.append(f"Spam {len(list1)}")
        list1.current = list1[0]

    def on_remove():
        if list1.current is not None:
            list1.remove(list1.current)

    list1 = comet.List()
    tab2 = comet.Tab(title="Tab 2", layout=comet.Column(
        comet.Row(
            comet.GroupBox(title="List 1", layout=comet.Column(
                list1,
                comet.Button(text="&Add", clicked=on_append),
                comet.Button(text="&Remove", clicked=on_remove)
            )),
            comet.GroupBox(title="List 2", layout=comet.List(items=values)),
            comet.GroupBox(title="List 3", layout=comet.List(items=values, enabled=False))
        ),
        comet.Spacer(),
        stretch=(0, 1)
    ))

    table1 = comet.Table(header=["Key", "Value"])
    tab3 = comet.Tab(title="Tab 3", layout=comet.Column(
        table1
    ))

    tree1 = comet.Tree(header=["Key", "Value"])
    tab4 = comet.Tab(title="Tab 4", layout=comet.Column(
        tree1
    ))

    first = comet.Button(text="Click")
    scroll = comet.ScrollArea(layout=comet.Column(*[comet.CheckBox(text=f"Option {i+1}", checked=random.choice([True, False])) for i in range(64)]))
    second = comet.Column(
        scroll
    )
    tab5 = comet.Tab(title="Tab 5", layout=first)
    tab5.layout = second
    del first

    def on_changed(value):
        app.message = value

    def on_click():
        app.message = combobox1.current

    tabs = comet.Tabs(tab1, tab2, tab3, tab4, tab5)
    combobox1 = comet.ComboBox(items=values)

    app.layout = comet.Row(
        comet.Column(
            comet.GroupBox(title="GroupBox 1", layout=comet.Column(
                comet.Button(text="Button 1", clicked=on_click),
                comet.Button(text="Button 2", enabled=False),
                comet.Button(text="Button 3", checkable=True),
                comet.Button(text="Button 4", checkable=True, enabled=False),
                comet.Button(text="Button 5", checkable=True, checked=True)
            )),
            comet.GroupBox(title="GroupBox 2", layout=comet.Column(
                comet.CheckBox(text="CheckBox 1"),
                comet.CheckBox(text="CheckBox 2", enabled=False),
                comet.CheckBox(text="CheckBox 3", checked=True, enabled=False),
                comet.CheckBox(text="CheckBox 4", checked=True)
            )),
            comet.GroupBox(title="GroupBox 3", layout=comet.Column(
                comet.ComboBox(),
                combobox1,
                comet.ComboBox(items=values, current="Cleese", changed=on_changed),
                comet.ComboBox(items=values, current="Idle", enabled=False)
            )),
            comet.Spacer()
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
    tab = comet.Tab()
    tabs.insert(0, tab)
    tab.title = "Spam"
    tabs.remove(tab)

    app.message = "Notification message..."
    app.progress = 3, 4

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
