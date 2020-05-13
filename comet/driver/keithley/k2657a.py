from comet.driver import lock, Driver, Action, Property
from comet.driver import IEC60488
from comet.driver.iec60488 import opc_wait, opc_poll

__all__ = ['K2657A']

class Source(Driver):

    def __init__(self, resource, prefix):
        super().__init__(resource)
        self._prefix = prefix

    @Property(values={False: 'false', True: 'true'})
    def compliance(self) -> str:
        """Current compliance."""
        return self.resource.query(f'print({self._prefix}.compliance)')

    @Property(values={'DCAMPS': 0, 'DCVOLTS': 1})
    def func(self) -> int:
        return int(self.resource.query(f'print({self._prefix}.func)'))

    @func.setter
    @opc_wait
    def func(self, value: int):
        self.resource.write(f'{self._prefix}.func = {value:d}')

    @Property(values={'OFF': 0, 'ON': 1, 'HIGH_Z': 2})
    def output(self) -> int:
        return int(self.resource.query(f'print({self._prefix}.output)'))

    @output.setter
    @opc_wait
    def output(self, value: int):
        self.resource.write(f'{self._prefix}.output = {value:d}')

    @property
    def levelv(self) -> float:
        """Voltage level in Volt."""
        return float(self.resource.query(f'print({self._prefix}.levelv)'))

    @levelv.setter
    @opc_wait
    def levelv(self, value: float):
        self.resource.write(f'{self._prefix}.levelv = {value:E}')

    @property
    def leveli(self) -> float:
        """Current level in Ampere."""
        return float(self.resource.query(f'print({self._prefix}.leveli)'))

    @leveli.setter
    @opc_wait
    def leveli(self, value: float):
        self.resource.write(f'{self._prefix}.leveli = {value:E}')

    @property
    def levelp(self) -> float:
        """Power level in Watt."""
        return float(self.resource.query(f'print({self._prefix}.levelp)'))

    @levelp.setter
    @opc_wait
    def levelp(self, value: float):
        self.resource.write(f'{self._prefix}.levelp = {value:E}')

    @property
    def limitv(self) -> float:
        """Voltage limit."""
        return float(self.resource.query(f'print({self._prefix}.limitv)'))

    @limitv.setter
    @opc_wait
    def limitv(self, value):
        self.resource.write(f'{self._prefix}.limitv = {value:E}')

    @property
    def limiti(self) -> float:
        """Current limit."""
        return float(self.resource.query(f'print({self._prefix}.limiti)'))

    @limiti.setter
    @opc_wait
    def limiti(self, value: float):
        self.resource.write(f'{self._prefix}.limiti = {value:E}')

    @property
    def limitp(self) -> float:
        """Power limit."""
        return float(self.resource.query(f'print({self._prefix}.limitp'))

    @limitp.setter
    @opc_wait
    def limitp(self, value: float):
        self.resource.write(f'{self._prefix}.limitp = {value:E}')

class SMU(Driver):

    def __init__(self, resource, prefix):
        super().__init__(resource)
        self._prefix = prefix
        self.source = Source(resource, f'{prefix}.source')

    @Property(values={'LOCAL': 0, 'REMOTE': 1, 'CALA': 3})
    def sense(self) -> int:
        return int(self.resource.query(f'print({self._prefix}.sense)'))

    @sense.setter
    @opc_wait
    def sense(self, value: int):
        self.resource.write(f'{self._prefix}.sense = {value:d}')

    @Action()
    @opc_wait
    def reset(self):
        self.resource.write(f'{self._prefix}.reset()')

class K2657A(IEC60488):
    """Keihtley Model 2657A High Power System SourceMeter."""

    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.smua = SMU(self.resource, 'smua')
        self.smub = SMU(self.resource, 'smub')
