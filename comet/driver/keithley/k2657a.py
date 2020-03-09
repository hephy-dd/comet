from comet.driver import lock, Driver
from comet.driver import IEC60488
from comet.driver.iec60488 import opc_wait, opc_poll

__all__ = ['K2657A']

class Source(Driver):

    def __init__(self, resource, prefix):
        super().__init__(resource)
        self._prefix = prefix

    @property
    def output(self) -> int:
        return int(self.resource.query(f'print({self._prefix}.output)'))

    @output.setter
    @opc_wait
    def output(self, value: int):
        self.resource.write(f'{self._prefix}.output = {value:d}')

    @property
    def levelv(self) -> float:
        return float(self.resource.query(f'print({self._prefix}.levelv)'))

    @levelv.setter
    @opc_wait
    def levelv(self, value: float):
        self.resource.write(f'{self._prefix}.levelv = {value:E}')

    @property
    def leveli(self) -> float:
        return float(self.resource.query(f'print({self._prefix}.leveli)'))

    @leveli.setter
    @opc_wait
    def leveli(self, value: float):
        self.resource.write(f'{self._prefix}.leveli = {value:E}')

    @property
    def limitv(self) -> float:
        return float(self.resource.query(f'print({self._prefix}.limitv)'))

    @limitv.setter
    @opc_wait
    def limitv(self, value):
        self.resource.write(f'{self._prefix}.limitv = {value:E}')

    @property
    def limiti(self) -> float:
        return float(self.resource.query(f'print({self._prefix}.limiti)'))

    @limiti.setter
    @opc_wait
    def limiti(self, value: float):
        self.resource.write(f'{self._prefix}.limiti = {value:E}')

class SMU(Driver):

    def __init__(self, resource, prefix):
        super().__init__(resource)
        self.source = Source(resource, f'{prefix}.source')

class K2657A(IEC60488):
    """Keihtley Model 2657A High Power System SourceMeter."""

    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.smua = SMU(self.resource, 'smua')
        self.smub = SMU(self.resource, 'smub')
