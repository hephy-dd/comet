from .rtp164 import RTP164, RTP164Channel

__all__ = ["RTO6", "RTO6Channel"]


class RTO6Channel(RTP164Channel):
    """Single channel of the RTO6 oscilloscope"""


class RTO6(RTP164):
    """Rohde & Schwarz RTO6 oscilloscope with 4 channels"""
