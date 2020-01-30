import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.iec60488 import IEC60488Handler
from comet.emulator.keithley.k2400 import SystemMixin, MeasureMixin

__all__ = ['K2700Handler']

class K2700Handler(IEC60488Handler, SystemMixin, MeasureMixin):
    """Generic Keithley 2700 series compliant request handler."""

    identification = "Spanish Inquisition Inc., Model 2700, 12345678, v1.0"

if __name__ == "__main__":
    run(K2700Handler)
