from comet.driver import Driver

from comet.driver.tsp import TSP
from comet.driver.tsp import opc_wait

__all__ = ['K2470']

class K2470(TSP):
    """Keithley Model 2470 SourceMeter."""

    class Source(Driver):

        class Protect(Driver):

            @property
            def tripped(self) -> bool:
                return bool(float(self.resource.query('print(smu.source.protect.tripped)')))

        @property
        def autorange(self) -> bool:
            return bool(float(self.resource.query('print(smu.source.autorange)')))

        @autorange.setter
        @opc_wait
        def autorange(self, value: bool):
            self.resource.write(f'smu.source.autorange = {value:d}')

        @property
        def autodelay(self) -> bool:
            return bool(float(self.resource.query('print(smu.source.autodelay)')))

        @autodelay.setter
        @opc_wait
        def autodelay(self, value: bool):
            self.resource.write(f'smu.source.autodelay = {value:d}')

        @property
        def delay(self) -> float:
            return float(self.resource.query('print(smu.source.delay)'))

        @delay.setter
        @opc_wait
        def delay(self, value: float):
            self.resource.write(f'smu.source.delay = {value:E}')

        FUNC_DC_CURRENT = 'CURRENT'
        FUNC_DC_VOLTAGE = 'VOLTAGE'

        @property
        def func(self) -> str:
            value = int(float(self.resource.query('print(smu.source.func)')))
            return {
                0: self.FUNC_DC_CURRENT,
                1: self.FUNC_DC_VOLTAGE
            }[value]

        @func.setter
        @opc_wait
        def func(self, value: str):
            value = {
                self.FUNC_DC_CURRENT: 0,
                self.FUNC_DC_VOLTAGE: 1
            }[value]
            self.resource.write(f'smu.source.func = {value:d}')

        @property
        def highc(self) -> bool:
            return bool(float(self.resource.query('print(smu.source.highc)')))

        @highc.setter
        @opc_wait
        def highc(self, value: bool):
            self.resource.write(f'smu.source.highc = {value:d}')

        @property
        def level(self) -> float:
            return float(self.resource.query('print(smu.source.level)'))

        @level.setter
        @opc_wait
        def level(self, value):
            self.resource.write(f'smu.source.level = {value:E}')

        OFFMODE_NORMAL = 'NORMAL'
        OFFMODE_ZERO = 'ZERO'
        OFFMODE_HIGHZ = 'HIGHZ'
        OFFMODE_GUARD = 'GUARD'

        @property
        def offmode(self) -> str:
            value = int(float(self.resource.query('print(smu.source.offmode)')))
            return {
                0: self.OFFMODE_NORMAL,
                1: self.OFFMODE_ZERO,
                2: self.OFFMODE_HIGHZ,
                3: self.OFFMODE_GUARD
            }[value]

        @offmode.setter
        @opc_wait
        def offmode(self, value: str):
            value = {
                self.OFFMODE_NORMAL: 0,
                self.OFFMODE_ZERO: 1,
                self.OFFMODE_HIGHZ: 2,
                self.OFFMODE_GUARD: 3
            }[value]
            self.resource.write(f'smu.source.offmode = {value:d}')

        @property
        def output(self) -> bool:
            return bool(float(self.resource.query('print(smu.source.output)')))

        @output.setter
        @opc_wait
        def output(self, value: bool):
            self.resource.write(f'smu.source.output = {value:d}')

        def __init__(self, resource, **kwargs):
            super().__init__(resource, **kwargs)
            self.protect = self.Protect(resource)

    @property
    def beeper(self) -> bool:
        return bool(float(self.resource.query('print(beeper)')))

    @beeper.setter
    @opc_wait
    def beeper(self, value: bool):
        self.resource.write(f'beeper = {value:d}')

    def __init__(self, resource, **kwargs):
        super().__init__(resource, **kwargs)
        self.source = self.Source(resource)
