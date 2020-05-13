"""Keithley 2410 emulator."""

from comet.emulator.emulator import message, run
from .k2400 import K2400Handler

__all__ = ['K2410Handler']

class K2410Handler(K2400Handler):
    """Generic Keithley 2400 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 2410, 43768438, v1.0"

if __name__ == "__main__":
    run(K2410Handler)
