from slave.driver import Command, Driver
from slave.iec60488 import IEC60488
from slave.types import Boolean, Float, Integer, Mapping, Set

__all__ = ['K2700']

class K2700(IEC60488):

    def fetch(self):
        """Returns the latest available reading
        .. note:: It does not perform a measurement.
        """
        return self._query((':FETC?', Float))

    def read(self):
        """A high level command to perform a singleshot measurement.
        It resets the trigger model(idle), initiates it, and fetches a new
        value.
        """
        return self._query((':READ?', Float))
