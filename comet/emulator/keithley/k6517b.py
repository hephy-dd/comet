"""Keithley 6517B Electrometer emulator."""

from comet.emulator.emulator import message, run
from comet.emulator.keithley.k6514 import K6514Handler

__all__ = ['K6517BHandler']

class K6517BHandler(K6514Handler):
    """Generic Keithley 6517B series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 6517B, 12345678, v1.0"

if __name__ == "__main__":
    run(K6517BHandler)
