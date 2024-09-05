from abc import abstractmethod

from .instrument import Instrument

__all__ = ["SourceMeterUnit"]


class SourceMeterUnit(Instrument):
    # Output

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    @property
    @abstractmethod
    def output(self) -> bool: ...

    @output.setter
    @abstractmethod
    def output(self, state: bool) -> None: ...

    # Function

    FUNCTION_VOLTAGE: str = "voltage"
    FUNCTION_CURRENT: str = "current"

    @property
    @abstractmethod
    def function(self) -> str: ...

    @function.setter
    @abstractmethod
    def function(self, function: str) -> None: ...

    # Voltage source

    @property
    @abstractmethod
    def voltage_level(self) -> float: ...

    @voltage_level.setter
    @abstractmethod
    def voltage_level(self, level: float) -> None: ...

    @property
    @abstractmethod
    def voltage_range(self) -> float: ...

    @voltage_range.setter
    @abstractmethod
    def voltage_range(self, level: float) -> None: ...

    @property
    @abstractmethod
    def voltage_compliance(self) -> float: ...

    @voltage_compliance.setter
    @abstractmethod
    def voltage_compliance(self, level: float) -> None: ...

    # Current source

    @property
    @abstractmethod
    def current_level(self) -> float: ...

    @current_level.setter
    @abstractmethod
    def current_level(self, level: float) -> None: ...

    @property
    @abstractmethod
    def current_range(self) -> float: ...

    @current_range.setter
    @abstractmethod
    def current_range(self, level: float) -> None: ...

    @property
    @abstractmethod
    def current_compliance(self) -> float: ...

    @current_compliance.setter
    @abstractmethod
    def current_compliance(self, level: float) -> None: ...

    @property
    @abstractmethod
    def compliance_tripped(self) -> bool: ...

    # Measurements

    @abstractmethod
    def measure_voltage(self) -> float: ...

    @abstractmethod
    def measure_current(self) -> float: ...
