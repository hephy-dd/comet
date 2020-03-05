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

class Source(Driver):

    class Voltage(Driver):

        @property
        def level(self) -> float:
            return float(self.resource.query(':SOUR:VOLT:LEV?'))

        @level.setter
        @opc_wait
        def level(self, value: float):
            self.resource.write(f':SOUR:VOLT:LEV {value:E}')

    def __init__(self, resource):
        super().__init__(resource)
        self.voltage = self.Voltage(resource)

    @opc_wait
    def clear(self):
        """Turn output source off when in idle."""
        self.resource.write(':SOUR:CLE')

class Sense(Driver):

    class Current(Driver):

        class Protection(Driver):

            @property
            def level(self) -> float:
                """Returns current compliance limit."""
                return float(self.resource.query(':SENS:CURR:PROT:LEV?'))

            @level.setter
            @opc_wait
            def level(self, value: float):
                """Set current compliance limit for V-Source."""
                self.resource.write(f':SENS:CURR:PROT:LEV {value:E}')

            @property
            def tripped(self) -> bool:
                """Returns True if in current compliance."""
                return bool(int(self.resource.query(':SENS:CURR:PROT:TRIP?')))

            @property
            def rsyncronize(self) -> bool:
                """Returns True if range syncronization enabled."""
                return bool(int(self.resource.query(':SENS:CURR:PROT:RSYN?')))

            @rsyncronize.setter
            @opc_wait
            def rsyncronize(self, value: bool):
                """Enable or disable measure and compliance range syncronization."""
                self.resource.write(f':SENS:CURR:PROT:RSYN {value:d}')

        def __init__(self, resource):
            super().__init__(resource)
            self.protection = self.Protection(resource)

    class Voltage(Driver):

        class Protection(Driver):

            @property
            def level(self) -> float:
                """Returns voltage compliance limit."""
                return float(self.resource.query(':SENS:VOLT:PROT:LEV?'))

            @level.setter
            @opc_wait
            def level(self, value: float):
                """Set voltage compliance limit for V-Source."""
                self.resource.write(f':SENS:VOLT:PROT:LEV {value:E}')

            @property
            def tripped(self) -> bool:
                """Returns True if in voltage compliance."""
                return bool(int(self.resource.query(':SENS:VOLT:PROT:TRIP?')))

            @property
            def rsyncronize(self) -> bool:
                """Returns True if range syncronization enabled."""
                return bool(int(self.resource.query(':SENS:VOLT:PROT:RSYN?')))

            @rsyncronize.setter
            def rsyncronize(self, value: bool):
                """Enable or disable measure and compliance range syncronization."""
                self.resource.write(f':SENS:VOLT:PROT:RSYN {value:d}')

        def __init__(self, resource):
            super().__init__(resource)
            self.protection = self.Protection(resource)

    def __init__(self, resource):
        super().__init__(resource)
        self.current = self.Current(resource)
        self.voltage = self.Current(resource)

class PowerMixin:

    @property
    def output(self) -> bool:
        """Returns True if output enabled.

        >>> instr.output
        True
        """
        return bool(int(self.resource.query(':OUTP:ENAB:STAT?')))

    @output.setter
    @opc_wait
    def output(self, value: bool):
        """Enable or disable output.

        >>> instr.output = True
        """
        self.resource.write(f':OUTP:ENAB:STAT {value:d}')

class MeasureMixin:

    @opc_poll
    def init(self):
        """Initiate a measurement.

        >>> instr.init()
        """
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
        self.sense = Sense(resource)
