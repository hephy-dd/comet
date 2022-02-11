from typing import Optional

from comet.driver.generic import SourceMeterUnit
from comet.driver.generic import InstrumentError

__all__ = ['K2657A']


class K2657A(SourceMeterUnit):

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')

    def clear(self) -> None:
        self.write('*CLS')

    def set_mute(self, state: bool) -> None:
        self.tsp_assign('beeper.enable', format(state, 'd'))


    # Error queue

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.tsp_print('errorqueue.next()').split('\t')[:2]
        if int(code):
            return InstrumentError(int(code), message.strip('\"\' '))
        return None

    # Source meter unit

    @property
    def output(self) -> bool:
        value = int(float(self.tsp_print('smua.source.output')))
        return {
            0: self.OUTPUT_OFF,
            1: self.OUTPUT_ON
        }[value]

    @output.setter
    def output(self, state: bool) -> None:
        value = {
            self.OUTPUT_OFF: 0,
            self.OUTPUT_ON: 1
        }[state]
        self.tsp_assign('smua.source.output', format(value, 'd'))

    @property
    def function(self) -> str:
        value = int(float(self.tsp_print('smua.source.func')))
        return {
            1: self.FUNCTION_VOLTAGE,
            0: self.FUNCTION_CURRENT
        }[value]

    @function.setter
    def function(self, function: str) -> None:
        value = {
            self.FUNCTION_VOLTAGE: 1,
            self.FUNCTION_CURRENT: 0
        }[function]
        self.tsp_assign('smua.source.func', format(value, 'd'))

    def get_voltage(self) -> float:
        return float(self.tsp_print('smua.source.levelv'))

    def set_voltage(self, level: float) -> None:
        self.tsp_assign('smua.source.levelv', format(level, 'E'))

    def get_voltage_range(self) -> float:
        return float(self.tsp_print('smua.source.rangev'))

    def set_voltage_range(self, level: float) -> None:
        self.tsp_assign('smua.source.rangev', format(level, 'E'))

    # Compliance voltage

    def get_voltage_compliance(self) -> float:
        return float(self.tsp_print('smua.source.limitv'))

    def set_voltage_compliance(self, level: float) -> None:
        self.tsp_assign('smua.source.limitv', format(level, 'E'))

    def get_current(self) -> float:
        return float(self.tsp_print('smua.source.leveli'))

    def set_current(self, level: float) -> None:
        self.tsp_assign('smua.source.leveli', format(level, 'E'))

    def get_current_range(self) -> float:
        return float(self.tsp_print('smua.source.rangei'))

    def set_current_range(self, level: float) -> None:
        self.tsp_assign('smua.source.rangei', format(level, 'E'))

    # Compliance current

    def get_current_compliance(self) -> float:
        return float(self.tsp_print('smua.source.limiti'))

    def set_current_compliance(self, level: float) -> None:
        self.tsp_assign('smua.source.limiti', format(level, 'E'))

    # Compliance tripped

    def compliance_tripped(self) -> bool:
        return {'false': False, 'true': True}[self.tsp_print('smua.source.compliance')]

    # Measure

    def measure_voltage(self) -> float:
        return float(self.tsp_print('smua.measure.v()'))

    def measure_current(self) -> float:
        return float(self.tsp_print('smua.measure.i()'))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query('*OPC?')

    def tsp_print(self, expression: str) -> str:
        return self.query(f'print({expression})')

    def tsp_assign(self, expression: str, value: str) -> str:
        self.write(f'{expression} = {value}')
