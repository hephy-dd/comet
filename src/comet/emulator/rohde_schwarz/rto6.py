"""Rohde Schwarz RTO6 oscilloscope emulator"""

from comet.emulator import run

from .rtp164 import RTP164Emulator

__all__ = ["RTO6Emulator"]


class RTO6Emulator(RTP164Emulator):
    IDENTITY: str = "Rohde&Schwarz,RTO6,1802.0001k04/123456,5.50.2.0"


if __name__ == "__main__":
    run(RTO6Emulator())
