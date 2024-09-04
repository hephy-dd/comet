from comet.driver.generic import Instrument, InstrumentError
from typing import Optional

__all__ = ["PM100"]


def parse_error(response: str):
    code, message = [token.strip() for token in response.split(",")][:2]
    return int(code), message.strip('"')


class PM100(Instrument):
    """Class for controlling Thorlabs PM100 USB power meters"""

    WAVELENGTH_UV: int = 370
    WAVELENGTH_IR: int = 1060

    def identify(self) -> str:
        return self.query("*IDN?")

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
    def average_count(self) -> int:
        """Get current average count

        Returns:
            int: Average count
        """
        return int(self.query("SENSe:AVERage:COUNt?"))

    @average_count.setter
    def average_count(self, value: int) -> None:
        """Set average count

        One sample is around 3ms of measurement time.
        Default is 100 samples.

        Args:
            value (int): _description_
        """
        self.write(f"SENSe:AVERage:COUNt {value}")

    @property
    def wavelength(self) -> int:
        """Get calibration wavelength

        Returns:
            int: Calibration wavelength in nm
        """
        return int(float(self.query("SENSe:CORRection:WAVelength?")))

    @wavelength.setter
    def wavelength(self, value: int) -> None:
        """Set calibration wavelength

        Args:
            wavelength (int): Wavelength in nm
        """

        if value > 1100 or value < 350:
            raise ValueError("Wavelength must be between 350 and 1100 nm")

        self.write(f"SENSe:CORRection:WAVelength {value}")

    def measure_power(self) -> float:
        """Measure power

        Returns:
            float: Power in W
        """

        return float(self.query("MEASure:POWer?").strip())

    # Helpers
    def query(self, message: str) -> str:
        return self.resource.query(message).strip()

    def write(self, message: str) -> None:
        self.resource.write(message)
        self.query("*OPC?")
