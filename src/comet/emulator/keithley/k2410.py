from comet.emulator.keithley.k2400 import K2400Emulator, run


class K2410Emulator(K2400Emulator):

    IDENTITY: str = "Keithley Inc., Model 2410, 43768438, v1.0 (Emulator)"

    DEFAULT_VOLTAGE_PROTECTION_LEVEL: float = 1100.


if __name__ == "__main__":
    run(K2410Emulator())
