"""Photonic F3000 LED light source emulator"""

from comet.emulator import Emulator
from comet.emulator import message, run

__all__ = ["F3000Emulator"]


class F3000Emulator(Emulator):
    IDENTITY: str = "F3000 v2.09, Emulator"

    def __init__(self) -> None:
        super().__init__()

        self.current_brightness: int = 50
        self.light_enabled: bool = False

    @message(r"^V\?$")
    def get_version(self) -> str:
        return self.IDENTITY

    @message(r"^B(\d{1,3})$")
    def set_brightness(self, brightness: str) -> None:
        brightness = max(0, min(int(brightness), 100))
        self.current_brightness = int(brightness)

    @message(r"^B\?$")
    def get_brightness(self) -> str:
        return "B" + str(self.current_brightness)

    @message(r"^S\?$")
    def get_light_enabled(self) -> str:
        return "S0" if self.light_enabled else "S1"

    @message(r"^S(0|1)$")
    def set_light_enabled(self, light_enabled: str) -> None:
        self.light_enabled = not bool(int(light_enabled))


if __name__ == "__main__":
    run(F3000Emulator())
