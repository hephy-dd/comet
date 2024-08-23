""" Driver for NKT Photonics PILAS picosecond pulsed diode laser """

from comet.driver import Driver
from typing import Optional

__all__ = ["PILAS"]


class PILAS(Driver):
    """Class for controllingNKT Photonics PILAS picosecond pulsed diode laser"""

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    TUNE_MANUAL: bool = False
    TUNE_AUTO: bool = True

    def identify(self) -> str:
        return self.resource.query("version?")

    @property
    def output(self) -> bool:
        return bool(int(self.resource.query("ld?")))

    @output.setter
    def output(self, state: bool) -> None:
        value = {False: 0, True: 1}[state]
        self.resource.write(f"ld={value}")

    @property
    def tune_mode(self) -> bool:
        return bool(int(self.resource.query("tm?")))

    @tune_mode.setter
    def tune_mode(self, state: bool) -> None:
        value = {False: 0, True: 1}[state]
        self.resource.write(f"tm={value}")

    @property
    def tune(self) -> float:
        return int(self.resource.query("tune?")) / 10

    @tune.setter
    def tune(self, value: float) -> None:
        if value < 0 or value > 100:
            raise ValueError("Tune value must be between 0 and 100")

        if self.tune_mode != self.TUNE_MANUAL:
            self.tune_mode = self.TUNE_MANUAL

        self.resource.write(f"tune={int(value*10)}")

    @property
    def frequency(self) -> int:
        return int(self.resource.query("f?"))

    @frequency.setter
    def frequency(self, frequency: int) -> None:
        if frequency < 25 or frequency > 40e6:
            raise ValueError("Frequency must be between 25Hz and 40MHz")
        self.resource.write(f"f={frequency}")

    @property
    def laser_diode_temperature(self) -> str:
        return float(self.resource.query("ldtemp?")) / 100

    @property
    def laser_head_temperature(self) -> float:
        return float(self.resource.query("lht?")) / 100
