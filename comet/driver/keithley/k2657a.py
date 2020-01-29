from comet.driver import lock, Driver
from comet.driver import IEC60488
from comet.driver.iec60488 import opc_wait, opc_poll

__all__ = ['K2657A']

class Source(Driver):

    @property
    def _smu(self):
        return self.kwargs.get('smu')

    @property
    def output(self) -> int:
        return int(self.resource.query(f'print({self._smu}.source.output)'))

    @output.setter
    @opc_wait
    def output(self, value: int):
        self.resource.write(f'{self._smu}.source.output = {value:d}')

    @property
    def levelv(self) -> float:
        return float(self.resource.query(f'print({self._smu}.source.levelv)'))

    @levelv.setter
    @opc_wait
    def levelv(self, value: float):
        self.resource.write(f'{self._smu}.source.levelv = {value:E}')

    @property
    def leveli(self) -> float:
        return float(self.resource.query(f'print({self._smu}.source.leveli)'))

    @leveli.setter
    @opc_wait
    def leveli(self, value: float):
        self.resource.write(f'{self._smu}.source.leveli = {value:E}')

    @property
    def limitv(self) -> float:
        return float(self.resource.query(f'print({self._smu}.source.limitv)'))

    @limitv.setter
    @opc_wait
    def limitv(self, value):
        self.resource.write(f'{self._smu}.source.limitv = {value:E}')

    @property
    def limiti(self) -> float:
        return float(self.resource.query(f'print({self._smu}.source.limiti)'))

    @limiti.setter
    @opc_wait
    def limiti(self, value: float):
        self.resource.write(f'{self._smu}.source.limiti = {value:E}')

class SMU(Driver):

    source = Source()

class K2657A(IEC60488):
    """Keihtley Model 2657A High Power System SourceMeter."""

    smua = SMU(smu='smua')
    smub = SMU(smu='smub')
