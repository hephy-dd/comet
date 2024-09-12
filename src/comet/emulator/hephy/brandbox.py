from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ["BrandBoxEmulator"]


def split_channels(channels: str) -> list[str]:
    return list({channel.strip() for channel in channels.split(",") if channel.strip()})


def join_channels(channels: list[str]) -> str:
    return ",".join([format(channel) for channel in channels])


def format_state(state: bool) -> str:
    return "ON" if state else "OFF"


def format_error(code: int) -> str:
    return f"Err{abs(code):d}"


class BrandBoxEmulator(Emulator):

    CHANNELS: list[str] = ["A1", "A2", "B1", "B2", "C1", "C2"]
    MODS: list[str] = ["IV", "CV"]

    IDENTITY: str = "BrandBox, v2.0 (Emulator)"
    SUCCESS: str = "OK"
    COMMAND_ERROR: str = format_error(99)

    def __init__(self) -> None:
        super().__init__()
        self.closed_channels: set[str] = set()
        self.test_state: bool = False
        self.mod: str = "N/A"

    @property
    def opened_channels(self) -> set[str]:
        return set(self.CHANNELS) - self.closed_channels

    @message(r'\*IDN\?')
    def get_idn(self) -> str:
        return self.options.get("identity", self.IDENTITY)

    @message(r'\*RST')
    def set_rst(self) -> str:
        return self.SUCCESS

    @message(r'\*CLS')
    def set_cls(self) -> str:
        return self.SUCCESS

    @message(r'\*STB\?')
    def get_stb(self) -> str:
        states = []
        for channel in self.CHANNELS:
            states.append("1" if channel in self.closed_channels else "0")
        return ",".join(states)

    @message(r'\*STR\?')
    def get_str(self) -> str:
        return "0"

    @message(r'\*OPC\?')
    def get_opc(self) -> str:
        return "1"

    @message(r':CLOS (.+)')
    def set_close(self, channels) -> str:
        for channel in split_channels(channels):
            if self.has_channel(channel):
                self.closed_channels.add(channel)
            else:
                return self.COMMAND_ERROR
        return self.SUCCESS

    @message(r':OPEN (.+)')
    def set_open(self, channels) -> str:
        for channel in split_channels(channels):
            if self.has_channel(channel):
                if channel in self.closed_channels:
                    self.closed_channels.remove(channel)
            else:
                return self.COMMAND_ERROR
        return self.SUCCESS

    @message(r':CLOS:STAT\?')
    def get_close_state(self) -> str:
        return join_channels(sorted(self.closed_channels))

    @message(r':OPEN:STAT\?')
    def get_open_state(self) -> str:
        return join_channels(sorted(self.opened_channels))

    @message(r':DEBUG?')
    def get_debug(self) -> str:
        return self.COMMAND_ERROR

    @message(r'SET:A_(ON|OFF)')
    def set_a(self, state) -> str:
        for channel in ("A1", "A2"):
            if state == "ON":
                self.closed_channels.add(channel)
            else:
                if channel in self.closed_channels:
                    self.closed_channels.remove(channel)
        return self.SUCCESS

    @message(r'SET:B_(ON|OFF)')
    def set_b(self, state) -> str:
        for channel in ("B1", "B2"):
            if state == "ON":
                self.closed_channels.add(channel)
            else:
                if channel in self.closed_channels:
                    self.closed_channels.remove(channel)
        return self.SUCCESS

    @message(r'SET:C_(ON|OFF)')
    def set_c(self, state) -> str:
        for channel in ("C1", "C2"):
            if state == "ON":
                self.closed_channels.add(channel)
            else:
                if channel in self.closed_channels:
                    self.closed_channels.remove(channel)
        return self.SUCCESS

    @message(r'SET:(A1|A2|B1|B2|C1|C2)_(ON|OFF)')
    def set_abc(self, channel, state) -> str:
        if state == "ON":
            self.closed_channels.add(channel)
        else:
            if channel in self.closed_channels:
                self.closed_channels.remove(channel)
        return self.SUCCESS

    @message(r'SET:MOD (IV|CV)')
    def set_mod(self, mod) -> str:
        if mod not in self.MODS:
            return self.COMMAND_ERROR
        self.mod = mod
        return self.SUCCESS

    @message(r'GET:A \?')
    def get_a(self) -> str:
        states = []
        for channel in ("A1", "A2"):
            states.append(format_state(channel in self.closed_channels))
        return ",".join(states)

    @message(r'GET:B \?')
    def get_b(self) -> str:
        states = []
        for channel in ("B1", "B2"):
            states.append(format_state(channel in self.closed_channels))
        return ",".join(states)

    @message(r'GET:C \?')
    def get_c(self) -> str:
        states = []
        for channel in ("C1", "C2"):
            states.append(format_state(channel in self.closed_channels))
        return ",".join(states)

    @message(r'GET:(A1|A2|B1|B2|C1|C2) \?')
    def get_abc(self, channel) -> str:
        return format_state(channel in self.closed_channels)

    @message(r'GET:MOD \?')
    def get_mod(self) -> str:
        return format(self.mod)

    @message(r'GET:TST \?')
    def get_test(self) -> str:
        return {False: "OFF", True: "ON"}[self.test_state]

    @message(r'SET:TST (ON|OFF)')
    def set_test(self, value) -> str:
        self.test_state = value == "ON"
        return self.SUCCESS

    @message(r'.*')
    def unknown_message(self) -> str:
        return self.COMMAND_ERROR

    def has_channel(self, channel) -> bool:
        return channel in self.CHANNELS


if __name__ == "__main__":
    run(BrandBoxEmulator())
