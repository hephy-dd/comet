from abc import abstractmethod

from .instrument import Instrument

__all__ = ["SourceMeterUnit"]


class SourceMeterUnit(Instrument):

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    @property  # type: ignore
    @abstractmethod
    def output(self) -> bool:
        ...

    @output.setter  # type: ignore
    @abstractmethod
    def output(self, state: bool) -> None:
        ...

    FUNCTION_VOLTAGE: str = "voltage"
    FUNCTION_CURRENT: str = "current"

    @property  # type: ignore
    @abstractmethod
    def function(self) -> str:
        ...

    @function.setter  # type: ignore
    @abstractmethod
    def function(self, function: str) -> None:
        ...

    # Voltage source

    @property  # type: ignore
    @abstractmethod
    def voltage_level(self) -> float:
        ...

    @voltage_level.setter  # type: ignore
    @abstractmethod
    def voltage_level(self, level: float) -> None:
        ...

    @property  # type: ignore
    @abstractmethod
    def voltage_range(self) -> float:
        ...

    @voltage_range.setter  # type: ignore
    @abstractmethod
    def voltage_range(self, level: float) -> None:
        ...

    @property  # type: ignore
    @abstractmethod
    def voltage_compliance(self) -> float:
        ...

    @voltage_compliance.setter  # type: ignore
    @abstractmethod
    def voltage_compliance(self, level: float) -> None:
        ...

    # Current source

    @property  # type: ignore
    @abstractmethod
    def current_level(self) -> float:
        ...

    @current_level.setter  # type: ignore
    @abstractmethod
    def current_level(self, level: float) -> None:
        ...

    @property  # type: ignore
    @abstractmethod
    def current_range(self) -> float:
        ...

    @current_range.setter  # type: ignore
    @abstractmethod
    def current_range(self, level: float) -> None:
        ...

    @property  # type: ignore
    def current_compliance(self) -> float:
        ...

    @current_compliance.setter  # type: ignore
    @abstractmethod
    def current_compliance(self, level: float) -> None:
        ...

    @property
    @abstractmethod
    def compliance_tripped(self) -> bool:
        ...

    # Measurements

    @abstractmethod
    def measure_voltage(self) -> float:
        ...

    @abstractmethod
    def measure_current(self) -> float:
        ...