import random
import time

from comet.emulator import IEC60488Emulator, message, run


class E4980AEmulator(IEC60488Emulator):

    IDENTITY = "Keysight Inc., Model E4980A, v1.0 (Emulator)"

    CORRECTION_OPEN_DELAY = 4.0

    def __init__(self) -> None:
        super().__init__()
        self.correction_open_state: int = 0
        self.correction_use: int = 0
        self.correction_method: str = 'SING'
        self.correction_channel: int = 0
        self.correction_length: int = 4
        self.bias_voltage_level: float = 0.
        self.bias_state: bool = False

    @message(r':SYST(?:EM)?:ERR(?:OR)?(?::NEXT)?\?')
    def get_system_error(self) -> str:
        return '+0, "no error"'

    @message(r':?CORR:OPEN:STAT\?')
    def get_correction_open_state(self) -> str:
        return format(self.correction_open_state, 'd')

    @message(r'^:?CORR:OPEN:STAT\s+(OFF|ON|0|1)$')
    def set_correction_open_state(self, state: str) -> None:
        self.correction_open_state = {'0': False, '1': True, 'OFF': False, 'ON': True}[state]

    @message(r':?CORR:OPEN')
    def get_correction_open(self) -> None:
        time.sleep(type(self).CORRECTION_OPEN_DELAY)

    @message(r':?CORR:USE\?')
    def get_correction_use(self) -> str:
        return format(self.correction_use, '+d')

    @message(r':?CORR:METH\?')
    def get_correction_method(self) -> str:
        return self.correction_method

    @message(r':?CORR:METH\s+(SING|MULT)')
    def set_correction_method_single(self, method: str) -> None:
        self.correction_method = method

    @message(r':?CORR:USE:CHAN\?')
    def get_correction_channel(self) -> str:
        return format(self.correction_channel, 'd')

    @message(r':?CORR:USE:CHAN\s+(\d+)')
    def set_correction_channel(self, value):
        self.correction_channel = int(value)

    @message(r':?CORR:LENG\?')
    def get_correction_length(self) -> str:
        return format(self.correction_length, '+d')

    @message(r':?CORR:LENG\s+(\d+)')
    def set_correction_length(self, length: str) -> None:
        self.correction_length = int(length)

    @message(r':?FETC[H]?(?:(?::IMP)?:FORM)?\?')
    def get_fetch(self):
        return '{:E},{:E},{:+d}'.format(random.random(), random.random(), 0)

    @message(r':?BIAS:POL:CURR(\::LEV)?\?')
    def get_bias_polarity_current_level(self):
        return format(random.random() / 1000., 'E')

    @message(r':?BIAS:POL:VOLT(\::LEV)?\?')
    def get_bias_polarity_voltage_level(self):
        return format(random.random() / 100., 'E')

    @message(r':?BIAS:VOLT(?::LEV)?\?')
    def get_bias_voltage_level(self):
        return format(self.bias_voltage_level, 'E')

    @message(r':?BIAS:VOLT(?::LEV)?\s+(.+)')
    def set_bias_voltage_level(self, value):
        self.bias_voltage_level = float(value)

    @message(r':?BIAS:STAT\?')
    def get_bias_state(self):
        return format(self.bias_state, 'd')

    @message(r':?BIAS:STAT\s+(0|1|ON|OFF)')
    def set_bias_state(self, value):
        self.bias_state = {'0': False, '1': True, 'OFF': False, 'ON': True}[value]


if __name__ == '__main__':
    run(E4980AEmulator())
