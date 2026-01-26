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

__all__ = ["PilasGui"]


class PilasGui(Driver):
    """Class for controlling NKT Photonics PILAS via PilasGui."""

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    TUNE_MANUAL: bool = False
    TUNE_AUTO: bool = True

    DIODE_TEMPERATURE_GOOD: bool = True
    DIODE_TEMPERATURE_BAD: bool = False

    def identify(self) -> str:
        self.resource.query("???")  # test connection
        return "PILAS GUI"

    @property
    def output(self) -> bool:
        response = self.query_value("LS?")
        return int(response) == 1

    @output.setter
    def output(self, state: bool) -> None:
        value = {False: 0, True: 1}[state]
        self.write_and_check(f"LS={value}")

    @property
    def tune_mode(self) -> bool:
        response = self.query_value("TM?")
        return int(response) == 1

    @tune_mode.setter
    def tune_mode(self, state: bool) -> None:
        value = {False: 0, True: 1}[state]
        self.write_and_check(f"TM={value}")

    @property
    def tune(self) -> float:
        return float(self.query_value("TV?"))

    @tune.setter
    def tune(self, value: float) -> None:
        if value < 0 or value > 100:
            raise ValueError("Tune value must be between 0 and 100")

        self.tune_mode = self.TUNE_MANUAL
        self.write_and_check(f"TV={float(value):.1f}")

    @property
    def frequency(self) -> int:
        return int(self.query_value("IF?"))

    @frequency.setter
    def frequency(self, frequency: int) -> None:
        if frequency < 25 or frequency > 40e6:
            raise ValueError("Frequency must be between 25Hz and 40MHz")
        self.write_and_check(f"IF={int(frequency)}")

    @property
    def laser_head_temperature(self) -> float:
        return float(self.query_value("LT?"))

    @property
    def laser_diode_temperature(self) -> bool:
        return True  # Not supported

    @property
    def interlock(self) -> bool:
        return int(self.query_value("IL?")) == 1

    # helpers
    def query_value(self, command: str) -> str:
        self.resource.write(command)
        return self.resource.read().strip()

    def write_and_check(self, command: str) -> None:
        self.resource.write(command)
        response = self.resource.read().strip()

        ok_responses = {"done", "ok", "OK", "1", "true", "True"}
        if response not in ok_responses:
            raise RuntimeError(
                f"Error sending command: {command}, received response {response!r}"
            )
