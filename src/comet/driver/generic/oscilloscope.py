from abc import abstractmethod

from typing import Iterator

from .instrument import Driver, Instrument

__all__ = ["Oscilloscope", "OscilloscopeChannel"]


class OscilloscopeChannel(Driver):

    def __init__(self, resource, channel: int) -> None:
        super().__init__(resource)
        self.channel: int = channel

    @property
    @abstractmethod
    def enabled(self) -> bool: ...

    @enabled.setter
    @abstractmethod
    def enabled(self, state: bool) -> None: ...

    @abstractmethod
    def time_axis(self) -> list[float]: ...

    @abstractmethod
    def acquire_waveform(self) -> list[float]: ...


class Oscilloscope(Instrument):

    @abstractmethod
    def __getitem__(self, channel: int) -> OscilloscopeChannel: ...

    @abstractmethod
    def __iter__(self) -> Iterator[OscilloscopeChannel]: ...

    @abstractmethod
    def __len__(self) -> int: ...
