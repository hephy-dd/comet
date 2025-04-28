# Helpers

## Estimate

Estimate remaining time for loop operations using class `Estimate`.

Call method `advance` to proceed to the next iteration and update average and
remaining time calculation.

```python
from comet.estimate import Estimate

n = 42
e = Estimate(n)  # start stopwatch
for i in range(n):
    ...
    e.advance()  # stop time since last step
    print("passed:", e.passed)
    print("remaining time:", e.remaining)
    print("elapsed time:", e.elapsed)
    print("average time:", e.average)
```

## Filters

Test if standard deviation / mean < threshold using function `std_mean_filter`.

```python
from comet.filters import std_mean_filter

if std_mean_filter(readings, threshold=0.005):
    ...
```

## Functions

Voltage ramps using `LinearRange` generator class.

```python
from comet.functions import LinearRange

for voltage in LinearRange(-10, +10, 0.25):
    ...
```

## Parameter

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

## Utils

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
