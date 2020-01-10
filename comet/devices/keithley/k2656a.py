from comet.devices import IEC60488
from comet.device import Mapping

__all__ = ['K2656A']

class K2656A(IEC60488):

    options = {
        'encoding': 'latin1',
        'read_termination': '\r',
    }

    Output = Mapping({'off': 0, 'on': 1, 'high_z': 2})

    @property
    def output(self):
        return self.Output.get_key(self.resource.query('print(smua.source.output)'))

    @output.setter
    def output(self, value):
        value = self.Output.get_value(value)
        with self.lock:
            self.resource.write(f'smua.source.output = {value:E}')
            self.resource.waitcomplete()

    @property
    def levelv(self):
        with self.lock:
            return float(self.resource.query('print(smua.source.levelv)'))

    @levelv.setter
    def levelv(self, value):
        with self.lock:
            self.resource.write(f'smua.source.levelv = {value:E}')
            self.resource.waitcomplete()

    @property
    def leveli(self):
        with self.lock:
            return float(self.resource.query('print(smua.source.leveli)'))

    @leveli.setter
    def leveli(self, value):
        with self.lock:
            self.resource.write(f'smua.source.leveli = {value:E}')
            self.resource.waitcomplete()

    @property
    def limitv(self):
        with self.lock:
            return float(self.resource.query('print(smua.source.limitv)'))

    @limitv.setter
    def limitv(self, value):
        with self.lock:
            self.resource.write(f'smua.source.limitv = {value:E}')
            self.resource.waitcomplete()

    @property
    def limiti(self):
        with self.lock:
            return float(self.resource.query('print(smua.source.limiti)'))

    @limiti.setter
    def limiti(self, value):
        with self.lock:
            self.resource.write(f'smua.source.limiti = {value:E}')
            self.resource.waitcomplete()
