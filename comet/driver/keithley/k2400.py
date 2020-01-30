import re
import time
from typing import Dict, List, Tuple

from comet.driver import lock, Driver
from comet.driver import IEC60488
from comet.driver.iec60488 import opc_wait, opc_poll

__all__ = ['K2400']

def parse_reading(s):
    """Returns list of dictionaries containing reading values."""
    readings = []
    # split '-4.32962079e-05VDC,+0.000SECS,+0.0000RDNG#,...'
    for values in re.findall(r'([^#]+)#\,?', s):
        values = re.findall(r'([+-]?\d+(?:\.\d+)?(?:E[+-]\d+)?)([A-Z]+)\,?', values)
        readings.append({suffix: float(value) for value, suffix in values})
    return readings

class Beeper(Driver):

    @property
    def status(self) -> bool:
        result = self.resource.query(':SYST:BEEP:STAT?')
        return bool(int(result))

    @status.setter
    @opc_wait
    def status(self, value: bool):
        self.resource.write(f':SYST:BEEP:STAT {value:d}')

class System(Driver):

    def __init__(self, resource):
        super().__init__(resource)
        self.beeper = Beeper(resource)

    @property
    def error(self) -> Tuple[int, str]:
        """Returns current instrument error.

        >>> system.error
        (0, "No error")
        """
        result = self.resource.query(':SYST:ERR?').split(',')
        return int(result[0]), result[1].strip().strip('"')

class Voltage(Driver):

    @property
    def level(self) -> float:
        return float(self.resource.query(':SOUR:VOLT:LEV?'))

    @level.setter
    @opc_wait
    def level(self, value: float):
        self.resource.write(f':SOUR:VOLT:LEV {value:E}')

class Source(Driver):

    def __init__(self, resource):
        super().__init__(resource)
        self.voltage = Voltage(resource)

class PowerMixin:

    @property
    def output(self) -> str:
        """Returns output state (on/off)."""
        return self.resource.query(':OUTP?').lower()

    @output.setter
    @opc_wait
    def output(self, value: str):
        self.resource.write(f':OUTP {value}')

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

class K2400(IEC60488, MeasureMixin, PowerMixin):
    """Keithley Series 2400 SourceMeter."""

    def __init__(self, resource):
        super().__init__(resource)
        self.system = System(resource)
        self.source = Source(resource)
