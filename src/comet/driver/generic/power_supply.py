from abc import abstractmethod

from .instrument import Driver, Instrument

__all__ = ["PowerSupply", "PowerSupplyChannel"]


class PowerSupplyChannel(Instrument):

    def __init__(self, resource, channel: int) -> None:
        super().__init__(resource)
        self.channel: int = channel

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    @property  # type: ignore
    @abstractmethod
    def enabled(self) -> bool: ...

    @enabled.setter  # type: ignore
    @abstractmethod
    def enabled(self, state: bool) -> None: ...

    # Voltage source

    @property  # type: ignore
    @abstractmethod
    def voltage_level(self) -> float: ...

    @voltage_level.setter  # type: ignore
    @abstractmethod
    def voltage_level(self, level: float) -> None: ...

    # Current source
    @property  # type: ignore
    def current_compliance(self) -> float: ...

    @current_compliance.setter  # type: ignore
    @abstractmethod
    def current_compliance(self, level: float) -> None: ...

    # Measurements

    @abstractmethod
    def measure_voltage(self) -> float: ...

    @abstractmethod
    def measure_current(self) -> float: ...

    @abstractmethod
    def measure_power(self) -> float: ...


class PowerSupply(Instrument):
    @abstractmethod
    def __getitem__(self, channel: int) -> PowerSupplyChannel: ...

    @abstractmethod
    def __iter__(self) -> PowerSupplyChannel: ...
