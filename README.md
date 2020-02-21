# COMET

Control and Measurement Toolkit (COMET)

A PyQt5 powered rapid development tool for creating graphical measurement desktop applications,
inspired by [QCoDeS](https://github.com/QCoDeS/Qcodes), [Lantz](https://github.com/LabPy/lantz),
[Slave](https://github.com/p3trus/slave), [FluidLab](https://github.com/fluiddyn/fluidlab) and
[Dash](https://github.com/plotly/dash).

See the documentation on https://hephy-dd.github.io/comet/

## Install

Install from GitHub using pip

```bash
pip install git+https://github.com/hephy-dd/comet.git@0.8.0
```

## Quick start

The following minimal example registers a VISA compatible device, a callback
action and invokes the application's main window containing a text field and a button.

```python
import comet

# Create application
app = comet.Application()
app.title = "Example"
app.width = 460
app.height = 240

# Register IEC compliant device, load optional settings
app.devices.add("iec", comet.IEC60488(
  comet.Resource("ASRL2::INSTR", visa_library="@sim")
))
app.devices.load_settings()

# Define a callback
def on_update():
  with app.devices.get("iec") as iec:
      app.layout.get('idn').value =  iec.identification

# Create UI layout
app.layout = comet.Column(
    comet.Row(
        comet.Text(id="idn", readonly=True),
        comet.Button(text="Read IDN", click=on_update)
    ),
    comet.Stretch()
)

# Run application
app.run()
```

## License

COMET is licensed under the [GNU General Public License Version 3](https://github.com/hephy-dd/comet/tree/master/LICENSE).
