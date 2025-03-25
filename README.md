# COMET

**Control and Measurement Toolkit**

Providing generic instrument drivers, instrument emulators for testing and and
utilities for instrumentation applications. Inspired by
[QCoDeS](https://github.com/QCoDeS/Qcodes),
[Lantz](https://github.com/LabPy/lantz),
[Slave](https://github.com/p3trus/slave),
[FluidLab](https://github.com/fluiddyn/fluidlab).

## Install

Install from GitHub using pip

```bash
pip install git+https://github.com/hephy-dd/comet.git@v1.2.0
```

## Drivers

Generic instrument drivers use a PyVISA compatible resource to communicate with.

```python
import pyvisa

from comet.driver.keithley import K2470

rm = pyvisa.ResourceManager("@py")

with rm.open_resource("TCPIP::0.0.0.0::11001::SOCKET") as res:
    smu = K2470(res)
    print(smu.identify())

    smu.reset()
    smu.function = smu.FUNCTION_VOLTAGE
    smu.current_compliance = 1e-6
    smu.output = smu.OUTPUT_ON
    smu.voltage_level = 5.0

    reading = smu.measure_current()
    print(reading)

    smu.voltage_level = 0.0
    smu.output = smu.OUTPUT_OFF
```

Loading driver by module name using driver factory.

```python
from comet.driver import driver_factory

rm = pyvisa.ResourceManager("@py")

with rm.open_resource("TCPIP::0.0.0.0::11001::SOCKET") as res:
    smu = driver_factory("keithley.k2410")(res)
```

Switching between generic drivers.

```python
from comet.driver import driver_factory

smu_drivers = {
    "Keithely2410": "keithley.k2410",
    "Keithely2470": "keithley.k2470",
    "Keitley2657A": "keithley.k2657a",
}

driver_name = "Keithely2470"

rm = pyvisa.ResourceManager("@py")

with rm.open_resource("TCPIP::0.0.0.0::11001::SOCKET") as res:
    smu = smu_drivers.get(driver_name)(res)
```

See package [comet.driver](src/comet/driver) for available instrument drivers.

## Helpers

### Estimate

Estimate remaining time for loop operations using class `Estimate`.

Call method `advance` to proceed to the next iteration and update average and
remaining time calculation.

```python
from comet.estimate import Estimate

e = Estimate(42)  # start stopwatch
for i in range(42 + 1):
    ...
    e.advance()  # stop time since last step
    print("passed:", e.passed)
    print("remaining time:", e.remaining)
    print("elapsed time:", e.elapsed)
    print("average time:", e.average)
```

### Filters

Test if standard deviation / mean < threshold using function `std_mean_filter`.

```python
from comet.filters import std_mean_filter

if std_mean_filter(readings, threshold=0.005):
    ...
```

### Functions

Voltage ramps using `LinearRange` generator class.

```python
from comet.functions import LinearRange

for voltage in LinearRange(-10, +10, 0.25):
    ...
```

### Parameter

Bind typed and bounded parameters to classes inheriting from class
`ParameterBase`.

```python
from comet.parameter import ParameterBase, Parameter

class Measurement(ParameterBase):

    voltage_level = Parameter(unit="V", minimum=-1000, maximum=1000)
    current_compliance = Parameter(default="25 uA", unit="A", minimum=0, maximum="10 mA")
    terminal = Parameter(default="front", choice=["front", "rear"])
    write_output = Parameter(default=True, type=bool)

measurement = Measurement({"voltage_level": "100 V"})  # supply required parameters

# Get dictionary of all parameter values.
print(measurement.parameters)
# {'voltage_level': 100.0, 'current_compliance': 2.5e-05, 'terminal': 'front', 'write_output': True}

# Update parameter values
measurement.update_parameters({"current_compliance": "50 uA", "terminal": "rear"})

# Access individual parameter
print(measurement.voltage_level)
# 100.0
print(measurement.current_compliance)
# 5e-05
print(measurement.terminal)
# 'rear'

measurement.write_output = False
# AttributeError: can't set parameter: 'write_output'

```

### Utils

Use [pint](https://pint.readthedocs.io/en/stable/) unit registry to convert
between units.

```python
from comet.utils import ureg, to_unit

quantity = ureg("25 nA").to("A")

print(to_unit(quantity, "mA"))
# 2.5e-05

print(to_unit("1200 V", "kV"))
# 1.2

print(to_unit(2.5, "pA"))
# 2.5
```

## Emulators

### Using TCP sockets

To emulate one or more instruments using TCP sockets create a `emulators.yaml`
configuration file in your project directory specifying emulator module and
port.

```yaml
version: '1.0'
emulators:
  smu:
    module: keithley.k2470
    port: 11001
  lcr:
    module: keysight.e4980a
    port: 11002
    # Set message termination
    termination: '\n'
    # Set specific options
    options:
      cp.min: 2.5e-10
      cp.max: 2.5e-9
```

To spin up the emulator sockets run `comet-emulator` or alternatively
`python -m comet.emulator`.

```bash
comet-emulator
```

Use command line argument `-f` to use a custom configuration file.

```bash
comet-emulator -f custom_emulators.yaml
```

See package [comet.emulator](src/comet/emulator) for available instrument emulators.

### Using Resources

To use instrument emulators as resources use function `open_emulator` from
package `comet.emulator` to open a mock resource for an instrument.

```python
from comet.emulator import open_emulator

with open_emulator("keithley.k2410") as res:
    print(res.query("*IDN?"))
```

Mock resources can be used like regular PyVISA resources in combination with
instrument drivers.

```python
from comet.driver.keithley import K2410
from comet.emulator import open_emulator

with open_emulator("keithley.k2410") as res:
    instr = K2410(res)
    print(instr.identify())
```

To set emulator specific options either provide an `options` dict to
`open_emulator` or update the `emulator.options` dict directly.

```python
from comet.emulator import open_emulator

options = {"correction_open_delay": 2.0}

with open_emulator("keysight.e4980a", options=options) as res:
    res.emulator.options.update({
        "cp.min": 2.5e-10,
        "cp.max": 2.5e-9,
    })
```

## License

COMET is licensed under the [GNU General Public License Version 3](LICENSE).
