from abc import abstractmethod
from typing import Tuple

from .instrument import Instrument

__all__ = ["LCRMeter"]


class LCRMeter(Instrument):

    @property  # type: ignore
    @abstractmethod
    def function(self) -> str:
        ...

    @function.setter  # type: ignore
    @abstractmethod
    def function(self, function: str) -> None:
        ...

    @property  # type: ignore
    @abstractmethod
    def amplitude(self) -> float:
        ...

    @amplitude.setter  # type: ignore
    @abstractmethod
    def amplitude(self, level: float) -> None:
        ...

    @property  # type: ignore
    @abstractmethod
    def frequency(self) -> float:
        ...

    @frequency.setter  # type: ignore
    @abstractmethod
    def frequency(self, frequency: float) -> None:
        ...

    @abstractmethod
    def measure_impedance(self) -> Tuple[float, float]:
        ...
