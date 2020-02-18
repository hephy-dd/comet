"""Simple UI demonstration example."""

import sys

import comet

def main():
    app = comet.Application()
    app.title = "UI Demo"

    values = ["Chapman", "Cleese", "Gilliam", "Idle", "Jones", "Palin"]

    tab1 = comet.Tab(title="Tab 1", layout=comet.Column(
        comet.Row(
            comet.Column(
                comet.FieldSet(title="Numbers", layout=comet.Column(
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
                comet.FieldSet(title="Text", layout=comet.Column(
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
            comet.Stretch(),
            stretch=(2, 2, 3)
        ),
        comet.Stretch(),
        stretch=(0, 1)
    ))

    tab2 = comet.Tab(title="Tab 2", layout=comet.Column(
        comet.Row(
            comet.FieldSet(title="List 1", layout=comet.List()),
            comet.FieldSet(title="List 2", layout=comet.List(values=values)),
            comet.FieldSet(title="List 3", layout=comet.List(values=values, enabled=False))
        ),
        comet.Stretch(),
        stretch=(0, 1)
    ))

    tab3 = comet.Tab(title="Tab 3", layout=comet.Column(
        comet.Table(id="table", header=["Key", "Value"])
    ))

    tab4 = comet.Tab(title="Tab 4", layout=comet.Column(
        comet.Tree(id="tree", header=["Key", "Value"])
    ))

    app.layout = comet.Row(
        comet.Column(
            comet.FieldSet(title="FieldSet 1", layout=comet.Column(
                comet.Button(text="Button 1"),
                comet.Button(text="Button 2", enabled=False),
                comet.Button(text="Button 3", checkable=True),
                comet.Button(text="Button 4", checkable=True, enabled=False),
                comet.Button(text="Button 5", checkable=True, checked=True)
            )),
            comet.FieldSet(title="FieldSet 2", layout=comet.Column(
                comet.CheckBox(text="CheckBox 1"),
                comet.CheckBox(text="CheckBox 2", enabled=False),
                comet.CheckBox(text="CheckBox 3", checked=True, enabled=False),
                comet.CheckBox(text="CheckBox 4", checked=True)
            )),
            comet.FieldSet(title="FieldSet 3", layout=comet.Column(
                comet.Select(),
                comet.Select(values=values),
                comet.Select(values=values, default="Cleese"),
                comet.Select(values=values, default="Cleese", enabled=False)
            )),
            comet.Stretch()
        ),
        comet.Tabs(tab1, tab2, tab3, tab4, id="tabs"),
        stretch=(2, 7)
    )

    # Populate table
    table = app.layout.get("table")
    spam = table.append(["Spam", 42])
    spam[0].checked = True
    #spam[0].enabled = False
    ham = table.append(["Ham", 41])
    ham[0].checked = True
    #ham[0].enabled = False

    # Populate tree
    tree = app.layout.get("tree")
    spam = tree.append(["Spam", 42])
    spam[0].checked = True
    spam.append(["Ham", 41])
    spam.append(["Eggs", 40])

    # Add an remove tab
    tabs = app.layout.get("tabs")
    tab = comet.Tab()
    tabs.insert(0, tab)
    tab.title = "Spam"
    tabs.remove(tab)

    app.message = "Notification message..."
    app.progress = 3, 4

    return app.run()

if __name__ == "__main__":
    sys.exit(main())
