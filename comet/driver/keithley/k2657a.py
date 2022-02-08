from typing import Optional

from comet.driver.generic import SourceMeterUnit
from comet.driver.generic import InstrumentError

__all__ = ['K2657A']


class K2657A(SourceMeterUnit):

    def identify(self) -> str:
        return self.query('*IDN?')

    def reset(self) -> None:
        self.write('*RST')
        self.waitcomplete()

    def clear(self) -> None:
        self.write('*CLS')
        self.waitcomplete()

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.tsp_print('errorqueue.next()').split('\t')[:2]
        if int(code):
            return InstrumentError(int(code), message.strip('\"\' '))
        return None

    def set_mute(self, state: bool) -> None:
        self.write(f'beeper.enable = {state:d}')
        self.waitcomplete()

    def get_terminal(self) -> str:
        return self.TERMINAL_REAR

    def set_terminal(self, terminal: str) -> None:
        {self.TERMINAL_REAR: None}[terminal]

    def get_output(self) -> bool:
        value = int(float(self.tsp_print('smua.source.output')))
        return {
            0: self.OUTPUT_OFF,
            1: self.OUTPUT_ON
        }[value]

    def set_output(self, state: bool) -> None:
        value = {
            self.OUTPUT_OFF: 0,
            self.OUTPUT_ON: 1
        }[state]
        self.write(f'smua.source.output = {value:d}')
        self.waitcomplete()

    def get_function(self) -> str:
        value = int(float(self.tsp_print('smua.source.func')))
        return {
            1: self.FUNCTION_VOLTAGE,
            0: self.FUNCTION_CURRENT
        }[value]

    def set_function(self, function: str) -> None:
        value = {
            self.FUNCTION_VOLTAGE: 1,
            self.FUNCTION_CURRENT: 0
        }[function]
        self.write(f'smua.source.func = {value:d}')
        self.waitcomplete()

    def get_voltage(self) -> str:
        return float(self.tsp_print('smua.source.levelv'))

    def set_voltage(self, level: float) -> None:
        self.write(f'smua.source.levelv = {level:E}')
        self.waitcomplete()

    def get_voltage_range(self) -> str:
        return float(self.tsp_print('smua.source.rangev'))

    def set_voltage_range(self, level: float) -> None:
        self.write(f'smua.source.rangev = {level:E}')
        self.waitcomplete()

    # Compliance voltage

    def get_voltage_compliance(self) -> float:
        return float(self.tsp_print('smua.source.limitv'))

    def set_voltage_compliance(self, level: float) -> None:
        self.write(f'smua.source.limitv = {level:E}')
        self.waitcomplete()

    def get_current(self) -> str:
        return float(self.tsp_print('smua.source.leveli'))

    def set_current(self, level: float) -> None:
        self.write(f'smua.source.leveli = {level:E}')
        self.waitcomplete()

    def get_current_range(self) -> str:
        return float(self.tsp_print('smua.source.rangei'))

    def set_current_range(self, level: float) -> None:
        self.write(f'smua.source.rangei = {level:E}')
        self.waitcomplete()

    # Compliance current

    def get_current_compliance(self) -> float:
        return float(self.tsp_print('smua.source.limiti'))

    def set_current_compliance(self, level: float) -> None:
        self.write(f'smua.source.limiti = {level:E}')
        self.waitcomplete()

    # Compliance tripped

    def compliance_tripped(self) -> bool:
        return {'false': False, 'true': True}[self.tsp_print('smua.source.compliance')]

    # Measure

    def read_voltage(self) -> float:
        return float(self.tsp_print('smua.measure.v()'))

    def read_current(self) -> float:
        return float(self.tsp_print('smua.measure.i()'))

    # Helper

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)

    def tsp_print(self, expression: str) -> str:
        return self.query(f'print({expression})')

    def waitcomplete(self) -> None:
        self.query('*OPC?')
