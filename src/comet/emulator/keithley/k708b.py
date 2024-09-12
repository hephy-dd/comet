from comet.emulator import run
from comet.utils import combine_matrix

from .k707b import K707BEmulator


class K708BEmulator(K707BEmulator):

    IDENTITY: str = "Keithley Inc., Model 708B, 43768438, v1.0 (Emulator)"
    CHANNELS: list[str] = combine_matrix("1", "ABCDEFGH", "0", "12345678")


if __name__ == "__main__":
    run(K708BEmulator())
