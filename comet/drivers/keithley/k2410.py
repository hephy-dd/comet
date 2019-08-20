from ..iec import IEC60488

__all__ = ['K2410']

class K2410(IEC60488):

    readTermination = '\r'

    def output(self):
        """Returns True if output enabled, else retruns False."""
        return bool(self.resource().query('OUTP?'))

    def enableOutput(self, enabled):
        values = {True: 'ON', False: 'OFF'}
        self.resource().write('OUTP {}'.format(values[enabled]))

    def voltage(self):
        return self.resource().query('SOUR:VOLT:LEV?')

    def setVoltage(self, value):
        self.resource().write('SOUR:VOLT:LEV {:E}'.format(value))

    def read(self):
        """A high level command to perform a singleshot measurement.
        It resets the trigger model(idle), initiates it, and fetches a new
        value.
        """
        return [float(value) for value in self.resource().query(':READ?').split(',')]
