---
layout: default
title: Home
nav_order: 1
permalink: /
---

# COMET - Control and Measurement Toolkit

A PyQt5 powered rapid development tool for creating graphical measurement desktop applications,
inspired by [QCoDeS](https://github.com/QCoDeS/Qcodes), [Lantz](https://github.com/LabPy/lantz),
[Slave](https://github.com/p3trus/slave), [FluidLab](https://github.com/fluiddyn/fluidlab) and
[Dash](https://github.com/plotly/dash).{: .fs-6 .fw-300 }

[Get started now](#getting-started){: .btn .btn-blue .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/hephy-dd/comet){: .btn .fs-5 .mb-4 .mb-md-0 }

## Getting started

### Dependencies

COMET depends on [PyVISA](https://pyvisa.readthedocs.io/en/latest/) for instrument
communication and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) for the
graphical user interface. COMET works on Linux and Windows operating systems.

### Install

Install from GitHub using pip

```bash
pip install git+https://github.com/hephy-dd/comet.git@0.2.3
```

### Quick start

COMET provides a basic application window and a set of modules for instrument communication
and threaded processes.

The following minimal example invokes the application's main window containing a text
field and some buttone.

```python
import comet

app = comet.Application()
app.title = "Example"
app.layout = comet.Column(
    comet.Text(id="txt", value="Click a button!", readonly=True),
    comet.Button(value="Update", click=lambda event: comet.get('txt').text = comet.time()),
    comet.Button(value="Clear", click=lambda event: comet.get('txt').text = None)
)
app.run()
```

## About the project

COMET is &copy; 2019 by [Bernhard Arnold](https://github.com/arnobaer/).

### License

COMET is licensed under the [GNU General Public License Version 3](https://github.com/hephy-dd/comet/tree/master/LICENSE).

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the maintainers of this repository before making a change.
