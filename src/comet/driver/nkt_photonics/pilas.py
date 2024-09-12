"""Driver for NKT Photonics PILAS picosecond pulsed diode laser."""

from comet.driver import Driver

__all__ = ["PILAS"]


class PILAS(Driver):
    """Class for controlling NKT Photonics PILAS picosecond pulsed diode laser"""

    OUTPUT_ON: bool = True
    OUTPUT_OFF: bool = False

    TUNE_MANUAL: bool = False
    TUNE_AUTO: bool = True

    DIODE_TEMPERATURE_GOOD: bool = True
    DIODE_TEMPERATURE_BAD: bool = False

    def identify(self) -> str:
        self.resource.write("version?")
        # read 8 lines
        return "\n".join([self.resource.read().strip() for _ in range(8)])

    @property
    def output(self) -> bool:
        response = self.query_value("ld?")

        return response == "on"

    @output.setter
    def output(self, state: bool) -> None:
        value = {False: 0, True: 1}[state]
        self.write_and_check(f"ld={value}")

    @property
    def tune_mode(self) -> bool:
        response = self.query_value("tm?")

        return response == "auto"

    @tune_mode.setter
    def tune_mode(self, state: bool) -> None:
        value = {False: 0, True: 1}[state]
        self.write_and_check(f"tm={value}")

    @property
    def tune(self) -> float:
        return float(self.query_value("tune?").replace("%", ""))

    @tune.setter
    def tune(self, value: float) -> None:
        if value < 0 or value > 100:
            raise ValueError("Tune value must be between 0 and 100")

        self.tune_mode = self.TUNE_MANUAL

        self.write_and_check(f"tune={int(value*10)}")

    @property
    def frequency(self) -> int:
        return int(self.query_value("f?").replace("Hz", ""))

    @frequency.setter
    def frequency(self, frequency: int) -> None:
        if frequency < 25 or frequency > 40e6:
            raise ValueError("Frequency must be between 25Hz and 40MHz")
        self.write_and_check(f"f={frequency}")

    def get_laser_head_temperature(self) -> float:
        response = self.query_value("lht?")

        return float(response.replace("°C", ""))

    def get_laser_diode_temperature(self) -> bool:
        response = self.query_value("ldtemp?")
        return response == "good"

    # helper
    def query_value(self, command: str) -> str:
        self.resource.write(command)
        return self.resource.read(encoding="latin1").split(":")[1].strip()

    def write_and_check(self, command: str) -> None:
        self.resource.write(command)
        response = self.resource.read().strip()
        if response != "done":
            raise RuntimeError(
                f"Error sending command: {command}, received response {response}"
            )
