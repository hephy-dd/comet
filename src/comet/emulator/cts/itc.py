"""CTS ITC climate chamber emulator."""

import random
from datetime import UTC, datetime

from comet.emulator import Context, Emulator, message, run

__all__ = ["ITCEmulator"]


def fake_analog_channel(channel, minimum, maximum):
    """Retruns analog channel fake reading."""
    actual = random.uniform(minimum, maximum)
    target = random.uniform(minimum, maximum)
    return f"{channel} {actual:05.1f} {target:05.1f}"


class ITCEmulator(Emulator):
    IDENTITY: str = "ITS Climate Chamber, v1.0 (Emulator)"

    def __init__(self, context: Context) -> None:
        super().__init__(context)

        options = context.options

        self.current_temp: float = float(options.get("current_temp", 24.0))
        self.target_temp: float = float(options.get("target_temp", 24.0))

        self.current_humid: float = float(options.get("current_humid", 55.0))
        self.target_humid: float = float(options.get("target_humid", 55.0))

        self.program: int = 0

    @message(r"T$")
    def get_t(self) -> str:
        return datetime.now(tz=UTC).strftime("T%d%m%y%H%M%S")

    @message(r"(t\d{6}\d{6})$")
    def set_t(self, value) -> str:
        t = datetime.strptime(value, "t%d%m%y%H%M%S").replace(tzinfo=UTC)
        return t.strftime("t%d%m%y%H%M%S")

    @message(r"(A0)$")
    def get_a0(self, channel) -> str:
        self.current_temp += random.uniform(-0.25, +0.25)
        self.current_temp = min(60.0, max(20.0, self.current_temp))
        return f"{channel} {self.current_temp:05.1f} {self.target_temp:05.1f}"

    @message(r"(A[34])$")
    def get_a3(self, channel) -> str:
        return fake_analog_channel(channel, -45.0, +185.0)

    @message(r"(A1)$")
    def get_a1(self, channel) -> str:
        self.current_humid += random.uniform(-0.25, +0.25)
        self.current_humid = min(95.0, max(15.0, self.current_humid))
        return f"{channel} {self.current_humid:05.1f} {self.target_humid:05.1f}"

    @message(r"(A2)$")
    def get_a2(self, channel) -> str:
        return fake_analog_channel(channel, +0.0, +15.0)

    @message(r"(A[56])$")
    def get_a5(self, channel) -> str:
        return fake_analog_channel(channel, +5.0, +98.0)

    @message(r"(A7)$")
    def get_a7(self, channel) -> str:
        return fake_analog_channel(channel, -50.0, +150.0)

    @message(r"(A8)$")
    def get_a8(self, channel) -> str:
        return fake_analog_channel(channel, -80.0, +190.0)

    @message(r"(A9)$")
    def get_a9(self, channel) -> str:
        return fake_analog_channel(channel, -0.0, +25.0)

    @message(r"(A\:)$")
    def get_a10(self, channel) -> str:
        return fake_analog_channel(channel, -50.0, +100.0)

    @message(r"(A\;)$")
    def get_a11(self, channel) -> str:
        return fake_analog_channel(channel, -0.0, +25.0)

    @message(r"(A\<)$")
    def get_a12(self, channel) -> str:
        return fake_analog_channel(channel, +2.0, +5.0)

    @message(r"(A[\=\>])$")
    def get_a13(self, channel) -> str:
        return fake_analog_channel(channel, -100.0, +200.0)

    @message(r"(A\?)$")
    def get_a14(self, channel) -> str:
        return fake_analog_channel(channel, -80.0, +200.0)

    @message(r"a[1-7]\s(-?\d+.\d)$")
    def set_a15(self, value) -> str:
        return "a"

    @message(r"a[0-6]\s+\d+\.\d+$")
    def set_a(self) -> str:
        return "a"

    @message(r"O$")
    def get_o(self) -> str:
        return "O1000000000000"

    @message(r"S$")
    def get_s(self) -> str:
        return "S11110100\x06"

    @message(r"P$")
    def get_p(self) -> str:
        return f"P{self.program:03d}"

    @message(r"p(\d{3})$")
    def set_p(self, program) -> str:
        self.program = int(program)
        return f"p{self.program:03d}"


if __name__ == "__main__":
    run(ITCEmulator)
