from comet.devices import IEC60488
from comet.device import Group, Mapping

__all__ = ['K2656A']

class SMU(Group):

    def __init__(self, parent, root):
        super().__init__(parent)
        self.__source = Source(self, root=f'{root}.source')

    @property
    def source(self):
        return self.__source

class Source(Group):

    OutputMapping = Mapping({'off': 0, 'on': 1, 'high_z': 2})

    def __init__(self, parent, root):
        super().__init__(parent)
        self.__root = root

    @property
    def output(self):
        return self.OutputMapping.get_key(self.resource.query(f'print({self.__root}.output)'))

    @output.setter
    def output(self, value):
        value = self.OutputMapping.get_value(value)
        with self.lock:
            self.resource.write(f'{self.__root}.output = {value}')
            self.resource.query('*OPC?')

    @property
    def levelv(self):
        with self.lock:
            return float(self.resource.query(f'print({self.__root}.levelv)'))

    @levelv.setter
    def levelv(self, value):
        with self.lock:
            self.resource.write(f'{self.__root}.levelv = {value:E}')
            self.resource.query('*OPC?')

    @property
    def leveli(self):
        with self.lock:
            return float(self.resource.query(f'print({self.__root}.leveli)'))

    @leveli.setter
    def leveli(self, value):
        with self.lock:
            self.resource.write(f'{self.__root}.leveli = {value:E}')
            self.resource.query('*OPC?')

    @property
    def limitv(self):
        with self.lock:
            return float(self.resource.query(f'print({self.__root}.limitv)'))

    @limitv.setter
    def limitv(self, value):
        with self.lock:
            self.resource.write(f'{self.__root}.limitv = {value:E}')
            self.resource.query('*OPC?')

    @property
    def limiti(self):
        with self.lock:
            return float(self.resource.query(f'print({self.__root}.limiti)'))

    @limiti.setter
    def limiti(self, value):
        with self.lock:
            self.resource.write(f'{self.__root}.limiti = {value:E}')
            self.resource.query('*OPC?')

class K2656A(IEC60488):

    options = {
        'encoding': 'latin1',
        'read_termination': '\r',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__smua = SMU(self, root='smua')
        self.__smub = SMU(self, root='smub')

    @property
    def smua(self):
        return self.__smua

    @property
    def smub(self):
        return self.__smub
