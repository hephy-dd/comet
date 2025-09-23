"""Rohde Schwarz SMA100B signal generator emulator"""

from comet.emulator import IEC60488Emulator
from comet.emulator import BinaryResponse, message, run
from comet.emulator.utils import SCPIError, scpi_bool, scpi_pack_real32, generate_waveform


__all__ = ["RTP164Emulator"]


class RTP164Emulator(IEC60488Emulator):
    IDENTITY: str = "Rohde&Schwarz,RTP,1320.5007k16/123456,5.50.2.0"

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: list[SCPIError] = []
        self.num_samples: int = 1000
        self.channel_state: dict[int, bool] = {}

    @message(r"\*IDN\?$")
    def identify(self) -> str:
        return self.IDENTITY

    @message(r"\*RST$")
    def set_reset(self) -> None:
        self.error_queue.clear()

    @message(r"\*CLS$")
    def set_clear(self) -> None:
        self.error_queue.clear()

    @message(r":?SYST(?:em)?:ERR(?::NEXT)?\?$")
    def get_system_error_next(self) -> str:
        if self.error_queue:
            error = self.error_queue.pop(0)
        else:
            error = SCPIError(0, "No error")
        return str(error)

    @message(r":?SING(?:LE)?$")
    def set_single(self) -> None:
        ...

    @message(r":?CHAN([1-4]):STAT\?$")
    def get_channel_state(self, channel) -> str:
        return str(int(self.channel_state.get(int(channel), False)))

    @message(r":?CHAN([1-4]):STAT\s+(OFF|ON|0|1)$")
    def set_channel_state(self, channel, enabled) -> None:
        self.channel_state[int(channel)] = scpi_bool(enabled)

    @message(r":?CHAN([1-4]):DATA:HEAD\?$")
    def get_channel_data_header(self, channel) -> str:
        window = 1e-3
        return f"{-(window / 2):E},{window / 2:E},{self.num_samples:d},0"

    @message(r":?CHAN([1-4]):DATA\?$")
    def get_channel_data(self, channel) -> BinaryResponse:
        values = generate_waveform(self.num_samples, 1e-3)  # TODO
        return BinaryResponse(scpi_pack_real32(values))

    @message(r"(.*)$")
    def undefined_header(self, command) -> None:
        self.error_queue.append(SCPIError(-113, "Undefined header"))


if __name__ == "__main__":
    run(RTP164Emulator())
