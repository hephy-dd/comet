import time
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

__all__ = [
    "Error",
    "SCPIError",
    "generate_waveform",
    "scpi_parse_bool",
    "tsp_assign",
    "tsp_print",
    "TimeGradient",
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
        return f'{self.code},"{self.message}"'


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


def generate_waveform(
    n_points: int = 1000,
    duration: float = 1e-3,  # 1 ms total time
    baseline: float = 0.0,  # DC baseline level
    spike_time: float = 0.5e-3,  # spike occurs at 0.5 ms
    spike_width: float = 5e-6,  # spike duration 5 µs
    spike_amplitude: float = 2.0,  # spike height
    noise_std: float = 0.0,  # optional Gaussian noise
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
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


class TimeGradient:
    def __init__(
        self,
        value: float,
        target: float | None = None,
        rate: float = 1.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.value = float(value)
        self.target = self.value if target is None else float(target)
        self.rate = float(rate)

        self._clock = clock
        self._time = clock()

    def update(self) -> float:
        now = self._clock()
        step = self.rate * (now - self._time)
        self._time = now

        delta = self.target - self.value
        self.value += max(-step, min(step, delta))
        return self.value

    def set(self, target: float) -> None:
        self.update()
        self.target = float(target)
