# Helpers

## Estimate

### `Estimate`

Track progress and estimate the remaining time of an iterative operation.

Create an `Estimate` with the total number of steps and call `advance()` after each completed step:

```python
from comet.estimate import Estimate

eta = Estimate(42)

for _ in range(42):
    ...
    eta.advance()

    print("progress:", eta.progress)
    print("elapsed:", eta.elapsed)
    print("remaining:", eta.remaining)
```

`Estimate` provides the following properties:

- `total` — total number of steps
- `passed` — number of completed steps
- `progress` — completed and total steps as `(passed, total)`
- `elapsed` — time elapsed since the estimate was created
- `average` — average duration of completed steps
- `remaining` — estimated duration of the remaining steps

Timing values are returned as `datetime.timedelta` objects.

The remaining time is calculated from the average duration of the steps recorded by `advance()`:

```python
eta = Estimate(len(items))

for item in items:
    process(item)
    eta.advance()

    passed, total = eta.progress
    print(f"{passed}/{total} - {eta.remaining} remaining")
```

Before the first completed step, `average` and `remaining` are `timedelta(0)`. Calls to `advance()` after all steps have been completed are ignored.

## Filters

### `std_mean_filter`

Test whether a series of values is stable within a given threshold.

Returns `True` if the ratio of the sample standard deviation to the mean is below `threshold`, otherwise `False`.

```python
from comet.filters import std_mean_filter

readings = [0.250, 0.249]

if std_mean_filter(readings, threshold=0.005):
    ...
```

This can be used to determine whether repeated measurements have settled within an acceptable relative variation.

## Functions

### `LinearRange`

Generate a linear range of floating-point values. The range includes both the start and end values.

```python
from comet.functions import LinearRange

for voltage in LinearRange(-10, 10, 0.25):
    ...
```

`LinearRange` automatically adjusts the direction of `step` to match the range:

```python
list(LinearRange(0, 10, 2.5))
# [0.0, 2.5, 5.0, 7.5, 10.0]

list(LinearRange(10, 0, 2.5))
# [10.0, 7.5, 5.0, 2.5, 0.0]
```

The end value is always included, even when the step does not divide the range evenly:

```python
list(LinearRange(0, 5, 2))
# [0.0, 2.0, 4.0, 5.0]
```

Use `distance` to get the absolute distance between the start and end values:

```python
LinearRange(-2.5, 2.5, 0.5).distance
# 5.0
```

## Utils

### `combine_matrix`

Combine multiple iterables into all possible string combinations.

```python
from comet.utils import combine_matrix

print(combine_matrix(["A", "B"], ["1", "2"]))
# ['A1', 'A2', 'B1', 'B2']
```

Any number of iterables can be combined:

```python
print(combine_matrix(["A", "B"], ["1", "2"], ["x", "y"]))
# ['A1x', 'A1y', 'A2x', 'A2y', 'B1x', 'B1y', 'B2x', 'B2y']
```

### `inverse_square`

Return the inverse square of a value, \(1/x^2\).

```python
from comet.utils import inverse_square

print(inverse_square(2))
# 0.25

print(inverse_square(10))
# 0.01
```

### `t_dew`

Calculate the dew point from temperature and relative humidity.

```python
from comet.utils import t_dew

dew_point = t_dew(25.0, 60.0)

print(dew_point)
# 16.68424959549877
```

`t` is the temperature in °C and `rh` is the relative humidity in percent.

### `make_iso`

Create a filesystem-safe ISO-like UTC timestamp.

```python
from comet.utils import make_iso

print(make_iso(1423456789.8))
# 2015-02-09T05-39-49
```

Without an argument, the current UTC time is used:

```python
timestamp = make_iso()
# e.g. '2026-09-02T15-17-42'
```

A `datetime` can also be passed directly:

```python
from datetime import UTC, datetime

dt = datetime(2026, 9, 2, 12, 30, tzinfo=UTC)

print(make_iso(dt))
# 2026-09-02T12-30-00
```

### `safe_filename`

Replace characters that are unsafe or inconvenient in filenames with underscores.

```python
from comet.utils import safe_filename

print(safe_filename("measurement 25°C.txt"))
# measurement_25_C.txt
```

Letters, numbers, underscores, hyphens, periods, and path separators are preserved.

```python
print(safe_filename("results/run #1/data.csv"))
# results/run_1/data.csv
```

### Unit conversions

Use [pint](https://pint.readthedocs.io/en/stable/) directly when working with physical quantities and unit conversions.

```python
import pint

ureg = pint.UnitRegistry()

q = ureg("25 nA").to("mA")
print(q.magnitude)
# 2.5e-05

q = ureg("1200 V").to("kV")
print(q.magnitude)
# 1.2

q = 2.5 * ureg("pA")
print(q.magnitude)
# 2.5
```
