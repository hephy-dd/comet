import re
from typing import Dict, List, Tuple

from comet.driver import IEC60488
from comet.driver.iec60488 import opc_wait, opc_poll

from .k2400 import System

__all__ = ['K2700']

def parse_reading(s):
    """Returns list of dictionaries containing reading values."""
    readings = []
    # split '-4.32962079e-05VDC,+0.000SECS,+0.0000RDNG#,...'
    for values in re.findall(r'([^#]+)#\,?', s):
        values = re.findall(r'([+-]?\d+(?:\.\d+)?(?:E[+-]\d+)?)([A-Z]+)\,?', values)
        readings.append({suffix: float(value) for value, suffix in values})
    return readings

class MeasureMixin:

    @opc_poll
    def init(self):
        """Initiate a measurement."""
        self.resource.write(':INIT')

    def fetch(self) -> List[Dict[str, float]]:
        """Returns the latest available readings as list of dictionaries..
        >>> instr.fetch()
        [{'VDC': -4.32962079e-05, 'SECS': 0.0, 'RDNG': 0.0}, ...]
        """
        result = self.resource.query(':FETC?')
        return parse_reading(result)

    def read(self) -> List[Dict[str, float]]:
        """High level command to perform a singleshot measurement. It resets the
        trigger model, initiates it, and fetches a new reading.
        >>> instr.read()
        [{'VDC': -4.32962079e-05, 'SECS': 0.0, 'RDNG': 0.0}, ...]
        """
        result = self.resource.query(':READ?')
        return parse_reading(result)

class K2700(IEC60488, MeasureMixin):
    """Keithley Model 2700 Multimeter/Switch."""

    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.system = System(self.resource)
