from abc import abstractmethod
from typing import List

from .instrument import Instrument

__all__ = ["SwitchingMatrix"]


class SwitchingMatrix(Instrument):
    CHANNELS: List[str] = []

    @property
    @abstractmethod
    def closed_channels(self) -> List[str]: ...

    @abstractmethod
    def close_channels(self, channels: List[str]) -> None: ...

    @abstractmethod
    def open_channels(self, channels: List[str]) -> None: ...

    @abstractmethod
    def open_all_channels(self) -> None: ...
