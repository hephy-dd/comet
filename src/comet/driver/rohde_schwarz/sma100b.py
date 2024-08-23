from comet.driver.generic import Instrument, InstrumentError
from typing import Optional

__all__ = ["SMA100B"]


def parse_error(response: str):
    code, message = [token.strip() for token in response.split(",")][:2]
    return int(code), message.strip('"')


class SMA100B(Instrument):
    """Class for controlling Rohde&Schwarz SMA100B signal generator"""

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    def identify(self) -> str:
        return self.query("*IDN?").strip()

    def reset(self) -> None:
        self.write("*RST")

    def clear(self) -> None:
        self.write("*CLS")

    def next_error(self) -> Optional[InstrumentError]:
        code, message = parse_error(self.query(":SYST:ERR:NEXT?"))
        if code:
            return InstrumentError(code, message)
        return None

    @property
    def frequency_mode(self) -> str:
        """Get frequency mode

        FIXed | FIXed | SWEep| LIST | COMBined

        Returns:
            str: Frequency mode
        """
        return self.query("SOUR1:FREQ:MODE?")

    @frequency_mode.setter
    def frequency_mode(self, mode: str) -> None:
        """Set frequency mode

        FIXed | FIXed | SWEep| LIST | COMBined

        Args:
            mode (str): Frequency mode
        """
        self.write(f"SOUR1:FREQ:MODE {mode}")

    @property
    def frequency(self) -> float:
        """Get current frequency

        Returns:
            float: Frequency in Hz
        """
        return float(self.query("SOUR1:FREQuency:FIXed?"))

    @frequency.setter
    def frequency(self, frequency: float) -> None:
        """Set frequency

        Args:
            frequency (float): Frequency in Hz
        """

        if frequency < 8e3 or frequency > 12.75e9:
            raise ValueError("Frequency must be in range 8 kHz to 12.75 GHz")

        self.write(f"SOUR1:FREQuency:FIXed {frequency:.4f}")

    @property
    def output_power(self) -> float:
        """Get output power

        Returns:
            float: Output power in dBm
        """
        return float(self.query("SOUR1:POWer:POWer?"))

    @output_power.setter
    def output_power(self, power: float) -> None:
        """Set output power in dBm

        Args:
            power (float): Output power in dBm
        """
        if power < -145 or power > 40:
            raise ValueError("Power must be in range -145 dBm to 40 dBm")

        self.write(f"SOUR1:POWer:POWer {power}")

    @property
    def output(self) -> bool:
        value = int(float(self.query("OUTPut:STATe?")))
        return {0: self.OUTPUT_OFF, 1: self.OUTPUT_ON}[value]

    @output.setter
    def output(self, state: bool) -> None:
        value = {self.OUTPUT_OFF: "OFF", self.OUTPUT_ON: "ON"}[state]
        self.write(f"OUTPut:STATe {value}")

    # Helpers
    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query("*OPC?")
