from abc import abstractmethod
from typing import Tuple

from .instrument import Instrument

__all__ = ["LCRMeter"]


class LCRMeter(Instrument):

    @property
    @abstractmethod
    def function(self) -> str: ...

    @function.setter
    @abstractmethod
    def function(self, function: str) -> None: ...

    @property
    @abstractmethod
    def amplitude(self) -> float: ...

    @amplitude.setter
    @abstractmethod
    def amplitude(self, level: float) -> None: ...

    @property
    @abstractmethod
    def frequency(self) -> float: ...

    @frequency.setter
    @abstractmethod
    def frequency(self, frequency: float) -> None: ...

    @abstractmethod
    def measure_impedance(self) -> Tuple[float, float]: ...
