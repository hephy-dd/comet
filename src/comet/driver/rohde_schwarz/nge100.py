from typing import Optional, Iterator

from comet.driver.generic import InstrumentError
from comet.driver.generic.power_supply import PowerSupply, PowerSupplyChannel

__all__ = ["NGE100", "NGE100Channel"]


class NGE100Channel(PowerSupplyChannel):
    """Single channel of the NGE100 power supply"""

    @property
    def enabled(self) -> bool:
        value = int(self.query("OUTPut?"))
        return {0: self.OUTPUT_OFF, 1: self.OUTPUT_ON}[value]

    @enabled.setter
    def enabled(self, state: bool) -> None:
        value = {self.OUTPUT_OFF: 0, self.OUTPUT_ON: 1}[state]
        self.write(f"OUTPut {value}")

    @property
    def voltage_level(self) -> float:
        return float(self.query("SOURce:VOLTage:LEVel:IMMediate:AMPLitude?"))

    @voltage_level.setter
    def voltage_level(self, level: float) -> None:
        if level < 0:
            raise ValueError("Voltage level must be non-negative")
        if level > 32:
            raise ValueError("Voltage level must be less than 32 V")
        self.write(f"SOURce:VOLTage:LEVel:IMMediate:AMPLitude {level}")

    @property
    def current_limit(self) -> float:
        return float(self.query("SOURce:CURRent:LEVel:IMMediate:AMPLitude?"))

    @current_limit.setter
    def current_limit(self, level: float) -> None:
        if level < 0:
            raise ValueError("Current limit must be non-negative")
        if level > 3:
            raise ValueError("Current limit must be less than 3 A")
        self.write(f"SOURce:CURRent:LEVel:IMMediate:AMPLitude {level}")

    def measure_voltage(self) -> float:
        return float(self.query("MEASure:SCALar:VOLTage:DC?"))

    def measure_current(self) -> float:
        return float(self.query("MEASure:SCALar:CURRent:DC?"))

    def measure_power(self) -> float:
        return float(self.query("MEASure:SCALar:POWer?"))

    # Helper
    def query(self, message: str) -> str:
        self.resource.write(f"INSTrument {self.channel + 1}")
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(f"INSTrument {self.channel + 1}")
        self.resource.write(message)
        self.resource.query("*OPC?")


class NGE100(PowerSupply):
    """Rohde & Schwarz NGE100 power supply featuring multiple channels"""

    N_CHANNELS: int = 3

    def identify(self) -> str:
        return self.query("*IDN?")

    def reset(self) -> None:
        self.write("*RST")

    def clear(self) -> None:
        self.write("*CLS")

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.query("SYSTem:ERRor?").split(", ")
        if int(code):
            return InstrumentError(int(code), message.strip("'"))
        return None

    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query("*OPC?")

    def __getitem__(self, channel: int) -> NGE100Channel:
        if not isinstance(channel, int):
            raise TypeError("Channel index must be an integer")
        if channel not in range(type(self).N_CHANNELS):
            raise IndexError("Channel index out of range")
        return NGE100Channel(self.resource, channel)

    def __iter__(self) -> Iterator[NGE100Channel]:
        return iter([NGE100Channel(self.resource, channel) for channel in range(3)])

    def __len__(self) -> int:
        return type(self).N_CHANNELS
