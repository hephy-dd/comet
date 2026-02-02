"""Driver for ECR AC3 thermal chuck"""

from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ["AC3Emulator"]


class AC3Emulator(Emulator):
    def __init__(self) -> None:
        super().__init__()

        self.temperature: float = 25.0
        self.target_temperature: float = 25.0
        self.mode: int = 1
        self.control_status: int = 1
        self.hold_mode: int = 11
        self.dewpoint_control_status: bool = True
        self.dewpoint: float = -20.0

    @message(r"^RC$")
    def get_temperature(self) -> str:
        return f"C{int(self.temperature*10):+05d}"

    @message(r"^RT$")
    def get_target_temperature(self) -> str:
        return f"T{int(self.target_temperature*10):+05d}"

    @message(r"^ST([+-]\d{4})$")
    def set_target_temperature(self, value: str) -> str:
        self.target_temperature = float(value) / 10
        self.temperature = self.target_temperature
        return "OK"

    @message(r"^RO$")
    def get_mode(self) -> str:
        return f"O{self.mode}"

    @message(r"^SO([1234])$")
    def set_mode(self, value: str) -> str:
        self.mode = int(value)
        return "OK"

    @message(r"^RF$")
    def get_dewpoint(self) -> str:
        return f"F{int(self.dewpoint*10):+05d}"

    @message(r"^RD$")
    def get_dewpoint_control_status(self) -> str:
        return f"D{int(self.dewpoint_control_status)}"

    @message(r"^SD([01])$")
    def set_dewpoint_control_status(self, value: str) -> str:
        self.dewpoint_control_status = bool(int(value))
        return "OK"

    @message(r"^RH$")
    def get_hold_mode(self) -> str:
        return f"H{self.hold_mode:02d}"

    @message(r"^SH([01])$")
    def set_hold_mode(self, value: str) -> str:
        val = int(value)
        if val == 0:
            self.hold_mode = 0
        else:
            self.hold_mode = 11
        return "OK"

    @message(r"^RI$")
    def get_control_status(self) -> str:
        return f"I{self.control_status}"

    @message(r"^RE$")
    def get_error(self) -> str:
        return "E000"


if __name__ == "__main__":
    run(AC3Emulator())
