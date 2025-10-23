"""NKT Photonics PILAS picosecond pulsed diode laser emulator"""

from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ["PILASEmulator"]


class PILASEmulator(Emulator):
    IDENTITY: str = (
        "controller serial: PLC1060CW0F00000715\n"
        + "laser head serial: PLH1060CW0F00000715\n"
        + "center wavelength: 1060 nm\n"
        + "CW laser option: no\n"
        + "CW laser power: fixed\n"
        + "software version: SW.PiLas.V1.1.AEb\n"
        + "controller hardware version: PiLas_Control_PCB_Rev.2.1\n"
        + "laser head hardware version: PiLas_Laser_Head_PCB_Rev.2.0"
    )

    def __init__(self) -> None:
        super().__init__()

        self.tune: float = 0
        self.tune_mode: bool = False
        self.output: bool = False
        self.frequency: int = 1000000

        self.laser_head_temperature: float = 25.0
        self.laser_diode_temperature: bool = True

    @message(r"^version\?$")
    def get_version(self) -> str:
        return self.IDENTITY

    @message(r"^ld\?$")
    def get_output(self) -> str:
        return "pulsed laser emission: " + ("on" if self.output else "off")

    @message(r"^ld=(0|1)$")
    def set_output(self, output: str) -> str:
        self.output = bool(int(output))
        return "done"

    @message(r"^tm\?$")
    def get_tune_mode(self) -> str:
        return "tune mode:\t" + ("auto" if self.tune_mode else "manual")

    @message(r"^tm=(0|1)$")
    def set_tune_mode(self, tune_mode: str) -> str:
        self.tune_mode = bool(int(tune_mode))
        return "done"

    @message(r"^tune\?$")
    def get_tune(self) -> str:
        return f"tune value:\t\t     {self.tune:.2f} %"

    @message(r"^tune=(\d{1,4})$")
    def set_tune(self, tune: int) -> str:
        self.tune = int(tune) / 10
        return "done"

    @message(r"^f\?$")
    def get_frequency(self) -> str:
        return f"int. frequency:\t       {self.frequency} Hz"

    @message(r"^f=(\d+)$")
    def set_frequency(self, frequency: int) -> str:
        self.frequency = int(frequency)
        return "done"

    @message(r"^lht\?$")
    def get_laser_head_temperature(self) -> str:
        return f"laser head temp.:\t     {self.laser_head_temperature} °C"

    @message(r"^ldtemp\?$")
    def get_laser_diode_temperature(self) -> str:
        return "LD temp.:\t\t" + ("good" if self.laser_diode_temperature else "bad")


if __name__ == "__main__":
    run(PILASEmulator())
