import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['ShuntBoxHandler']

start_time = time.time()
def uptime():
    return int(round(time.time() - start_time))

class ShuntBoxHandler(RequestHandler):
    """HEPHY ShuntBox request handler."""

    identification = "Spanish Inquisition Inc., Shuntbox, v1.0"
    memory_bytes = 4200
    channels = 10

    @message(r'\*IDN\?')
    def query_get_idn(self, message):
        return self.identification

    @message(r'GET:UP \?')
    def query_get_up(self, message):
        return format(uptime())

    @message(r'GET:RAM \?')
    def query_get_ram(self, message):
        return format(self.memory_bytes)

    @message(r'GET:TEMP ALL')
    def query_get_temp_all(self, message):
        values = []
        for i in range(self.channels):
            values.append(format(random.uniform(22.0, 26.0), '.1f'))
        return ",".join(values)

    @message(r'GET:TEMP \d+')
    def query_get_temp(self, message):
        return format(random.uniform(22.0, 26.0), '.1f')

    @message(r'SET:REL_(ON|OFF) (\d+|ALL)')
    def query_set_rel(self, message):
        return "OK"

    @message(r'GET:REL (\d+)')
    def query_get_rel(self, message):
        return "0"

    @message(r'GET:REL ALL')
    def query_get_rel_all(self, message):
        return ",".join(["0"] * self.channels + 4)

if __name__ == "__main__":
    run(ShuntBoxHandler)
