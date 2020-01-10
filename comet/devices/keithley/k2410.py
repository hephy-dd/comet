from comet.devices import IEC60488
from comet.device import Mapping

__all__ = ['K2410']

class K2410(IEC60488):

    options = {
        'read_termination': '\r',
    }

    Output = Mapping({'on': 'ON', 'off': 'OFF'})

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

    @property
    def voltage(self):
        return float(self.resource.query('SOUR:VOLT:LEV?'))

    @voltage.setter
    def voltage(self, value):
        with self.lock:
            self.resource.write(f'SOUR:VOLT:LEV {value:E}')
            self.resource.query('*OPC?')

    def init(self):
        with self.lock:
            self.resource.write(':INIT')
            self.resource.query('*OPC?')

    def read(self):
        """A high level command to perform a singleshot measurement.
        It resets the trigger model(idle), initiates it, and fetches a new
        value.
        """
        values = self.resource.query(':READ?').split(',')
        return [float(value) for value in values]
