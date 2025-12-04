# COMET

**Control and Measurement Toolkit**

COMET makes it easy to control, automate, and emulate scientific instruments.

Providing generic instrument drivers, instrument emulators for testing and utilities for instrumentation
applications. Inspired by
[QCoDeS](https://github.com/QCoDeS/Qcodes),
[Lantz](https://github.com/LabPy/lantz),
[Slave](https://github.com/p3trus/slave),
[FluidLab](https://github.com/fluiddyn/fluidlab).

## Highlights

- **Generic instrument drivers** - communicate with devices over PyVISA-compatible resources.
- **Station abstraction** - define and manage your entire instrument setup from code or config files.
- **Emulators** - simulate instruments over TCP sockets or in-process mock resources for testing without hardware.
- **Utilities** - from parameter handling to time estimations, unit conversions, and filtering tools.

## Install

Install from GitHub using pip

```bash
pip install https://github.com/hephy-dd/comet/archive/refs/tags/v1.4.1.tar.gz
```

## Quick Example

```python
from comet.station import Station

config = {"instruments": {
    "smu": {"resource_name": "GPIB::16", "model": "keithley.k2470"},
    "dmm": {"resource_name": "GPIB::18", "model": "keithley.k2700"},
}}

with Station.from_config(config) as station:
    print(station.smu.identify())
    station.smu.voltage_level = 5.0
    print(station.dmm.measure_voltage())
```

See [Station](https://hephy-dd.github.io/comet/station/) and [Drivers](https://hephy-dd.github.io/comet/drivers/) for more.

No instruments at hand? COMET comes with a powerful set of emulators using TCP sockets.

```yaml
# emulators.yaml
emulators:
  smu:
    module: keithley.k2470
    port: 11001
  dmm:
    module: keithley.k2700
    port: 11002
```

```bash
comet-emulator
```

When using emulators, update the resource_name to point to the local TCP endpoints instead of GPIB addresses:

```python
config = {"instruments": {
    "smu": {"resource_name": "TCPIP0::localhost::11001::SOCKET", "model": "keithley.k2470"},
    "dmm": {"resource_name": "TCPIP0::localhost::11002::SOCKET", "model": "keithley.k2700"},
}}
```

See [Emulators](https://hephy-dd.github.io/comet/emulators/) for more.


## Documentation

📚 Full docs are available at: [COMET Documentation](https://hephy-dd.github.io/comet/)

## License

COMET is licensed under the [GNU General Public License Version 3](LICENSE).
