---
layout: default
title: Home
nav_order: 1
permalink: /
---

# COMET - Control and Measurement Toolkit

A PyQt5 powered rapid development tool for creating graphical measurement desktop applications
for scientific laboratory use. Inspired by [QCoDeS](https://github.com/QCoDeS/Qcodes),
[Lantz](https://github.com/LabPy/lantz), [Slave](https://github.com/p3trus/slave),
[FluidLab](https://github.com/fluiddyn/fluidlab) and [Dash](https://github.com/plotly/dash){: .fs-6 .fw-300 }

[Get started now](#getting-started){: .btn .btn-blue .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/hephy-dd/comet){: .btn .fs-5 .mb-4 .mb-md-0 }

## Getting started

### Dependencies

COMET depends on [PyVISA](https://pyvisa.readthedocs.io/en/latest/) for instrument
communication and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) for the
graphical user interface. COMET works on Linux and Windows operating systems.

### Install

Install from GitHub using pip

```bash
pip install git+https://github.com/hephy-dd/comet.git@0.9.0
```

### Quick start

COMET provides a basic application window and a set of modules for instrument
communication and threaded processes.

The following minimal example registers a VISA compatible instrument, a callback
action and invokes the application's main window providing a layout with a text
field and a button.

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
      app.layout.get("idn").value = iec.identification

# Create UI layout
app.layout = comet.Column(
    comet.Row(
        comet.Text(id="idn", readonly=True),
        comet.Button(text="Read IDN", click=on_update)
    ),
    comet.Stretch()
)

# Run event loop
app.run()
```

![Example application](static/example.png)

## About the project

COMET is &copy; 2019-2020 by [Bernhard Arnold](https://github.com/arnobaer/).

### License

COMET is licensed under the [GNU General Public License Version 3](https://github.com/hephy-dd/comet/tree/master/LICENSE).
