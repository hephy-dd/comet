import re
import time

from comet.devices import IEC60488
from comet.device import Node

from .k2400 import Beeper

__all__ = ['K2700']

class System(Node):

    def __init__(self, parent):
        super().__init__(parent)
        self.__beeper = Beeper(self)

    @property
    def beeper(self):
        return self.__beeper

    @property
    def error(self) -> tuple:
        """Returns current instrument error.

        >>> system.error
        (0, "No error")
        """
        with self.lock:
            result = self.resource.query(':SYST:ERR?').split(',')
            return int(result[0]), result[1].strip('"')

class K2700(IEC60488):
    """Keithley Model 2700 Multimeter/Switch."""

    options = {
        'read_termination': '\r',
    }

    poll_count = 40
    """Poll retry count."""

    poll_interval = .250
    """Poll interval in seconds."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__system = System(self)

    @property
    def system(self):
        return self.__system

    def init(self):
        with self.lock:
            self.resource.write('*CLS')
            self.resource.write(':INIT')
            self.resource.write('*OPC')
            # Poll for OPC flag (bit 0)
            for i in range(self.poll_count):
                if int(self.resource.query('*ESR?')) & 0x1:
                    return
                time.sleep(self.poll_interval)
            raise RuntimeError("Failed to poll for OPC flag in ESR.")

    def fetch(self):
        """Returns the latest available readings as list of dictionaries.
        .. note:: It does not perform a measurement.
        >>> device.fetch()
        [{'VDC': -4.32962079e-05, 'SECS': 0.0, 'RDNG': 0.0}, ...]
        """
        readings = []
        # split '-4.32962079e-05VDC,+0.000SECS,+0.0000RDNG#,...'
        with self.lock:
            result = self.resource.query(':FETC?')
        for values in re.findall(r'([^#]+)#\,?', result):
            values = re.findall(r'([+-]?\d+(?:\.\d+)?(?:E[+-]\d+)?)([A-Z]+)\,?', values)
            readings.append({suffix: float(value) for value, suffix in values})
        return readings

    def read(self):
        """A high level command to perform a singleshot measurement.
        It resets the trigger model(idle), initiates it, and fetches a new
        value.
        """
        with self.lock:
            result = self.resource.query(':READ?')
        return [float(value) for value in result.split(',')]
