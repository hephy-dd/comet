import random

from comet.emulator import IEC60488Emulator, message, run


class E4980AEmulator(IEC60488Emulator):

    IDENTITY = "Keysight Inc., Model E4980A, v1.0 (Emulator)"

    def __init__(self):
        super().__init__()
        self.correction_method = 0
        self.correction_channel = 0
        self.bias_voltage_level = 0.
        self.bias_state = False

    @message(r':SYST:ERR\?')
    def get_system_error(self):
        return '0, "no error"'

    @message(r':?CORR:METH\?')
    def get_correction_method(self):
        return format(self.correction_method, 'd')

    @message(r':?CORR:METH\s+SING')
    def set_correction_method_single(self):
        self.correction_method = 0

    @message(r':?CORR:METH\s+MULT')
    def set_correction_method_multi(self):
        self.correction_method = 1

    @message(r':?CORR:USE:CHAN\?')
    def get_correction_channel(self):
        return self.correction_channel

    @message(r':?CORR:USE:CHAN\s+(\d+)')
    def set_correction_channel(self, value):
        self.correction_channel = int(value)

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


if __name__ == "__main__":
    run(E4980AEmulator())
