from typing import Optional, Iterator, List

import numpy as np

from comet.driver.generic import InstrumentError
from comet.driver.generic.oscilloscope import Oscilloscope, OscilloscopeChannel

__all__ = ["RTP164", "RTP164Channel"]


class RTP164Channel(OscilloscopeChannel):
    """Single channel of the RTP164 oscilloscope"""

    @property
    def enabled(self) -> bool:
        source = f"CHAN{self.channel + 1}"
        return bool(int(self.resource.query(f":{source}:STAT?")))

    @enabled.setter
    def enabled(self, state: bool) -> None:
        value = {False: "OFF", True: "ON"}[state]
        self.resource.write(f":CHAN{self.channel + 1}:STAT {value}")

    def time_axis(self) -> List[float]:
        source = f"CHAN{self.channel + 1}"
        head = self.resource.query(f":{source}:DATA:HEAD?").strip()
        xmin, xmax, pts, *_ = [float(x) for x in head.split(",")]
        t = np.linspace(xmin, xmax, int(pts), endpoint=True)
        return t.tolist()

    def acquire_waveform(self) -> List[float]:
        self.resource.write("SING")
        self.resource.query("*OPC?")

        source = f"CHAN{self.channel + 1}"
        values = self.resource.query_binary_values(f":{source}:DATA?", datatype="f", is_big_endian=False)
        return values


class RTP164(Oscilloscope):
    """Rohde & Schwarz RTP164 oscilloscope with 4 channels"""

    N_CHANNELS: int = 4

    def identify(self) -> str:
        return self.resource.query("*IDN?")

    def reset(self) -> None:
        raise NotImplementedError()  # dangerous

    def clear(self) -> None:
        self.resource.write("*CLS")
        self.resource.query("*OPC?")

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.resource.query("SYST:ERR?").split(",")
        if int(code):
            return InstrumentError(int(code), message.strip().strip("\""))
        return None

    def __getitem__(self, channel: int) -> RTP164Channel:
        if not isinstance(channel, int):
            raise TypeError("Channel index must be an integer")
        if channel not in range(type(self).N_CHANNELS):
            raise IndexError("Channel index out of range")
        return RTP164Channel(self.resource, channel)

    def __iter__(self) -> Iterator[RTP164Channel]:
        return iter([RTP164Channel(self.resource, channel) for channel in range(type(self).N_CHANNELS)])

    def __len__(self) -> int:
        return type(self).N_CHANNELS
