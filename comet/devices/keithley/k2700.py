import re

from comet.devices import IEC60488

__all__ = ['K2700']

class K2700(IEC60488):

    options = {
        'read_termination': '\r',
    }

    def init(self):
        """Initialize measurement."""
        with self.lock:
            self.resource.write(':INIT')
            self.resource.query('*OPC?')

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
