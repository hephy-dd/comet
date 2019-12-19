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
pip install git+https://github.com/hephy-dd/comet.git@0.5.0
```

## Quick start

The following minimal example invokes the application's main window.

```python
import comet

app = comet.Application()
window = comet.MainWindow()
window.show()
app.run()
```

## License

COMET is licensed under the [GNU General Public License Version 3](https://github.com/hephy-dd/comet/tree/master/LICENSE).
