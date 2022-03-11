"""HEPHY Shunt Box emulator."""

import random
import time

from comet.emulator import Emulator
from comet.emulator import message, run


__all__ = ['ShuntBoxEmulator']

start_time = time.time()


def uptime():
    return int(round(time.time() - start_time))


class ShuntBoxEmulator(Emulator):

    IDENTITY = 'ShuntBox, v1.0 (Emulator)'
    MEMORY_BYTES = 4200
    CHANNELS = 10
    SUCCESS = 'OK'

    @message(r'\*IDN\?')
    def get_idn(self):
        return self.IDENTITY

    @message(r'GET:UP \?')
    def get_up(self):
        return format(uptime())

    @message(r'GET:RAM \?')
    def get_ram(self):
        return format(self.MEMORY_BYTES)

    @message(r'GET:TEMP ALL')
    def get_temp_all(self):
        values = []
        for i in range(self.CHANNELS):
            values.append(format(random.uniform(22.0, 26.0), '.1f'))
        return ",".join(values)

    @message(r'GET:TEMP (\d+)')
    def get_temp(self, value):
        return format(random.uniform(22.0, 26.0), '.1f')

    @message(r'SET:REL_(ON|OFF) (\d+|ALL)')
    def set_rel(self, state, value):
        return self.SUCCESS

    @message(r'GET:REL (\d+)')
    def get_rel(self, value):
        return "0"

    @message(r'GET:REL ALL')
    def get_rel_all(self):
        return ",".join(["0"] * (self.CHANNELS + 4))

    @message(r'.*')
    def unknown_message(self):
        return 'Err99'


if __name__ == '__main__':
    run(ShuntBoxEmulator())
