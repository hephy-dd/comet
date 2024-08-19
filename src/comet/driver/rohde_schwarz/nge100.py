from typing import Optional, Iterator

from comet.driver.generic import InstrumentError
from comet.driver.generic.power_supply import PowerSupply, PowerSupplyChannel


__all__ = ["NGE100", "NGE100Channel"]


class NGE100Channel(PowerSupplyChannel):
    """Single channel of the NGE100 power supply"""

    def identify(self) -> str:
        return self.query("*IDN?") + ", Channel " + str(self.channel)

    def reset(self) -> None:
        self.write("*RST")

    def clear(self) -> None:
        self.write("*CLS")

    def next_error(self) -> Optional[InstrumentError]:
        code, message = self.query("SYSTem:ERRor?").split(", ")
        if int(code):
            return InstrumentError(int(code), message.strip("'"))
        return None

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
        self.write(f"SOURce:VOLTage:LEVel:IMMediate:AMPLitude {level}")

    @property
    def current_compliance(self) -> float:
        return float(self.query("SOURce:CURRent:LEVel:IMMediate:AMPLitude?"))

    @current_compliance.setter
    def current_compliance(self, level: float) -> None:
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
        print(self.resource.buffer)
        self.resource.write(message)
        print(self.resource.buffer)
        self.query("*OPC?")
        print(self.resource.buffer)


class NGE100(PowerSupply):
    """Rohde & Schwarz NGE100 power supply featuring multiple channels"""

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
        return NGE100Channel(self.resource, channel)

    def __iter__(self) -> Iterator[NGE100Channel]:
        return iter([NGE100Channel(self.resource, channel) for channel in range(3)])
