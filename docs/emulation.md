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

Create a custom instrument emulator socket by inheriting from class `RequestHandler`. Use method decorator `message` to create message routes using regular expressions.

```python
from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

class MyHandler(RequestHandler):
    """My custom request handler."""

    @message(r'\*IDN\?')
    def query_idn(self, message):
        return "MyInstrument, version 1.0"

    @message(r'\*RST')
    def write_reset(self, message):
        pass

if __name__ == "__main__":
    run(MyHandler)
```

Running a custom emulator from the command line.

```bash
python my_handler.py -p 10001
```

