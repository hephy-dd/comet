# Emulators

See package [comet.emulator](https://github.com/hephy-dd/comet/tree/main/src/comet/emulator)
for available instrument emulators.

## Using TCP sockets

To emulate one or more instruments using TCP sockets create a `emulators.yaml`
configuration file in your project directory specifying emulator module and
port.

```yaml
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

## Using Resources

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
