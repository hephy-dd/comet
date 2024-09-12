from abc import abstractmethod

from .instrument import Instrument

__all__ = ["SwitchingMatrix"]


class SwitchingMatrix(Instrument):
    CHANNELS: list[str] = []

    @property
    @abstractmethod
    def closed_channels(self) -> list[str]: ...

    @abstractmethod
    def close_channels(self, channels: list[str]) -> None: ...

    @abstractmethod
    def open_channels(self, channels: list[str]) -> None: ...

    @abstractmethod
    def open_all_channels(self) -> None: ...
