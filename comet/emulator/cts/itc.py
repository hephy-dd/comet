"""CTS ITC emulator."""

import datetime
import random
import time

from comet.emulator.emulator import message, run
from comet.emulator.emulator import RequestHandler

__all__ = ['ITCHandler']

def fake_analog_channel(channel, minimum, maximum):
    """Retruns analog channel fake reading."""
    actual = random.uniform(minimum, maximum)
    target = random.uniform(minimum, maximum)
    return f'{channel} {actual:05.1f} {target:05.1f}'

class ITCHandler(RequestHandler):
    """ITC request handler."""

    identification = "Spanish Inquisition Inc., ITS Climate Chamber, v1.0"
    current_temp = 24.0
    target_temp = 24.0
    current_humid = 55.0
    target_humid = 55.0

    @message(r'T')
    def query_get_t(self, message):
        return datetime.datetime.now().strftime('T%d%m%y%H%M%S')

    @message(r't\d{12}')
    def query_set_t(self, message):
        t = datetime.datetime.strptime(message, 't%d%m%y%H%M%S')
        return t.strftime('T%d%m%y%H%M%S')

    @message(r'A0')
    def query_get_a(self, message):
        self.current_temp += random.uniform(-.25, +.25)
        self.current_temp = min(60., max(20., self.current_temp))
        return f'{message} {self.current_temp:05.1f} {self.target_temp:05.1f}'

    @message(r'A[34]')
    def query_get_a(self, message):
        return fake_analog_channel(message, -45., +185.)

    @message(r'A1')
    def query_get_a(self, message):
        self.current_humid += random.uniform(-.25, +.25)
        self.current_humid = min(95., max(15., self.current_humid))
        return f'{message} {self.current_humid:05.1f} {self.target_humid:05.1f}'

    @message(r'A2')
    def query_get_a(self, message):
        return fake_analog_channel(message, +0., +15.)

    @message(r'A[56]')
    def query_get_a(self, message):
        return fake_analog_channel(message, +5., +98.)

    @message(r'A7')
    def query_get_a(self, message):
        return fake_analog_channel(message, -50., +150.)

    @message(r'A8')
    def query_get_a(self, message):
        return fake_analog_channel(message, -80., +190.)

    @message(r'A9')
    def query_get_a(self, message):
        return fake_analog_channel(message, -0., +25.)

    @message(r'A\:')
    def query_get_a(self, message):
        return fake_analog_channel(message, -50., +100.)

    @message(r'A\;')
    def query_get_a(self, message):
        return fake_analog_channel(message, -0., +25.)

    @message(r'A\<')
    def query_get_a(self, message):
        return fake_analog_channel(message, +2., +5.)

    @message(r'A[\=\>]')
    def query_get_a(self, message):
        return fake_analog_channel(message, -100., +200.)

    @message(r'A\?')
    def query_get_a(self, message):
        return fake_analog_channel(message, -80., +200.)

    @message(r'a[1-7]\s(-?\d+.\d)')
    def query_set_a(self, message):
        return 'a'

    @message(r'S')
    def query_get_s(self, message):
        return 'S11110100\x06'

    @message(r'P')
    def query_get_p(self, message):
        return 'P000'

    @message(r'P\d{3}')
    def query_set_p(self, message):
        return message

    @message(r'a[0-6]\s+\d+\.\d+')
    def query_set_a(self, message):
        return 'a'

if __name__ == "__main__":
    run(ITCHandler)
