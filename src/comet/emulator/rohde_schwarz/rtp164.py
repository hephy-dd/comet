"""Rohde Schwarz RTP164 oscilloscope emulator"""

from comet.emulator import IEC60488Emulator
from comet.emulator import BinaryResponse, message, run
from comet.emulator.utils import SCPIError, scpi_parse_bool, generate_waveform

__all__ = ["RTP164Emulator"]


class RTP164Emulator(IEC60488Emulator):
    IDENTITY: str = "Rohde&Schwarz,RTP,1320.5007k16/123456,5.50.2.0"

    def __init__(self) -> None:
        super().__init__()
        self.error_queue: list[SCPIError] = []
        self.format_border: str = "LSBF"
        self.format_data: str = "ASC,0"

        self.num_samples: int = 1000
        self.duration: float = 1e-3
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

    @message(r":?FORM(?:AT)?:BORD(?:ER)?\?$")
    def get_format_border(self) -> str:
        return self.format_border

    @message(r":?FORM(?:AT)?:BORD(?:ER)?\s+(LSBF(?:irst)?|MSBF(?:irst)?)$")
    def set_format_border(self, byte_order) -> None:
        self.format_border = byte_order[:4]

    @message(r":?FORM(?:AT)?(?::DATA)?\?$")
    def get_format_data(self) -> str:
        return self.format_data

    @message(r":?FORM(?:AT)?(?::DATA)?\s+(ASC|ASC,0|REAL,32|INT,8|INT,16)$")
    def set_format_data(self, format_length) -> None:
        if format_length == "ASC":
            format_length == "ASC,0"
        self.format_data = format_length

    @message(r":?SING(?:LE)?$")
    def set_single(self) -> None:
        ...

    @message(r":?CHAN([1-4]):STAT\?$")
    def get_channel_state(self, channel) -> str:
        return str(int(self.channel_state.get(int(channel), False)))

    @message(r":?CHAN([1-4]):STAT\s+(OFF|ON|0|1)$")
    def set_channel_state(self, channel, enabled) -> None:
        self.channel_state[int(channel)] = scpi_parse_bool(enabled)

    @message(r":?CHAN([1-4])(?::WAV([1-3]))?:DATA:HEAD\?$")
    def get_channel_waveform_data_header(self, channel, waveform) -> str:
        return f"{-(self.duration / 2):E},{self.duration / 2:E},{self.num_samples:d},1"

    @message(r":?CHAN([1-4])(?::WAV([1-3]))?:DATA(?::VAL)?\?$")
    def get_channel_waveform_data(self, channel, waveform) -> BinaryResponse:
        _, y = generate_waveform(self.num_samples, duration=self.duration, noise_std=0.01)  # TODO
        big_endian = self.format_border == "MSBF"
        return BinaryResponse.pack_real32(y, big_endian=big_endian)

    @message(r"(.*)$")
    def undefined_header(self, command) -> None:
        self.error_queue.append(SCPIError(-113, "Undefined header"))


if __name__ == "__main__":
    run(RTP164Emulator())
