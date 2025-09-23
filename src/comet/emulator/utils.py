
import math
import random
import struct
from dataclasses import dataclass

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


def scpi_pack_real32(values: list[float]) -> bytes:
    return struct.pack('>' + 'f' * len(values), *values)


def generate_waveform(num_samples=1000, duration_s=1e-3):
    samples = []
    dt = duration_s / num_samples

    # parameters
    sine_freq = 50_000.0        # 50 kHz
    peak_center = 0.5e-3        # 0.5 ms
    peak_width = 10e-6          # 10 µs sigma
    peak_ampl = 1.0

    for n in range(num_samples):
        t = n * dt
        # base sine + tiny noise
        base = 0.1 * math.sin(2 * math.pi * sine_freq * t) + 0.01 * (random.random() - 0.5)
        # Gaussian bump
        gauss = peak_ampl * math.exp(-0.5 * ((t - peak_center) / peak_width) ** 2)
        samples.append(base + gauss)

    # normalize roughly to ±1
    max_abs = max(abs(x) for x in samples)
    if max_abs > 0:
        samples = [x / max_abs for x in samples]

    return samples
