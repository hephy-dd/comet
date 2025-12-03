# Emulators

See package [comet.emulator](https://github.com/hephy-dd/comet/tree/main/src/comet/emulator)
for available instrument emulators.

## Using TCP sockets

To emulate one or more instruments using TCP sockets create a `emulators.yaml`
configuration file in your project directory specifying instrument `model` URN and
`port`.

```yaml
emulators:
  smu:
    model: urn:comet:model:keithley:2470
    port: 11001
  lcr:
    model: urn:comet:model:keysight:e4980a
    port: 11002
    # Set message termination (\n, \r, \n, \r\n, CR, LF, CRLF)
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

Use command line argument `-f` (or `--file`) to use a custom configuration file.

```bash
comet-emulator -f custom_emulators.yaml
```

## The Emulators file

The default path for an Emulators file is `emulators.yaml` (preferred) or
`emulators.yml` that is placed in the current working directory. If both files
exist, `comet-emulator` prefers the canonical `emulators.yaml`.

## Using Resources

To use instrument emulators as resources use function `open_emulator` from
package `comet.emulator` to open a mock resource for an instrument.

```python
from comet.emulator import open_emulator

with open_emulator("urn:comet:model:keithley:2410") as res:
    print(res.query("*IDN?"))
```

Mock resources can be used like regular PyVISA resources in combination with
instrument drivers.

```python
from comet.driver import driver_factory
from comet.emulator import open_emulator

model_urn = "urn:comet:model:keithley:2410"

with open_emulator(model_urn) as res:
    instr = driver_factory(model_urn)(res)
    print(instr.identify())
```

To set emulator specific options either provide an `options` dict to
`open_emulator` or update the `emulator.options` dict directly.

```python
from comet.emulator import open_emulator

options = {"correction_open_delay": 2.0}

with open_emulator("urn:comet:model:keysight:e4980a", options=options) as res:
    res.emulator.options.update({
        "cp.min": 2.5e-10,
        "cp.max": 2.5e-9,
    })
```
