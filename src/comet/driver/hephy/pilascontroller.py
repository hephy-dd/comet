"""
HEPHY PILAS GUI

LS? / LS=x        -> Laser Status
IL?               -> Interlock Status
TM? / TM=x        -> Tune Mode
TV? / TV=x.x      -> Tune Value
LT?               -> Laser Temperature
IF? / IF=xxxxxxxx -> Internal Frequency
???               -> Help/command list
"""

from comet.driver import Driver

__all__ = ["PilasController"]


class PilasController(Driver):
    """Class for controlling NKT Photonics PILAS via HEPHY Pilas Controller."""

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    TUNE_MANUAL: bool = False
    TUNE_AUTO: bool = True

    def identify(self) -> str:
        self._query("LS?")  # test connection
        return "Picosecond Laser System"

    @property
    def output(self) -> bool:
        return int(self._query("LS?")) == 1

    @output.setter
    def output(self, state: bool) -> None:
        self._write(f"LS={state:d}")

    @property
    def interlock(self) -> bool:
        return int(self._query("IL?")) == 1

    @property
    def tune_mode(self) -> bool:
        return int(self._query("TM?")) == 1

    @tune_mode.setter
    def tune_mode(self, state: bool) -> None:
        self._write(f"TM={state:d}")

    @property
    def tune(self) -> float:
        return float(self._query("TV?").replace("%", ""))

    @tune.setter
    def tune(self, value: float) -> None:
        value = float(value)
        if value < 0 or value > 100:
            raise ValueError("Tune value must be between 0 and 100")
        self.tune_mode = self.TUNE_MANUAL
        self._write(f"TV={value:.1f}")

    @property
    def frequency(self) -> int:
        return int(self._query("IF?").replace("Hz", ""))

    @frequency.setter
    def frequency(self, frequency: int) -> None:
        frequency = int(frequency)
        if frequency < 25 or frequency > 40e6:
            raise ValueError("Frequency must be between 25Hz and 40MHz")
        self._write(f"IF={frequency:d}")

    @property
    def laser_head_temperature(self) -> float:
        return float(self._query("LT?").replace("°C", ""))

    def _query(self, message: str) -> str:
        self.resource.write(message)
        return self.resource.read(encoding="latin1").strip()

    def _write(self, message: str) -> None:
        self.resource.write(message)
