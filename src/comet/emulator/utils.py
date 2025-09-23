
import math
import random
import struct
from dataclasses import dataclass

import numpy as np

__all__ = [
    "Error",
    "SCPIError",
    "tsp_print",
    "tsp_assign",
    "scpi_parse_bool",
    "generate_waveform",
]


@dataclass
class Error:
    """Generic error message container."""
    code: int
    message: str


@dataclass
class SCPIError(Error):
    """Generic SCPI error message container."""
    def __str__(self) -> str:
        return f"{self.code},\"{self.message}\""


def tsp_print(route: str) -> str:
    return rf"^print\({route}\)$"


def tsp_assign(route: str) -> str:
    return rf"^{route}\s*\=\s*(.+)$"


def scpi_parse_bool(s: str) -> bool:
    s = s.strip().upper()
    if s in ("ON", "1", "TRUE"):
        return True
    if s in ("OFF", "0", "FALSE"):
        return False
    raise ValueError(f"Not a SCPI boolean: {s!r}")


def scpi_pack_real32(values: list[float], big_endian: bool = False) -> bytes:
    endian_format = ">" if big_endian else "<"
    data_format = "f"
    return struct.pack(endian_format + data_format * len(values), *values)


def generate_waveform(
    n_points=1000,
    duration=1e-3,         # 1 ms total time
    baseline=0.0,          # DC baseline level
    spike_time=0.5e-3,     # spike occurs at 0.5 ms
    spike_width=5e-6,      # spike duration 5 µs
    spike_amplitude=2.0,   # spike height
    noise_std=0.0          # optional Gaussian noise
):
    """Create a waveform with a DC baseline and one spike for testing."""
    # Time axis
    t = np.linspace(0, duration, n_points, endpoint=False)

    # Baseline
    y = np.full_like(t, baseline)

    # Add spike using a Gaussian shape
    spike = spike_amplitude * np.exp(-0.5 * ((t - spike_time) / spike_width) ** 2)
    y += spike

    # Optional noise
    if noise_std > 0:
        y += np.random.normal(scale=noise_std, size=t.shape)

    return t, y
