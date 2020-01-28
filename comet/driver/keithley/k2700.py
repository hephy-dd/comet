import re
import time

from comet.driver import IEC60488
from comet.driver.iec60488 import opc_wait, opc_poll

from .k2400 import System
from .k2400 import MeasureMixin

__all__ = ['K2700']

class System(System):

    pass

class K2700(IEC60488, MeasureMixin):
    """Keithley Model 2700 Multimeter/Switch."""

    system = System()
