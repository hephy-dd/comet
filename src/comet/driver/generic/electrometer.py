from abc import abstractmethod
from .instrument import Instrument

__all__ = ["Electrometer"]


class Electrometer(Instrument):

    # Measurements

    @abstractmethod
    def measure_voltage(self) -> float: ...

    @abstractmethod
    def measure_current(self) -> float: ...

    @abstractmethod
    def measure_resistance(self) -> float: ...

    @abstractmethod
    def measure_charge(self) -> float: ...
