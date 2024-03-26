from typing import List, Set

from comet.emulator import IEC60488Emulator, message, run
from comet.emulator.utils import tsp_print, Error
from comet.utils import combine_matrix


class K707BEmulator(IEC60488Emulator):

    IDENTITY: str = "Keithley Inc., Model 707B, 43768438, v1.0 (Emulator)"
    CHANNELS = combine_matrix("1234", "ABCDEFGH", (format(i, "02d") for i in range(1, 13)))

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: List[Error] = []
        self.closed_channels: Set[str] = set()

    @message(r'^reset\(\)|\*RST$')
    def set_reset(self):
        self.error_queue.clear()

    @message(r'^clear\(\)|\*CLS$')
    def set_clear(self):
        self.error_queue.clear()

    @message(r'errorqueue\.clear\(\)')
    def set_errorqueue_clear(self):
        self.error_queue.clear()

    @message(tsp_print(r'errorqueue\.count'))
    def get_errorqueue_count(self):
        return format(len(self.error_queue), "d")

    @message(tsp_print(r'errorqueue\.next\(\)'))
    def get_errorqueue_next(self):
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = Error(0, "Queue is Empty")
        return f"{error.code}, \"{error.message}\", 0, 0"

    @message(tsp_print(r'channel\.getclose\(([^\)]+)\)'))
    def get_channel_getclose(self, channels):
        if not self.closed_channels:
            return "nil"
        return ";".join(sorted(self.closed_channels))

    @message(r'channel\.close\(([^\)]+)\)')
    def set_channel_close(self, channels):
        channels = channels.strip('"').split(',')
        self.closed_channels.update(channels)

    @message(r'channel\.open\(([^\)]+)\)')
    def set_channel_open(self, channels):
        channels = channels.strip('"').split(',')
        if "allslots" in channels:
            self.closed_channels.clear()
        else:
            for channel in channels:
                if channel in self.closed_channels:
                    self.closed_channels.remove(channel)

    @message(r'^(.*)$')
    def unknown_message(self, v):
        self.error_queue.append(Error(101, "malformed command"))


if __name__ == "__main__":
    run(K707BEmulator())
