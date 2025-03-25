from abc import abstractmethod
from .instrument import Instrument

__all__ = ["DigitalMultiMeter"]


class DigitalMultiMeter(Instrument):

    # Measurements

    @abstractmethod
    def measure_voltage(self) -> float: ...

    @abstractmethod
    def measure_current(self) -> float: ...
