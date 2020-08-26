---
layout: default
title: Emulation
nav_order: 7
---

# Instrument emulation
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

* TOC
{: toc}

## Quick start

Run an instrument emulation socket on port `10001` from the command line.

```bash
python -m comet.emulator.keithley.k2410 -p 10001
```

See package [comet.emulator](https://github.com/hephy-dd/comet/tree/master/comet/emulator) for available emulators.

## Custom emulators

Create a custom instrument emulator socket by inheriting from class
`RequestHandler`. Use method decorator `message` to create message routes using
regular expressions. Use capture groups `()` and to extract strings and map to
function arguments.

```python
from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

class MyHandler(RequestHandler):
    """My custom request handler."""

    @message(r'\*IDN\?')
    def query_idn(self):
        return "MyInstrument, version 1.0"

    @message(r'\*RST')
    def write_reset(self):
        pass

    @message(r':?SYST:BEEP:STAT\s+(0|1|OFF|ON)')
    def write_voltage(self, state):
        state = {'0': False, '1': True, 'OFF': False, 'ON': True}[state]

    @message(r':?SOUR:VOLT:LEV\s+([+-]\d+(?:\.\d+)?(?:)[eE]\d+)?)')
    def write_voltage(self, voltage):
        voltage = float(voltage)

if __name__ == "__main__":
    run(MyHandler)
```

Running a custom emulator from the command line.

```bash
python my_handler.py -p 10001
```
