---
layout: default
title: Home
nav_order: 1
permalink: /
---

# COMET

Control and Measurement Toolkit. 
{: .fs-6 .fw-300 }

A PyQt5 powered rapid development tool for creating graphical measurement desktop applications,
inspired by [QCoDeS](https://github.com/QCoDeS/Qcodes), [Lantz](https://github.com/LabPy/lantz),
[Slave](https://github.com/p3trus/slave), [FluidLab](https://github.com/fluiddyn/fluidlab) and
[Dash](https://github.com/plotly/dash).

[Get started now](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/hephy-dd/comet){: .btn .fs-5 .mb-4 .mb-md-0 }

## Getting started

### Dependencies

COMET depends on [PyVISA-py](https://pyvisa-py.readthedocs.io/en/latest/) for instrument 
communication and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) for the
graphical user interface. COMET works on Linux and Windows operating systems.

### Install

Install from GitHub using pip

```bash
pip install git+https://github.com/hephy-dd/comet.git@0.1.0
```

### Quick start

COMET provides a basic application window and a set of modules for instrument communication
and threaded processes.

The following minimal example invokes the application's main window.

```python
import comet

app = comet.Application()
window = comet.MainWindow()
window.show()
app.run()
```

## About the project

COMET is &copy; 2019 by [Bernhard Arnold](https://github.com/arnobaer/).

### License

COMET is licensed under the [GNU General Public License Version 3](https://github.com/hephy-dd/comet/tree/master/LICENSE).

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the maintainers of this repository before making a change.
