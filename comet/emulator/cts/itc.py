"""CTS ITC climate chamber emulator."""

import datetime
import random
import time

from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ["ITCEmulator"]


def fake_analog_channel(channel, minimum, maximum):
    """Retruns analog channel fake reading."""
    actual = random.uniform(minimum, maximum)
    target = random.uniform(minimum, maximum)
    return f"{channel} {actual:05.1f} {target:05.1f}"


class ITCEmulator(Emulator):

    IDENTITY: str = "ITS Climate Chamber, v1.0 (Emulator)"

    def __init__(self) -> None:
        super().__init__()

        self.current_temp: float = 24.0
        self.target_temp: float = 24.0

        self.current_humid: float = 55.0
        self.target_humid: float = 55.0

        self.program: int = 0

    @message(r'^T$')
    def get_t(self):
        return datetime.datetime.now().strftime("T%d%m%y%H%M%S")

    @message(r'^(t\d{6}\d{6})$')
    def set_t(self, value):
        t = datetime.datetime.strptime(value, "t%d%m%y%H%M%S")
        return t.strftime("T%d%m%y%H%M%S")

    @message(r'^(A0)$')
    def get_a0(self, channel):
        self.current_temp += random.uniform(-.25, +.25)
        self.current_temp = min(60., max(20., self.current_temp))
        return f"{channel} {self.current_temp:05.1f} {self.target_temp:05.1f}"

    @message(r'^(A[34])$')
    def get_a3(self, channel):
        return fake_analog_channel(channel, -45., +185.)

    @message(r'^(A1)$')
    def get_a1(self, channel):
        self.current_humid += random.uniform(-.25, +.25)
        self.current_humid = min(95., max(15., self.current_humid))
        return f"{channel} {self.current_humid:05.1f} {self.target_humid:05.1f}"

    @message(r'^(A2)$')
    def get_a2(self, channel):
        return fake_analog_channel(channel, +0., +15.)

    @message(r'^(A[56])$')
    def get_a5(self, channel):
        return fake_analog_channel(channel, +5., +98.)

    @message(r'^(A7)$')
    def get_a7(self, channel):
        return fake_analog_channel(channel, -50., +150.)

    @message(r'^(A8)$')
    def get_a8(self, channel):
        return fake_analog_channel(channel, -80., +190.)

    @message(r'^(A9)$')
    def get_a9(self, channel):
        return fake_analog_channel(channel, -0., +25.)

    @message(r'^(A\:)$')
    def get_a10(self, channel):
        return fake_analog_channel(channel, -50., +100.)

    @message(r'^(A\;)$')
    def get_a11(self, channel):
        return fake_analog_channel(channel, -0., +25.)

    @message(r'^(A\<)$')
    def get_a12(self, channel):
        return fake_analog_channel(channel, +2., +5.)

    @message(r'^(A[\=\>])$')
    def get_a13(self, channel):
        return fake_analog_channel(channel, -100., +200.)

    @message(r'^(A\?)$')
    def get_a14(self, channel):
        return fake_analog_channel(channel, -80., +200.)

    @message(r'^a[1-7]\s(-?\d+.\d)$')
    def set_a15(self, value):
        return "a"

    @message(r'^a[0-6]\s+\d+\.\d+$')
    def set_a(self):
        return "a"

    @message(r'^S$')
    def get_s(self):
        return "S11110100\x06"

    @message(r'^P$')
    def get_p(self):
        return f"P{self.program:03d}"

    @message(r'^P(\d{3})$')
    def set_p(self, program):
        self.program = int(program)
        return f"P{self.program:03d}"


if __name__ == "__main__":
    run(ITCEmulator())
