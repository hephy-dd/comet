from abc import abstractmethod

from typing import Iterator

from .instrument import Driver, Instrument

__all__ = ["PowerSupply", "PowerSupplyChannel"]


class PowerSupplyChannel(Driver):

    def __init__(self, resource, channel: int) -> None:
        super().__init__(resource)
        self.channel: int = channel

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    @property
    @abstractmethod
    def enabled(self) -> bool: ...

    @enabled.setter
    @abstractmethod
    def enabled(self, state: bool) -> None: ...

    # Voltage source

    @property
    @abstractmethod
    def voltage_level(self) -> float: ...

    @voltage_level.setter
    @abstractmethod
    def voltage_level(self, level: float) -> None: ...

    # Current source

    @property
    @abstractmethod
    def current_limit(self) -> float: ...

    @current_limit.setter
    @abstractmethod
    def current_limit(self, level: float) -> None: ...

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
    def __iter__(self) -> Iterator[PowerSupplyChannel]: ...

    @abstractmethod
    def __len__(self) -> int: ...
