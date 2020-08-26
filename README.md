# COMET

Control and Measurement Toolkit (COMET)

A [Qutie](https://github.com/arnobaer/qutie) powered rapid development
tool for creating graphical measurement desktop applications for scientific
laboratory use. Inspired by
[QCoDeS](https://github.com/QCoDeS/Qcodes),
[Lantz](https://github.com/LabPy/lantz),
[Slave](https://github.com/p3trus/slave),
[FluidLab](https://github.com/fluiddyn/fluidlab) and
[Dash](https://github.com/plotly/dash).

See the documentation on https://hephy-dd.github.io/comet/

## Install

Install from GitHub using pip

```bash
pip install git+https://github.com/hephy-dd/comet.git@0.11.0
```

## Quick start

The following minimal example registers a VISA compatible instrument, a callback
action and invokes the application's main window providing a layout with a text
field and a button.

```python
import comet
from comet import ui

# Create application
app = comet.Application("example")
app.title = "Example"
app.width = 460
app.height = 240

# Register resources
app.resources.add("res", comet.Resource("ASRL2::INSTR", visa_library="@sim"))

# Load persistent settings
app.devices.load_settings()

# Define a callback
def on_update():
    with app.resources.get("res") as res:
        instr = comet.IEC60488(res)
        text.value = instr.identification

# Create UI layout
text = ui.Text(readonly=True)
button = ui.Button(text="Read IDN", clicked=on_update)
app.layout = ui.Column(
    ui.Row(
        text_field,
        button
    ),
    ui.Stretch()
)

# Run event loop
app.run()
```

## License

COMET is licensed under the [GNU General Public License Version 3](https://github.com/hephy-dd/comet/tree/master/LICENSE).
