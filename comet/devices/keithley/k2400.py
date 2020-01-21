import re
import time

from comet.devices import IEC60488
from comet.device import Node, Mapping

__all__ = ['K2400']

class System(Node):

    def __init__(self, parent):
        super().__init__(parent)
        self.__beeper = Beeper(self)

    @property
    def beeper(self):
        return self.__beeper

    @property
    def error(self):
        """Returns current instrument error.

        >>> system.error
        (0, "No error")
        """
        with self.lock:
            result = self.resource.query(':SYST:ERR?').split(',')
            return int(result[0]), result[1].strip('"')

class Beeper(Node):

    @property
    def status(self) -> bool:
        with self.lock:
            result = self.resource.query(':SYST:BEEP:STAT?')
            return bool(int(result))

    @status.setter
    def status(self, value: bool):
        with self.lock:
            self.resource.write(f':SYST:BEEP:STAT {value:d}')
            self.resource.query('*OPC?')

class Source(Node):

    def __init__(self, parent):
        super().__init__(parent)
        self.__voltage = Voltage(self)

    @property
    def voltage(self):
        return self.__voltage

class Voltage(Node):

    @property
    def level(self) -> float:
        with self.lock:
            return float(self.resource.query('SOUR:VOLT:LEV?'))

    @level.setter
    def level(self, value: float):
        with self.lock:
            self.resource.write(f'SOUR:VOLT:LEV {value:E}')
            self.resource.query('*OPC?')

class K2400(IEC60488):
    """Keithley Series 2400 SourceMeter."""

    options = {
        'read_termination': '\r\n',
    }

    poll_count = 40
    """Poll retry count."""

    poll_interval = .250
    """Poll interval in seconds."""

    Output = Mapping({'on': 'ON', 'off': 'OFF'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__system = System(self)
        self.__source = Source(self)

    @property
    def system(self):
        return self.__system

    @property
    def source(self):
        return self.__source

    @property
    def output(self):
        """Returns True if output enabled, else retruns False."""
        value = self.resource.query('OUTP?').strip()
        return self.Output.get_key(value)

    @output.setter
    def output(self, value):
        value = self.Output.get_value(value)
        with self.lock:
            self.resource.write(f'OUTP {value}')
            self.resource.query('*OPC?')

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

    def read(self):
        """A high level command to perform a singleshot measurement.
        It resets the trigger model(idle), initiates it, and fetches a new
        value.
        """
        values = self.resource.query(':READ?').split(',')
        return [float(value) for value in values]
