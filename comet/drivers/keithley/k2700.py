import re

from ..iec import IEC60488

__all__ = ['K2700']

class K2700(IEC60488):

    readTermination = '\r'

    def init(self):
        """Initialize measurement."""
        self.resource().write('INIT')

    def fetch(self):
        """Returns the latest available readings as list of dictionaries.
        .. note:: It does not perform a measurement.

        >>> device.fetch()
        [{'VDC': -4.32962079e-05, 'SECS': 0.0, 'RDNG': 0.0}, ...]
        """
        results = []
        # split '-4.32962079e-05VDC,+0.000SECS,+0.0000RDNG#,...'
        for values in re.findall(r'([^#]+)#\,?', self.resource().query('FETC?')):
            values = re.findall(r'([+-]?\d+(?:\.\d+)?(?:E[+-]\d+)?)([A-Z]+)\,?', values)
            results.append({suffix: float(value) for value, suffix in values})
        return results

    def read(self):
        """A high level command to perform a singleshot measurement.
        It resets the trigger model(idle), initiates it, and fetches a new
        value.
        """
        return [float(value) for value in self.resource().query(':READ?').split(',')]
