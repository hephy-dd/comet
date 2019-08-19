from ..iec import IEC60488

__all__ = ['K2410']

class K2410(IEC60488):

    def fetch(self):
        """Returns the latest available reading
        .. note:: It does not perform a measurement.
        """
        return self.transport().query(':FETC?')

    def read(self):
        """A high level command to perform a singleshot measurement.
        It resets the trigger model(idle), initiates it, and fetches a new
        value.
        """
        return self.transport().query(':READ?')
