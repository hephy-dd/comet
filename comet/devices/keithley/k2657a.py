from comet.devices import IEC60488
from comet.device import Node, Mapping

__all__ = ['K2657A']

class SMU(Node):

    def __init__(self, parent, prefix):
        super().__init__(parent, prefix)
        self.__source = Source(self, prefix='.source')

    @property
    def source(self):
        return self.__source

class Source(Node):

    OutputMapping = Mapping({'off': 0, 'on': 1, 'high_z': 2})

    @property
    def output(self):
        return self.OutputMapping.get_key(self.resource.query(f'print({self.prefix}.output)'))

    @output.setter
    def output(self, value):
        value = self.OutputMapping.get_value(value)
        with self.lock:
            self.resource.write(f'{self.prefix}.output = {value}')
            self.resource.query('*OPC?')

    @property
    def levelv(self):
        with self.lock:
            return float(self.resource.query(f'print({self.prefix}.levelv)'))

    @levelv.setter
    def levelv(self, value):
        with self.lock:
            self.resource.write(f'{self.prefix}.levelv = {value:E}')
            self.resource.query('*OPC?')

    @property
    def leveli(self):
        with self.lock:
            return float(self.resource.query(f'print({self.prefix}.leveli)'))

    @leveli.setter
    def leveli(self, value):
        with self.lock:
            self.resource.write(f'{self.prefix}.leveli = {value:E}')
            self.resource.query('*OPC?')

    @property
    def limitv(self):
        with self.lock:
            return float(self.resource.query(f'print({self.prefix}.limitv)'))

    @limitv.setter
    def limitv(self, value):
        with self.lock:
            self.resource.write(f'{self.prefix}.limitv = {value:E}')
            self.resource.query('*OPC?')

    @property
    def limiti(self):
        with self.lock:
            return float(self.resource.query(f'print({self.prefix}.limiti)'))

    @limiti.setter
    def limiti(self, value):
        with self.lock:
            self.resource.write(f'{self.prefix}.limiti = {value:E}')
            self.resource.query('*OPC?')

class K2657A(IEC60488):
    """Keihtley Model 2657A High Power System SourceMeter."""

    options = {
        'encoding': 'latin1',
        'read_termination': '\r\n',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__smua = SMU(self, prefix='smua')
        self.__smub = SMU(self, prefix='smub')

    @property
    def smua(self):
        return self.__smua

    @property
    def smub(self):
        return self.__smub
